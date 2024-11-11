# BumsBot

BumsBot is an automated bot for daily sign-ins, tapping, and handling upgrades on the Bums platform, managed with the `uv` package manager.

## Features

- **Daily Sign-In**: Automatically checks in each day.
- **Tap Task**: Runs tapping tasks using user information.
- **Process Upgrades**: Continues upgrading as long as there are available funds.
- **Error Handling**: Logs errors and outputs status messages for easy tracking.

---

## Setup

### 1. Clone the Repository

To clone the repository, run:

```bash
git clone https://github.com/Praveensenpai/bumsBot.git
cd bumsBot
```

### 2. Install `uv` Package Manager

Windows:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Linux/macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Sync Environment with `uv`

```bash
uv sync --python 3.13
```

### 4. Run the Bot

```bash
uv run main.py
```

---

## .env Configuration

Create a `.env` file in the root directory with the following keys:

```plaintext
API_ID=45454
API_HASH=fdasfdsfadfad
REF_ID=ref_vJ8atdt5
SESSION_NAME=bums
PHONE=+91
SLEEP_DELAY_MINUTES=30  # Adjust the delay as needed
```

| Key                   | Description                     |
| --------------------- | ------------------------------- |
| `API_ID`              | Your Telegram API ID            |
| `API_HASH`            | Your Telegram API Hash          |
| `REF_ID`              | Referral ID                     |
| `SESSION_NAME`        | Session name, set to **bums**   |
| `PHONE`               | Your phone number               |
| `SLEEP_DELAY_MINUTES` | Delay between tasks, in minutes |

---

## Notes

- **No Proxy**: The bot operates without any proxy settings.
- **Single Session**: Only one active session is supported at a time.
- **Future Enhancements**: A task completion feature will be added in future updates.
