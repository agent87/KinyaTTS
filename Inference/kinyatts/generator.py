import warnings
from typing import Tuple
import re
import torch
from io import BytesIO
import torchaudio
from kinyatts.tts.commons import intersperse
from kinyatts.tts.utils import get_hparams_from_file, load_checkpoint
from kinyatts.tts.models import SynthesizerTrn
from kinyatts.tts.text import text_to_sequence
from kinyatts.tts.text.symbols import symbols

warnings.filterwarnings("ignore")

class Generator:
    inference_engine = (None, None, None, None)

    @staticmethod
    def setup():
        device = torch.device('cpu')
        if torch.cuda.is_available():
            device = torch.device('cuda:0')

        path_to_tts_config = 'ms_ktjw_istft_vits2_base.json'
        path_to_tts_model = 'TTS_MODEL_ms_ktjw_istft_vits2_base_1M.pt'
        tts_hps = get_hparams_from_file(path_to_tts_config)
        if "use_mel_posterior_encoder" in tts_hps.model.keys() and tts_hps.model.use_mel_posterior_encoder:
            print("Using mel posterior encoder for VITS2")
            posterior_channels = 80
            tts_hps.data.use_mel_posterior_encoder = True
        else:
            print("Using lin posterior encoder for VITS1")
            posterior_channels = tts_hps.data.filter_length // 2 + 1
            tts_hps.data.use_mel_posterior_encoder = False
        tts_model = SynthesizerTrn(
            len(symbols),
            posterior_channels,
            tts_hps.train.segment_size // tts_hps.data.hop_length,
            n_speakers=tts_hps.data.n_speakers,
            **tts_hps.model
        ).to(device)
        tts_model.eval()
        load_checkpoint(path_to_tts_model, tts_model, None)

        print('TTS API service ready!', flush=True)

        louder_vol = torchaudio.transforms.Vol(gain=3.0, gain_type="amplitude")

        Generator.inference_engine = (device, tts_model, tts_hps, louder_vol)

    @staticmethod
    def get_text(text, hps):
        text_norm = text_to_sequence(text)
        if hps.data.add_blank:
            text_norm = intersperse(text_norm, 0)
        return torch.LongTensor(text_norm)

    def __init__(self, inputstr):
        self.inputstr = inputstr
        self.audio_buffer = BytesIO()
        self.response = self.kinya_tts()

    def kinya_tts(self):
        device, tts_model, tts_hps, louder_vol = Generator.inference_engine
        fltstr = re.sub(r"[\[\](){}]", "", self.inputstr)
        stn_tst = Generator.get_text(fltstr, tts_hps)
        speed = 1
        with torch.no_grad():
            x_tst = stn_tst.to(device).unsqueeze(0)
            x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).to(device)
            audio = tts_model.infer(
                x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1 / speed
            )[0][0, 0].data.cpu().float()
        audio = louder_vol(audio.unsqueeze(0))
        torchaudio.save(self.audio_buffer, audio, tts_hps.data.sampling_rate, format='wav')
        self.audio_buffer.seek(0)
        return {"status_code": 0, "error": ""}