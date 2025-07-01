import os
import time
import requests

TG_TOKEN = os.getenv("BOT_TOKEN")
TG_CHAT_ID = os.getenv("CHAT_ID")
BTC_ADDRESSES = [os.getenv(f"address_{i}", "").strip() for i in range(1, 11)]
LAST_TX = {}

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
    try:
        url = f"https://blockchain.info/rawaddr/{address}"
        res = requests.get(url).json()
        txs = res.get("txs", [])
        for tx in txs:
            for out in tx["out"]:
                if out.get("addr") == address:
                    return tx
    except:
        pass
    return None

def main():
    global LAST_TX
    btc_price = get_price()
    while True:
        for addr in BTC_ADDRESSES:
            if not addr:
                continue
            tx = get_latest_btc_tx(addr)
            if tx and tx.get("hash") and tx["hash"] != LAST_TX.get(addr):
                total = sum(out["value"] for out in tx["out"] if out.get("addr") == addr) / 1e8
                usd_val = total * btc_price
                from_addr = tx.get("inputs", [{}])[0].get("prev_out", {}).get("addr", "unknown")
                msg = (
                    "[BTC 入金]\n"
                    f"👤 จาก: `{from_addr}`\n"
                    f"👥 ถึง: `{addr}`\n"
                    f"💰 {total:.8f} BTC ≈ ${usd_val:,.2f} USD\n"
                    f"🧾 TXID: `{tx['hash']}`"
                )
                send_message(msg)
                LAST_TX[addr] = tx["hash"]
        time.sleep(10)

if __name__ == "__main__":
    main()