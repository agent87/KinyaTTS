import re

import torch
from scipy.io.wavfile import write
from torch.utils.data import DataLoader
import torchaudio

from kinyatts.tts.commons import intersperse
from kinyatts.tts.utils import get_hparams_from_file, load_checkpoint
from kinyatts.tts.data_utils import TextAudioSpeakerLoader, TextAudioSpeakerCollate
from kinyatts.tts.models import SynthesizerTrn
from kinyatts.tts.text import text_to_sequence
from kinyatts.tts.text.symbols import symbols

sid = 0
input = "Polisi y’u Rwanda ku bufatanye n’abaturage mu Karere ka Nyanza, yafashe umusore w’imyaka 18, wari ufite ibizingo bine by’insinga z’amashanyarazi zitujuje ubuziranenge yacuruzaga mu buryo bwa magendu."

# - paths
model_steps = 462000
path_to_config = "/home/nzeyi/KINLP/data/ms_ktjw_istft_vits2_base.json" # path to .json
path_to_model = f"/home/nzeyi/KINLP/data/G_{model_steps}.pth"

# check device
if torch.cuda.is_available() is True:
    device = "cuda:0"
else:
    device = "cpu"


def get_text(text, hps):
    text_norm = text_to_sequence(text)
    if hps.data.add_blank:
        text_norm = intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm


def vcms(inputstr, sid): # multi
    fltstr = re.sub(r"[\[\](){}]", "", inputstr)
    #fltstr = langdetector(fltstr) #- optional for cjke/cjks type cleaners
    stn_tst = get_text(fltstr, hps)
    speed = 1
    output = (f'mb_istft_{sid}_{model_steps}_'+inputstr.replace(' ', '_').replace("'","_"))[:40]
    with torch.no_grad():
        x_tst = stn_tst.to(device).unsqueeze(0)
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).to(device)
        sid = torch.LongTensor([sid]).to(device)
        audio = net_g.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8, length_scale=1 / speed)[0][
            0, 0].data.cpu().float()#.numpy()
    #write(f'{output}.wav', hps.data.sampling_rate, audio.numpy())
    torchaudio.save(f'{output}.wav', audio.unsqueeze(0), hps.data.sampling_rate)
    print(f'{output}.wav Generated!')


def ex_voice_conversion(sid_tgt): # dummy - TODO : further work
    #import IPython.display as ipd
    output_dir = 'ex_output'
    dataset = TextAudioSpeakerLoader(hps.data.validation_files, hps.data)
    collate_fn = TextAudioSpeakerCollate()
    loader = DataLoader(dataset, num_workers=0, shuffle=False, batch_size=1, pin_memory=False, drop_last=True, collate_fn=collate_fn)
    data_list = list(loader)
    # print(data_list)

    with torch.no_grad():
        x, x_lengths, spec, spec_lengths, y, y_lengths, sid_src = [x.to(device) for x in data_list[0]]
        '''
        sid_tgt1 = torch.LongTensor([1]).to(device)
        sid_tgt2 = torch.LongTensor([2]).to(device)
        sid_tgt3 = torch.LongTensor([4]).to(device)
        '''
        audio = net_g.voice_conversion(spec, spec_lengths, sid_src=sid_src, sid_tgt=sid_tgt)[0][0, 0].data.cpu().float().numpy()
        '''
        audio1 = net_g.voice_conversion(spec, spec_lengths, sid_src=sid_src, sid_tgt=sid_tgt1)[0][0, 0].data.cpu().float().numpy()
        audio2 = net_g.voice_conversion(spec, spec_lengths, sid_src=sid_src, sid_tgt=sid_tgt2)[0][0, 0].data.cpu().float().numpy()
        audio3 = net_g.voice_conversion(spec, spec_lengths, sid_src=sid_src, sid_tgt=sid_tgt3)[0][0, 0].data.cpu().float().numpy()
        '''

    write(f'./{output_dir}/output_{sid_src}-{sid_tgt}.wav', hps.data.sampling_rate, audio)
    print(f'./{output_dir}/output_{sid_src}-{sid_tgt}.wav Generated!')

    '''
    print("Original SID: %d" % sid_src.item())
    ipd.display(ipd.Audio(y[0].cpu().numpy(), rate=hps.data.sampling_rate, normalize=False))
    print("Converted SID: %d" % sid_tgt1.item())
    ipd.display(ipd.Audio(audio1, rate=hps.data.sampling_rate, normalize=False))
    print("Converted SID: %d" % sid_tgt2.item())
    ipd.display(ipd.Audio(audio2, rate=hps.data.sampling_rate, normalize=False))
    print("Converted SID: %d" % sid_tgt3.item())
    ipd.display(ipd.Audio(audio3, rate=hps.data.sampling_rate, normalize=False))
    '''
if __name__ == '__main__':
    hps = get_hparams_from_file(path_to_config)

    if "use_mel_posterior_encoder" in hps.model.keys() and hps.model.use_mel_posterior_encoder == True:
        print("Using mel posterior encoder for VITS2")
        posterior_channels = 80  # vits2
        hps.data.use_mel_posterior_encoder = True
    else:
        print("Using lin posterior encoder for VITS1")
        posterior_channels = hps.data.filter_length // 2 + 1
        hps.data.use_mel_posterior_encoder = False

    net_g = SynthesizerTrn(
        len(symbols),
        posterior_channels,
        hps.train.segment_size // hps.data.hop_length,
        n_speakers=hps.data.n_speakers, #- >0 for multi speaker
        **hps.model).to(device)
    _ = net_g.eval()

    _ = load_checkpoint(path_to_model, net_g, None)

    vcms(input, sid)
