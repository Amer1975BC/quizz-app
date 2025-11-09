# Quiz App

Een eenvoudige FastAPI + Bootstrap quiz applicatie met Postgres en Traefik. Deze versie bevat fixes voor Safari (ES modules, click handlers) en directe feedback na antwoorden.

## Features
- FastAPI backend met sessies en Postgres via SQLAlchemy
- SPA frontend (Bootstrap) met directe feedback (groen/rood)
- Traefik reverse proxy ondersteuning
- Docker Compose voor lokale en productie-deployments

## Snel starten (Docker)

```bash
docker compose up -d --build
```

Bezoek vervolgens:
- Origin (Traefik): http://localhost:9080
- Via je domein (Traefik/Cloudflared): https://quiz.karovic.net (voorbeeld)

## Automatisch committen & pushen

Gebruik het script `scripts/push.sh` om snel wijzigingen op Git te zetten:

```bash
./scripts/push.sh "feat: update vragen"
```

Als je geen message meegeeft wordt automatisch een tijdstempel gebruikt.

### Cron (optioneel)
Voeg bijvoorbeeld elke 30 minuten auto-save toe:
```bash
*/30 * * * * /root/quiz-app/scripts/push.sh "chore: autosave" >> /root/quiz-app/push.log 2>&1
```


## Handmatig ontwikkelen
```bash
uvicorn webapi:app --reload --host 0.0.0.0 --port 8000
```

## Build en deploy
```bash
docker compose build quiz-app
docker compose up -d quiz-app
```

## Troubleshooting
- Hard refresh/Incognito bij frontend updates (JS versie querystring wordt gebruikt, bv. `app.js?v=20251109L`)
- Safari: click handlers zijn met `onclick` en directe `createElement` geïmplementeerd om issues te omzeilen

## Versie
Release tag: `v20251109L`
# quizz-app
