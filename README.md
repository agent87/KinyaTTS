# KinyaTTS

A codebase for Kinyarwanda speech synthesis (text-to-speech) based on MB-iSTFT-VITS2 model in PyTorch.
The original codebase and description comes from [MB-iSTFT-VITS2](https://github.com/FENRlR/MB-iSTFT-VITS2) which itself is a hybrid combination of [vits2_pytorch](https://github.com/p0p4k/vits2_pytorch) and [MB-iSTFT-VITS](https://github.com/MasayaKawamura/MB-iSTFT-VITS).

An architectural depiction of the model is presented below and its details can be found the original sources.
![MB-iSTFT-VITS2 architecture](image6.png)

## Getting started

### Inference
2. Checkout the code in the [Inference](Inference) directory and install `monotonic_align` the `kinyatts` modules
````sh
pip install -e  ./Inference/monotonic_align/
pip install -e ./Inference/
````
3. Download the pre-trained Kinyarwanda TTS model [TTS_MODEL_ms_ktjw_istft_vits2_base_1M.pt](https://drive.google.com/file/d/1g37e5QtBAQwXUQRc36RNrJeiQqpgy83c/view)
4. Go to the `kinyatts` sub-directory and run an inference server using uwsgi
````
cd Inference/kinyatts/
nohup sh run.sh &
````
5. Alternatively use the provided Jupiter notebook to synthetise speech: [Inference/kinyatts/kinyatts_inference.ipynb](Inference/kinyatts/kinyatts_inference.ipynb)

### Training

Follow instructions in [Training codebase](Training/MB-iSTFT-VITS2/README.md) to install requirements and train a basic multi-speaker TTS model.

## Credits
- [FENRlR/MB-iSTFT-VITS2](https://github.com/FENRlR/MB-iSTFT-VITS2)
- [jaywalnut310/vits](https://github.com/jaywalnut310/vits)
- [p0p4k/vits2_pytorch](https://github.com/p0p4k/vits2_pytorch)
- [MasayaKawamura/MB-iSTFT-VITS](https://github.com/MasayaKawamura/MB-iSTFT-VITS)
- [ORI-Muchim/PolyLangVITS](https://github.com/ORI-Muchim/PolyLangVITS)
- [tonnetonne814/MB-iSTFT-VITS-44100-Ja](https://github.com/tonnetonne814/MB-iSTFT-VITS-44100-Ja)
- [misakiudon/MB-iSTFT-VITS-multilingual](https://github.com/misakiudon/MB-iSTFT-VITS-multilingual)