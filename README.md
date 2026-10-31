# AURA: Voice AI Assistant

AURA understands your commands by voice or text. Simple commands (notes, expenses, time, date, open apps) are handled by a trained ML model. Open-ended questions go to an OpenAI model with function calling.

## Architecture

Voice or text, then intent classifier (scikit-learn), then local tools or LLM, then reply.

- `Aura/ml/`: intent classifier (dataset, training, evaluation)
- `Aura/router.py`: routes a command to a tool or the LLM
- `Aura/tools.py`: notes, expenses, open apps
- `Aura/brain.py`: OpenAI function calling
- `Aura/api.py`: FastAPI service (`POST /chat`, `GET /health`)
- `Aura/frontend/`: React UI
- `Aura/main.py`: voice assistant for the terminal (microphone and speaker)

## Run with Docker

Create `Aura/.env` with `OPENAI_API_KEY=your_key`, then:

```
docker compose up --build
```

Open http://localhost:3000 (UI) or http://localhost:8000/docs (API).

```
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "what is my total expense"}'
```

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
- LLM function calling is implemented but has had limited testing.
- The API has no authentication yet and must not be exposed publicly as is.

## Roadmap

- [x] Voice assistant (speech in, speech out)
- [x] Intent classifier with held-out evaluation
- [x] FastAPI service
- [x] Docker and docker-compose
- [x] React frontend
- [ ] AWS deployment
- [ ] Whisper speech-to-text