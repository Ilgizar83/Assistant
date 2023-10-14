import os
from gtts import gTTS
from io import BytesIO
import torch
import sounddevice as sd
import soundfile as sf
from omegaconf import OmegaConf

language = 'ru'
model_id = 'v3_1_ru'
device = torch.device('cpu')

# прогружаем русскую модель
model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language=language,
                                     speaker=model_id)
model.to(device)  # gpu or cpu
torch.set_num_threads(4)

# настройки
sample_rate = 48000
speaker = 'aidar'  # 'aidar', 'baya', 'kseniya', 'xenia', 'eugene', 'random', 'xenia'


def speaker_silero(text):
    print(text)
    audio = model.apply_tts(text=text,
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=True,
                            put_yo=True
                            )

    sd.play(audio, blocking=True)


def speaker_gtts(text):
    lang = 'ru'
    with BytesIO() as f:
        gTTS(text=text, lang=lang, slow=False).write_to_fp(f)
        f.seek(0)
        data, fs = sf.read(f)
        sd.play(data, fs, blocking=True)
