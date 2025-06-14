import os
import requests
from flask import Flask
from datetime import datetime
app = Flask(__name__)

FINNHUB_TOKEN = os.environ.get("FINNHUB_TOKEN", "")
HEADERS = {"X-Finnhub-Token": FINNHUB_TOKEN}
TICKERS = ["AAPL", "MSFT", "GOOGL", "TSLA"]

def get_dividends(ticker):
    url = f"https://finnhub.io/api/v1/stock/dividend?symbol={ticker}&from=2023-01-01&to=2025-12-31"
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        return data if isinstance(data, list) else []
    except Exception as e:
        print(f"Erro com {ticker}: {e}")
        return []

@app.route("/")
def index():
    table_rows = ""
    for ticker in TICKERS:
        dividendos = get_dividends(ticker)
        for d in dividendos:
            table_rows += f"<tr><td>{ticker}</td><td>{d.get('exDate')}</td><td>{d.get('paymentDate')}</td><td>{d.get('amount')}</td></tr>"

    html = f"""
    <html><head><title>Dividendos</title><meta charset="utf-8">
    <style>table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:8px}}</style></head>
    <body><h1>Dividendos Recentes</h1>
    <table><tr><th>Ativo</th><th>Data Ex</th><th>Pagamento</th><th>Valor</th></tr>
    {table_rows if table_rows else "<tr><td colspan='4'>Nenhum dado encontrado</td></tr>"}
    </table></body></html>
    """
    return html

if __name__ == "__main__":
    import sys
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
