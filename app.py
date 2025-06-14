import os
import finnhub
from flask import Flask
from datetime import datetime

app = Flask(__name__)
API_KEY = os.environ.get("FINNHUB_KEY", "")
client = finnhub.Client(api_key=API_KEY)

ATIVOS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JNJ", "PG", "KO", "PFE", "NVDA"]

@app.route("/")
def index():
    hoje = datetime.today().strftime("%Y-%m-%d")
    all_rows = ""

    for ticker in ATIVOS:
        try:
            dividendos = client.stock_dividends(ticker, _from=hoje)
            for d in dividendos:
                ex_date = d.get('exDate', '—')
                payment_date = d.get('paymentDate', '—')
                amount = d.get('amount', 0)
                all_rows += f"<tr><td>{ticker}</td><td>{ex_date}</td><td>{payment_date}</td><td>{amount:.4f}</td></tr>"
        except Exception as e:
            print(f"Erro ao consultar {ticker}: {e}")

    html = f"""
    <html><head><meta charset="utf-8"><title>Leverage IA – Dividendos EUA</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head><body class="p-4">
    <h1>Dividendos previstos (EUA)</h1>
    <table class="table table-bordered table-striped mt-3">
    <thead><tr><th>Ativo</th><th>Data Ex</th><th>Data Pagamento</th><th>Valor</th></tr></thead>
    <tbody>{all_rows or '<tr><td colspan="4">Nenhum dividendo encontrado.</td></tr>'}</tbody>
    </table>
    <p class="text-muted">Dados fornecidos por <a href="https://finnhub.io">Finnhub</a>.</p>
    </body></html>
    """
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
