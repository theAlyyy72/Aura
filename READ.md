# AURA: Voice AI Assistant

AURA listens to your voice, understands the command, and replies by speech.

## How it works

Mic, speech-to-text, intent classifier (scikit-learn), then either local tools (notes, expenses, time, date, open apps) or an OpenAI model with function calling, and finally text-to-speech.

Simple commands are handled locally by a trained ML model (fast and free). Open-ended conversation goes to the LLM, which can call the same tools.

## Intent classifier

TF-IDF + Logistic Regression, 9 intents, 174 training examples (template-generated).

| Version | Change | Accuracy |
|---|---|---|
| v1 | 5 templates per intent | 37.9% (dev set, 29 sentences) |
| v2 | balanced classes, more varied data | 93.1% (dev set) |
| v3 | C=10 (sharper probabilities) | 96.55% (dev set) |
| final | held-out test, 40 new sentences | 95.0% (38/40) |

Approximate 95% confidence interval for the final number: 83% to 99% (small test set).

## Limitations

- Training data is synthetic. Real speech is noisier.
- Google speech recognition sometimes mishears commands ("add" becomes "at").
- The test set was written by the same author as the training templates, so real-world accuracy is likely lower.

## Roadmap

- [ ] FastAPI service
- [ ] Docker
- [ ] AWS deployment
- [ ] Whisper speech-to-text