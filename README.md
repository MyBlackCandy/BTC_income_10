# BTC Income Bot (10 Addresses)

A simple Telegram bot that monitors **up to 10 BTC addresses** and notifies the Telegram group when any income transaction is detected.

## Features
- Monitors BTC transactions via blockchain.info
- Reports incoming transaction details (sender, receiver, amount, USD value)
- Designed for Railway deployment

## Environment Variables
| Variable      | Description                        |
|---------------|------------------------------------|
| BOT_TOKEN     | Telegram bot token                 |
| CHAT_ID       | Telegram chat ID (group/channel)   |
| address_1~10  | BTC address to monitor (up to 10)  |

## Deploy on Railway
1. Clone or upload this repo to Railway.
2. Set the environment variables.
3. Railway will auto-detect and start the bot.

## Requirements
```
pip install -r requirements.txt
```

## Start the bot
```
python bot.py
```
