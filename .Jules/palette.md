## 2025-02-14 - Telegram Bot Menu Discovery
**Learning:** Telegram bots often lack obvious discovery of commands for end-users, requiring them to memorize or lookup commands via `/help`. We can use `set_my_commands` API to register commands so they appear in autocomplete and the bot menu, a highly impactful micro-UX improvement for conversational interfaces.
**Action:** When working on Telegram bots, always ensure the bot commands are registered with Telegram API (`set_my_commands`) so users have discoverability and a graphical menu.## 2023-08-15 - Chat Action Order
**Learning:** In Telegram bots, sending a chat action (like typing or upload_photo) must be done *after* sending any loading messages, because sending any message immediately clears the bot's current chat action in the UI.
**Action:** Always dispatch `ChatAction` after sending loading messages so the action persists during the long-running operation.

## 2026-08-17 - Inline Action for Error States
**Learning:** When a user attempts an action but lacks a prerequisite (like setting a region), telling them to run a different command creates friction and a dead-end experience. Providing the required interactive element (e.g., inline keyboard) directly in the error message significantly improves UX by allowing them to resolve the issue without context switching.
**Action:** For conversational interfaces, always replace dead-end error text that says 'use X command first' with an inline UI that lets the user accomplish the prerequisite immediately.
