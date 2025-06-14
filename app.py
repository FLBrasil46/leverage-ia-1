import os
import requests
from flask import Flask, request
from datetime import datetime, timedelta

app = Flask(__name__)
API_KEY = os.getenv("TD_APIKEY", "")  # defina essa variável no Render
BASE = "https://api.twelvedata.com"
ATIVOS = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]

def fetch_us_dividends(start, end):
    url = f"{BASE}/dividends_calendar?start_date={start}&end_date={end}&apikey={API_KEY}"
    try:
        r = requests.get(url)
        data = r.json()
        return data.get("dividends", []) if "dividends" in data else []
    except Exception as e:
        print(f"Erro na API: {e}")
        return []

@app.route("/")
def index():
    hoje = datetime.today().date()
    fim = hoje + timedelta(days=15)
    filtro = request.args.get("q", "").upper()

    dividendos = fetch_us_dividends(hoje.isoformat(), fim.isoformat())

    if filtro:
        dividendos = [d for d in dividendos if filtro in d['symbol']]
    else:
        dividendos = [d for d in dividendos if d['symbol'] in ATIVOS]

    rows = "".join(
        f"<tr><td>{d['symbol']}</td><td>{d['ex_date']}</td><td>{d['dividend']}</td></tr>"
        for d in dividendos
    )

    html = f"""
    <html><head><meta charset="utf-8"><title>Proventos EUA</title></head>
    <body style="font-family: sans-serif; padding: 20px;">
        <h1>Dividendos próximos 15 dias (EUA)</h1>
        <form>
            <input name="q" placeholder="Buscar ativo..." value="{filtro}">
            <button>Buscar</button>
        </form>
        <table border="1" cellpadding="5" style="margin-top: 20px; border-collapse: collapse;">
            <tr><th>Ativo</th><th>Data Ex</th><th>Valor</th></tr>
            {rows if rows else "<tr><td colspan='3'>Sem dados</td></tr>"}
        </table>
    </body></html>
    """
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
