## 2024-05-18 - Transform Dead-End Errors into Actionable Empty States
**Learning:** In Telegram bots, displaying static error messages that tell users to run another command (e.g., "Run /start or /daerah first") breaks the flow and increases friction.
**Action:** Always provide the prerequisite setup UI (like inline keyboards for selecting options) directly within the error response. This turns a dead-end into an actionable empty state.
