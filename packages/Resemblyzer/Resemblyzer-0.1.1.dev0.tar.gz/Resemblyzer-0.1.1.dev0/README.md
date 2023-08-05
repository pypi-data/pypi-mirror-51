Resemblyzer allows you to derive a **high-level representation of a voice** through a deep learning model called the voice encoder. Given an audio file of speech, it creates a summary vector of 256 values (an embedding, often shortened to "embed" in this repo) that summarizes the characteristics of the voice spoken. Resemblyzer has many uses:
- **Voice similarity metric**: compare different voices and get a value on how similar they sound. This leads to other applications:
  - **Speaker verification**: create a voice profile for a person from a few seconds of speech (5s - 30s) and compare it to that of new audio. Reject similarity scores below a threshold.
  - **Speaker diarization**: figure out who is talking when by comparing voice profiles with the continuous embedding of a speech segment.
  - **Fake speech detection**: verify if some speech is legitimate or fake by comparing the similarity of possible fake speech to real speech.
- **High-level feature extraction**: you can use the embeddings generated as feature vectors for your machine learning models! This also leads to other applications:
  - **Voice cloning**: see [this other project](https://github.com/CorentinJ/Real-Time-Voice-Cloning).
  - **Component analysis**: figure out accents, tones, prosody, gender, ... through component analysis of the embeddings.
  - **Virtual voices**: create entirely new voice embeddings by sampling from a prior distribution.
- **Loss function**: you can backpropagate through the voice encoder model and use it as a perceptual loss for your deep learning model! The voice encoder is written in PyTorch.

Resemblyzer is fast to execute (around 1000x real-time on a GTX 1080, with a minimum of 10ms for I/O operations), and can run both on CPU or GPU. It is robust to noise. It currently works best on English language only, but should still be able to perform somewhat decently on other languages.

## Examples
This is a short example showing how to use Resemblyzer:
```
from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path

fpath = Path("path_to_an_audio_file")
wav = preprocess_wav(fpath)

encoder = VoiceEncoder()
embed = encoder.embed_utterance(wav)
np.set_printoptions(precision=3, suppress=True)
print(embed)
```
More thorough examples demonstrating the use cases of Resemblyzer can be found in [examples.py](https://github.com/resemble-ai/Resemblyzer/blob/master/examples.py).

## Additional info
Resemblyzer emerged as a side project of the [Real-Time Voice Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning) repository. The pretrained model that comes with Resemblyzer is interchangeable with models trained in that repository, so feel free to finetune a model on new data and possibly new languages! The paper from which the voice encoder was implemented is [Generalized End-To-End Loss for Speaker Verification](https://arxiv.org/pdf/1710.10467.pdf) (in which it is called the *speaker* encoder).
