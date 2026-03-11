# LinkedIn AI Poster

A production-ready AI-powered LinkedIn Auto Posting System.

## Features
- Generates 2 LinkedIn posts daily (Bengali, motivational, software engineering topics)
- Sends posts to email for manual approval
- Publishes to LinkedIn only after approval
- Uses Gemini, OpenRouter, OpenAI APIs with fallback and key rotation
- Modular, robust, and fully automated

## Tech Stack
- Python 3.11
- FastAPI
- APScheduler
- SQLite
- Gmail SMTP
- LinkedIn API
- Gemini, OpenRouter, OpenAI APIs

## Folder Structure
```
linkedin_ai_poster/
  app/
    main.py
    config.py
    database.py
    scheduler.py
  ai/
    generator.py
    gemini_provider.py
    openrouter_provider.py
    openai_provider.py
    key_manager.py
  services/
    email_service.py
    linkedin_service.py
  models/
    post_model.py
  routes/
    approval_routes.py
  utils/
    logger.py
  .env
  requirements.txt
```

## Usage
1. Set your API keys and credentials in `.env`
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the server:
   ```
   uvicorn app.main:app --reload
   ```

## Workflow
- Scheduler triggers post generation
- AI generates post
- Email sent for approval
- Approve via link
- Post published to LinkedIn

## Environment Variables
- GEMINI_KEYS
- OPENROUTER_KEYS
- OPENAI_KEYS
- LINKEDIN_ACCESS_TOKEN
- LINKEDIN_PERSON_URN
- EMAIL_ADDRESS
- EMAIL_PASSWORD

## Logging & Error Handling
- Logs all actions
- Retries and fallback for AI providers
- Robust error handling

---

**Replace placeholder values in `.env` with your actual credentials.**
