import os
import requests
from flask import Flask, request
from datetime import datetime, timedelta
import json

app = Flask(__name__)
TD_APIKEY = os.environ.get("TD_APIKEY", "")

ATIVOS_USA = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JNJ", "PG", "KO", "PFE", "NVDA"]

def fetch_dividends(ticker):
    url = f"https://api.twelvedata.com/dividends?symbol={ticker}&apikey={TD_APIKEY}"
    try:
        res = requests.get(url)
        return res.json().get("dividends", [])
    except Exception as e:
        print(f"Erro ao buscar {ticker}: {e}")
        return []

@app.route("/")
def index():
    hoje = datetime.today()
    fim = hoje + timedelta(days=90)

    all_rows = ""
    for ticker in ATIVOS_USA:
        divs = fetch_dividends(ticker)
        for d in divs:
            try:
                ex_date = datetime.strptime(d["ex_date"], "%Y-%m-%d")
                if hoje <= ex_date <= fim:
                    pay_date = d.get("pay_date", "—")
                    amount = d.get("amount", 0)
                    all_rows += f"<tr><td>{ticker}</td><td>{d['ex_date']}</td><td>{pay_date}</td><td>{amount}</td></tr>"
            except:
                continue

    html = f"""
    <html><head><meta charset="utf-8"><title>LEVERAGE IA - Dividendos</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
    </head><body class="p-4">
        <h1 class="mb-4">Dividendos Previstos (próximos 90 dias)</h1>
        <table class="table table-striped table-bordered table-hover">
            <thead class="table-dark">
                <tr><th>Ticker</th><th>Data Ex</th><th>Pagamento</th><th>Valor</th></tr>
            </thead>
            <tbody>
                {all_rows if all_rows else "<tr><td colspan='4'>Nenhum dividendo previsto</td></tr>"}
            </tbody>
        </table>
        <p class="text-muted">Dados fornecidos por Twelve Data para ativos dos EUA.</p>
    </body></html>
    """
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
