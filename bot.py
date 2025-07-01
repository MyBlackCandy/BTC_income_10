import os
import time
import requests

TG_TOKEN = os.getenv("BOT_TOKEN")
TG_CHAT_ID = os.getenv("CHAT_ID")

BTC_ADDRESSES = [
    os.getenv("address_1", ""),
    os.getenv("address_2", ""),
    os.getenv("address_3", ""),
    os.getenv("address_4", ""),
    os.getenv("address_5", ""),
    os.getenv("address_6", ""),
    os.getenv("address_7", ""),
    os.getenv("address_8", ""),
    os.getenv("address_9", ""),
    os.getenv("address_10", "")
]

def send_message(msg):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    data = {"chat_id": TG_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram Error:", e)

def get_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
        return float(r["price"])
    except:
        return 0

def get_latest_btc_tx(address):
    try:
        url = f"https://blockchain.info/rawaddr/{address}"
        r = requests.get(url).json()
        txs = r.get("txs", [])
        for tx in txs:
            for out in tx.get("out", []):
                if out.get("addr") == address:
                    return tx, out["value"] / 1e8  # BTC value
    except:
        pass
    return None, None

def main():
    last_seen = {}
    while True:
        btc_price = get_price()
        for address in BTC_ADDRESSES:
            address = address.strip()
            if not address:
                continue
            tx, amount = get_latest_btc_tx(address)
            if tx and tx.get("hash") and tx["hash"] != last_seen.get(address):
                from_addr = tx.get("inputs", [{}])[0].get("prev_out", {}).get("addr", "不明")
                usd = amount * btc_price
                msg = f"🟢 *BTC 入金*
从: `{from_addr}`
到: `{address}`
💰 {amount:.8f} BTC ≈ ${usd:,.2f}
TXID: `{tx['hash']}`"
                send_message(msg)
                last_seen[address] = tx["hash"]
        time.sleep(10)

if __name__ == "__main__":
    main()
