# AI Отдел кадров

Проект включает телеграм-бота, который отвечает на вопросы новых сотрудников на основе информации о компании и коллегах. Ответы генерируются с помощью OpenAI API.

## Требования
- Python 3.10+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- Requests
- Доступ к OpenAI API

Установить зависимости:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Переменные окружения
- `TELEGRAM_BOT_TOKEN` — токен телеграм-бота.
- `OPENAI_API_KEY` — ключ доступа к OpenAI API.
- `OPENAI_MODEL` — (опционально) модель, по умолчанию `gpt-4o-mini`.
- `OPENAI_API_URL` — (опционально) URL эндпоинта chat completions.

Создайте файл `.env` или экспортируйте переменные в сессии:

```bash
export TELEGRAM_BOT_TOKEN="your-telegram-token"
export OPENAI_API_KEY="sk-your-openai-key"
```

## Запуск телеграм-бота

1. Создайте файл `.env` в корне проекта (или экспортируйте переменные в сессию) и добавьте ключи:

   ```bash
   TELEGRAM_BOT_TOKEN=your-telegram-token
   OPENAI_API_KEY=sk-your-openai-key
   OPENAI_MODEL=gpt-4o-mini           # можно оставить по умолчанию
   OPENAI_API_URL=https://api.openai.com/v1/chat/completions  # опционально
   ```

2. Активируйте виртуальное окружение и установите зависимости (см. раздел «Требования»).

3. Запустите бота в режиме long polling:

   ```bash
   python -m ai_hr_bot.bot
   ```

   Процесс должен оставаться запущенным, пока бот нужен; при старте в логах появится сообщение `Starting bot with model ...`.

4. Откройте Telegram, найдите своего бота и отправьте `/start`. В ответ придёт приветствие. Любое текстовое сообщение
   будет перенаправлено в OpenAI, а ответ вернётся в чат с рекомендацией, к кому обратиться в компании.

## Проверка без Телеграма

Скрипт `scripts/query_openai.py` отправляет вопрос прямо в OpenAI и выводит ответ:

```bash
python scripts/query_openai.py "Мне нужно подключить принтер к ноутбуку"
```

## Структура промпта

Инструкции для модели находятся в `ai_hr_bot/prompt_builder.py`. Они описывают компанию, ключевых сотрудников и то, что ответы должны быть короткими и ориентированными на действие.
