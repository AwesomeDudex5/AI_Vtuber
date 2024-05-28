
from transformers import AutoProcessor, BarkModel
import scipy
import torch

print("processing_test")

processor = AutoProcessor.from_pretrained("suno/bark")
model = BarkModel.from_pretrained("suno/bark")

device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = model.to(device)

#setting up parameters
text_to_parse = "Hi, I'm Chuchu. I love watching anime."
voice_preset = "v2/en_speaker_1"

#passing into transformers processor
inputs = processor(text_to_parse, voice_preset=voice_preset)  

audio_array = model.generate(**inputs.to(device))
#audio_array = audio_array.cpu().numpy().squeeze()

#save as wav file
sample_rate = model.generation_config.sample_rate
scipy.io.wavfile.write("bark_out.wav", rate=sample_rate, data=audio_array[0].cpu().numpy())