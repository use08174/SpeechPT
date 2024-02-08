from pyannote.audio.tasks import VoiceActivityDetection
from pyannote.audio.pipelines import VoiceActivityDetection
from pyannote.audio import Model
# from pyannote.pipeline import Optimizer

# 1. visit hf.co/pyannote/segmentation and accept user conditions
# 2. visit hf.co/settings/tokens to create an access token
# 3. instantiate pretrained model

model = Model.from_pretrained("pyannote/segmentation", use_auth_token= True)

pipeline = VoiceActivityDetection(segmentation=model)

HYPER_PARAMETERS = {
  # onset/offset activation thresholds
  "onset": 0.3, "offset": 0.5,
  # remove speech regions shorter than that many seconds.
  "min_duration_on": 0.0,
  # fill non-speech regions shorter than that many seconds.
  "min_duration_off": 1.0
}
pipeline.instantiate(HYPER_PARAMETERS)
vad = pipeline(r"C:\Users\82102\Desktop\프메\audio_sumin_with_pause (2).wav")
# `vad` is a pyannote.core.Annotation instance containing speech regions

print(f'1초 이상 멈춤의 개수 : {len(vad)-1}개 입니다.')
idx = 21
for i in range(len(vad)-1) : 
  vad = str(vad)
  print(f'{vad[idx:idx+11]} ~ {vad[idx+24:idx+36]}')
  idx += 43