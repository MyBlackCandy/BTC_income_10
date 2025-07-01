
import os
import time
import requests

TG_TOKEN = os.getenv("BOT_TOKEN")
TG_CHAT_ID = os.getenv("CHAT_ID")

BTC_ADDRESSES = [
    os.getenv('address_1', '').strip(),
    os.getenv('address_2', '').strip(),
    os.getenv('address_3', '').strip(),
    os.getenv('address_4', '').strip(),
    os.getenv('address_5', '').strip(),
    os.getenv('address_6', '').strip(),
    os.getenv('address_7', '').strip(),
    os.getenv('address_8', '').strip(),
    os.getenv('address_9', '').strip(),
    os.getenv('address_10', '').strip(),
]

def send_message(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    data = {"chat_id": TG_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram ERROR:", e)

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
    except Exception as e:
        print("BTC API ERROR:", e)
    return None

def main():
    last_seen = {}
    while True:
        btc_price = get_price()
        for btc in BTC_ADDRESSES:
            btc = btc.strip()
            if not btc:
                continue
            tx = get_latest_btc_tx(btc)
            if tx and tx["hash"] != last_seen.get(btc):
                total = sum([out["value"] for out in tx["out"] if out.get("addr") == btc]) / 1e8
                usd = total * btc_price
                from_addr = tx.get("inputs", [{}])[0].get("prev_out", {}).get("addr", "不明")
                msg = f"🟢 *BTC 入金*\n👤 从: `{from_addr}`\n👥 到: `{btc}`\n💰 {total:.8f} BTC ≈ ${usd:,.2f}"
                send_message(msg)
                last_seen[btc] = tx["hash"]
        time.sleep(10)

if __name__ == "__main__":
    main()
