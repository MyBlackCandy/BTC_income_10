import os
import time
import requests

TG_TOKEN = os.getenv("BOT_TOKEN")
TG_CHAT_ID = os.getenv("CHAT_ID")
BTC_ADDRESSES = [os.getenv(f"address_{i}") for i in range(1, 11)]
LAST_TX_FILE = "last_seen.txt"

def send_message(msg):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    data = {"chat_id": TG_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram Error:", e)

def get_price(symbol="BTCUSDT"):
    try:
        r = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}").json()
        return float(r["price"])
    except:
        return 0

def get_latest_btc_tx(address):
    url = f"https://blockchain.info/rawaddr/{address}"
    try:
        r = requests.get(url).json()
        txs = r.get("txs", [])
        for tx in txs:
            for out in tx["out"]:
                if out.get("addr") == address:
                    return tx
    except:
        return None

def load_last_seen():
    if not os.path.exists(LAST_TX_FILE):
        return {}
    with open(LAST_TX_FILE, "r") as f:
        return dict(line.strip().split("=", 1) for line in f if "=" in line)

def save_last_seen(seen):
    with open(LAST_TX_FILE, "w") as f:
        for k, v in seen.items():
            f.write(f"{k}={v}\n")

def main():
    last_seen = load_last_seen()
    btc_price = get_price()

    while True:
        updated = False
        for addr in BTC_ADDRESSES:
            if not addr:
                continue
            tx = get_latest_btc_tx(addr)
            if not tx or not tx.get("hash"):
                continue
            if last_seen.get(addr) == tx["hash"]:
                continue

            total = sum([out["value"] for out in tx["out"] if out.get("addr") == addr]) / 1e8
            from_addr = tx.get("inputs", [{}])[0].get("prev_out", {}).get("addr", "不明")
            usd = total * btc_price
            msg = f"""🟢 *BTC 入金*
从: `{from_addr}`
到: `{addr}`
💰 {total:.8f} BTC ≈ ${usd:,.2f} USD
📦 TXID: `{tx['hash']}`"""
            send_message(msg)
            last_seen[addr] = tx["hash"]
            updated = True

        if updated:
            save_last_seen(last_seen)

        time.sleep(10)

if __name__ == "__main__":
    main()
