## 2025-02-14 - Telegram Bot Menu Discovery
**Learning:** Telegram bots often lack obvious discovery of commands for end-users, requiring them to memorize or lookup commands via `/help`. We can use `set_my_commands` API to register commands so they appear in autocomplete and the bot menu, a highly impactful micro-UX improvement for conversational interfaces.
**Action:** When working on Telegram bots, always ensure the bot commands are registered with Telegram API (`set_my_commands`) so users have discoverability and a graphical menu.## 2023-08-15 - Chat Action Order
**Learning:** In Telegram bots, sending a chat action (like typing or upload_photo) must be done *after* sending any loading messages, because sending any message immediately clears the bot's current chat action in the UI.
**Action:** Always dispatch `ChatAction` after sending loading messages so the action persists during the long-running operation.

## 2026-08-19 - Actionable Empty States
**Learning:** In Telegram bots, displaying dead-end text like "You haven't selected a region. Use /start or /daerah" forces the user to remember and type a command. It is much better UX to provide the actionable inline keyboard directly within the error message, saving them steps and reducing friction.
**Action:** When a user lacks a prerequisite (like a selected region) for a command, always provide the necessary inline actionable UI immediately rather than just text instructions.
