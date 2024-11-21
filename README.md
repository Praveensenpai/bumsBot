# BumsBot

BumsBot is an automated bot for daily sign-ins, tapping, and handling upgrades on the Bums platform, managed with the `uv` package manager.

## Features

- **Daily Sign-In**: Automatically checks in each day.
- **Tap Task**: Runs tapping tasks using user information.
- **Process Upgrades**: Continues upgrading as long as there are available funds. Upgrade which is most profitable.
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

**Windows:**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/macOS:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Sync Environment with `uv`

```bash
uv sync
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

## Getting Your Telegram API ID and Hash

To obtain the **API ID** and **API Hash** for Telegram, follow these steps:

1. **Log in to Telegram**: Use the official [Telegram Web](https://web.telegram.org/) or app to log in to your account.

2. **Access the Telegram Developer Portal**:

   - Go to [https://my.telegram.org](https://my.telegram.org) and sign in with your Telegram credentials.

3. **Create a New Application**:

   - After logging in, click on **API Development Tools**.
   - Choose **Create new application** and fill in the required details, like the app name, platform (e.g., Desktop), and a short description.

4. **Get Your API ID and Hash**:
   - Once you complete the form, Telegram will provide you with an **API ID** and **API Hash**. Copy these and paste them into your `.env` file for BumsBot.

These credentials allow your bot to interact with Telegram. Keep them secure and avoid sharing them publicly.

---

## Notes

- **No Proxy**: The bot operates without any proxy settings.
- **Single Session**: Only one active session is supported at a time.
- **Future Enhancements**: A task completion feature will be added in future updates.
