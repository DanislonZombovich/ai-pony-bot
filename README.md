# Uncensored AI Discord Bot 

This is a powerful, AI-driven Discord bot powered by Google's Gemini API.

## Features
- **Uncensored Chat:** Utilizes Gemini 3.1 Flash Lite with Safety Settings explicitly turned off (`BLOCK_NONE`) to answer all queries without constraints.
- **Multimodal Support:** Analyzes images, documents, and videos directly attached in Discord chats.
- **Unified Memory:** Tracks conversation context natively across the server.
- **Admin Moderation:** Provides AI-driven execution of Discord moderation functions (kick, ban, timeout) that strictly respond only to the assigned Admin ID (Данислон).
- **Live Voice (Experimental):** Can join voice channels and process audio using the Gemini 3 Flash Live API.

## Setup
1. Define `.env` with the following:
   - `DISCORD_TOKEN`
   - `GEMINI_API_KEY`
   - `AIVEN_URI` (MongoDB URI for database)
   - `ADMIN_ID`
2. Install dependencies: `pip install -r requirements.txt`
3. Install additional voice dependency: `pip install discord-ext-voice-recv`
4. Run: `python bot.py`
