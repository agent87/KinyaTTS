from __future__ import print_function, division

# Ignore warnings
import warnings
from typing import Tuple

warnings.filterwarnings("ignore")

import torchaudio
from flask import Flask, request

import re

import torch

from kinyatts.tts.commons import intersperse
from kinyatts.tts.utils import get_hparams_from_file, load_checkpoint
from kinyatts.tts.models import SynthesizerTrn
from kinyatts.tts.text import text_to_sequence
from kinyatts.tts.text.symbols import symbols

inference_engine = (None, None, None, None)

def kinya_tts_setup():
    global inference_engine

    device = torch.device('cpu')
    if torch.cuda.is_available():
        device = torch.device('cuda:0')

    path_to_tts_config = 'ms_ktjw_istft_vits2_base.json'
    path_to_tts_model = 'TTS_MODEL_ms_ktjw_istft_vits2_base_1M.pt'
    tts_hps = get_hparams_from_file(path_to_tts_config)
    if "use_mel_posterior_encoder" in tts_hps.model.keys() and tts_hps.model.use_mel_posterior_encoder == True:
        print("Using mel posterior encoder for VITS2")
        posterior_channels = 80  # vits2
        tts_hps.data.use_mel_posterior_encoder = True
    else:
        print("Using lin posterior encoder for VITS1")
        posterior_channels = tts_hps.data.filter_length // 2 + 1
        tts_hps.data.use_mel_posterior_encoder = False
    tts_model = SynthesizerTrn(
        len(symbols),
        posterior_channels,
        tts_hps.train.segment_size // tts_hps.data.hop_length,
        n_speakers=tts_hps.data.n_speakers, #- >0 for multi speaker
        **tts_hps.model).to(device)
    _ = tts_model.eval()
    _ = load_checkpoint(path_to_tts_model, tts_model, None)

    print('TTS API service ready!', flush=True)

    louder_vol = torchaudio.transforms.Vol(gain=3.0, gain_type="amplitude")

    inference_engine = (device, tts_model, tts_hps, louder_vol)

def get_text(text, hps):
    text_norm = text_to_sequence(text)
    if hps.data.add_blank:
        text_norm = intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

def kinya_tts(inputstr, output_wav_file = 'kinyatts_output.wav') -> Tuple[str,float]: # multi-speaker-tts
    global inference_engine
    (device, tts_model, tts_hps, louder_vol) = inference_engine
    fltstr = re.sub(r"[\[\](){}]", "", inputstr)
    stn_tst = get_text(fltstr, tts_hps)
    speed = 1
    with torch.no_grad():
        x_tst = stn_tst.to(device).unsqueeze(0)
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).to(device)
        audio = tts_model.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1 / speed)[0][
            0, 0].data.cpu().float()
    AUDIO_TIME = audio.size(0) / tts_hps.data.sampling_rate
    audio = louder_vol(audio.unsqueeze(0))
    torchaudio.save(output_wav_file, audio, tts_hps.data.sampling_rate)
    return output_wav_file, AUDIO_TIME

kinya_tts_setup()
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["JSONIFY_MIMETYPE"] = "application/json; charset=utf-8"

@app.route('/tts', methods=['POST'])
def tts_task():
    content_type = request.headers.get('Content-Type')
    if ('application/json' in content_type):
        json = request.get_json()
        input = json['input']
        output,seconds = kinya_tts(input, output_wav_file=json['output'])
        json['output'] = output
        json['seconds'] = seconds
        json['task'] = 'tts'
        return json
    else:
        return 'Content-Type not supported!'

if __name__ == '__main__':
    # app.run(debug=False, host='0.0.0.0', port=8888)
    app.run()
