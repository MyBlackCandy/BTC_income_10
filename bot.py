
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

def get_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
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
        pass
    return None

def main():
    last_seen = {}
    while True:
        btc_price = get_price()

        for addr in BTC_ADDRESSES:
            if not addr:
                continue
            addr = addr.strip()
            tx = get_latest_btc_tx(addr)
            if tx and tx.get("hash") and tx["hash"] != last_seen.get(addr):
                total = sum([out["value"] for out in tx["out"] if out.get("addr") == addr]) / 1e8
                usd_val = total * btc_price
                from_addr = tx.get("inputs", [{}])[0].get("prev_out", {}).get("addr", "unknown")
                msg = "[BTC] 入金\n客户地址: `{}`\n我们地址: `{}`\n💰 {:.8f} BTC ≈ ${:,.2f} USD".format(
                    from_addr, addr, total, usd_val)
                send_message(msg)
                last_seen[addr] = tx["hash"]
        time.sleep(10)

if __name__ == "__main__":
    main()
