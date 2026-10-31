# Discord AI Assistant Bot (Gemini 3.5 Flash Lite & Neon DB)

Многофункциональный Discord-бот на базе нейросетей Google Gemini (основная модель Gemini 3.5 Flash Lite) с бессерверной базой данных Neon PostgreSQL. Бот поддерживает мультимодальные вложения (видео, аудио, изображения, файлы), контекстную долговременную память, интерактивное голосовое общение, воспроизведение YouTube-аудио и администрирование сервера через AI Function Calling.

## Ключевые возможности

- **Языковое ядро Gemini 3.5 Flash Lite**:
  - Быстрая генерация ответов с низкими задержками и поддержкой высокой креативности (температура настроена на 1.2).
  - Каскадная лестница моделей (fallback): при исчерпании лимитов или временных сбоях эндпоинта запрос автоматически перенаправляется на `gemini-3.5-flash`, `gemini-3.1-flash-lite` и `gemini-2.5-flash`.
  - Отключенные фильтры цензуры (`HarmBlockThreshold.BLOCK_NONE`) для раскрепощенных и живых диалогов в закрытом комьюнити.
- **Мультимодальный анализ вложений**:
  - Распознавание изображений, документов и прямое чтение видео- и аудиофайлов через Google File API.
- **Бессерверная память в Neon PostgreSQL**:
  - Асинхронный пул соединений через `asyncpg`.
  - Автоматическая инициализация таблицы `memory` с составным индексом по `(channel_id, timestamp DESC)`.
  - Сохранение истории диалога и извлечение скользящего контекста (по умолчанию 40 сообщений) для каждого канала отдельно.
  - Локальный in-memory fallback при временном отсутствии подключения к базе данных.
- **Голосовые возможности и YouTube**:
  - Подключение к голосовым каналам сервера по текстовой команде пользователя или по решению нейросети (`join_voice`).
  - Воспроизведение звука с YouTube через `yt-dlp` (`play_youtube`, `stop_youtube`).
  - Экспериментальный Live-режим двустороннего аудиопотока через Gemini Live API (`gemini-2.5-flash-native-audio-latest`).
- **AI-модерация через Function Calling**:
  - Исполнение административных команд (кик, бан, мут/таймаут, управление ролями) только по запросу назначенного администратора (`ADMIN_ID`).
  - Распознавание команд с опечатками и разговорным контекстом ("заглуши его", "выдай роль гостя").

---

## Архитектура проекта

```
ai-pony-bot/
├── bot.py             # Главная точка входа, обработка событий Discord и вызов инструментов
├── ai_core.py         # Взаимодействие с Google Gemini API, fallback моделей и вложения
├── bot_settings.py    # Тонкие настройки нейросети, системных инструкций и параметров
├── config.py          # Загрузка переменных окружения и проверка ключей
├── memory.py          # Менеджер долговременной памяти на Neon PostgreSQL (asyncpg)
├── moderation.py      # Описание инструментов (Function Calling) и логика модерации
├── live_voice.py      # Модуль работы с голосовыми каналами и YouTube-стримингом
├── requirements.txt   # Зависимости Python
├── .env.example       # Шаблон переменных окружения
└── README.md          # Документация проекта
```

---

## Настройка параметров в коде (`bot_settings.py`)

Все ключевые поведенческие параметры вынесены в отдельный файл `bot_settings.py`. Вы можете изменять их без вмешательства в логику работы бота:

| Параметр | По умолчанию | Описание и рекомендации по кастомизации |
| :--- | :--- | :--- |
| `TEMPERATURE` | `1.2` | Креативность и вариативность ответов. Диапазон от `0.0` (строгие, предсказуемые ответы) до `2.0` (максимально безумные и свободные формулировки). Рекомендуется: `0.7` - `1.3`. |
| `TEXT_MODEL` | `"gemini-3.5-flash-lite"` | Основная текстовая модель. Можно заменить на `"gemini-3.5-flash"`, `"gemini-3.8-flash"` или `"gemini-2.5-pro"`. |
| `FALLBACK_MODELS` | `["gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-2.5-flash"]` | Список резервных моделей в порядке приоритета. Если основная модель возвращает ошибку квоты или таймаут, бот автоматически пробует следующую модель из списка. |
| `VOICE_MODEL` | `"gemini-2.5-flash-native-audio-latest"` | Модель для двустороннего аудиостриминга в реальном времени. Требует поддержку нативного звука. |
| `CONTEXT_LIMIT` | `40` | Количество последних сообщений канала, загружаемых в промпт в качестве предыстории. Можно увеличить или уменьшить в зависимости от расхода токенов. |
| `SYSTEM_INSTRUCTION` | Текст промпта | Системный характер, правила общения и манера поведения бота. Здесь можно изменить личность, обращение к пользователям, язык общения или добавить новые правила. |

---

## Схема базы данных Neon PostgreSQL

Таблица создается автоматически при первом запуске:

```sql
CREATE TABLE IF NOT EXISTS memory (
    id SERIAL PRIMARY KEY,
    channel_id BIGINT,
    user_id BIGINT,
    username TEXT,
    content TEXT,
    is_bot BOOLEAN,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_channel_timestamp 
ON memory(channel_id, timestamp DESC);
```

---

## Переменные окружения

Создайте файл `.env` в корне проекта (на основе шаблона `.env.example`):

```bash
cp .env.example .env
```

Заполните переменные:

```env
# Токен бота из Discord Developer Portal (вкладка Bot -> Reset Token)
DISCORD_TOKEN="your_discord_bot_token"

# API ключ от Google Gemini (получить в Google AI Studio)
GEMINI_API_KEY="your_gemini_api_key"

# Числовой Discord ID администратора сервера (для выполнения команд модерации)
ADMIN_ID=862759084200558609

# Строка подключения к базе данных Neon Serverless PostgreSQL
DATABASE_URL="postgresql://neondb_owner:password@ep-wild-sunset-ashrz9sx.c-4.eu-central-1.aws.neon.tech/discord_bot_db?sslmode=require"
```

---

## Локальный запуск

1. Склонируйте репозиторий:
```bash
git clone https://github.com/DanislonZombovich/ai-pony-bot.git
cd ai-pony-bot
```

2. Создайте и активируйте виртуальное окружение Python:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите бота:
```bash
python bot.py
```

---

## Настройка прав в Discord Developer Portal

Для корректной работы бота включите в панели Discord Developer Portal следующие **Privileged Gateway Intents**:
- **MESSAGE CONTENT INTENT** (чтение сообщений для диалога)
- **SERVER MEMBERS INTENT** (поиск пользователей и управление ролями)
- **PRESENCE INTENT** (опционально)

В правах бота (Bot Permissions) укажите:
- Send Messages, Read Message History, Attach Files, Embed Links
- Connect, Speak, Use Voice Activity
- Manage Roles, Kick Members, Ban Members, Moderate Members
