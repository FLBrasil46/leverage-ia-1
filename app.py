import os
import finnhub
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)
API_KEY = os.environ.get("FINNHUB_KEY", "")
client = finnhub.Client(api_key=API_KEY)

ATIVOS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JNJ", "PG", "KO", "PFE", "NVDA"]

@app.route("/")
def index():
    filtro = request.args.get("q", "").upper()
    hoje = datetime.today().strftime("%Y-%m-%d")

    all_rows = ""
    for t in ATIVOS:
        try:
            divs = client.stock_dividends(t, _from=hoje)
            for d in divs:
                ex = d.get('exDate', '—')
                pay = d.get('paymentDate', '—')
                amount = d.get('amount', 0)
                if not filtro or filtro in t:
                    all_rows += f"<tr><td>{t}</td><td>{ex}</td><td>{pay}</td><td>{amount:.4f}</td></tr>"
        except Exception as e:
            print(f"Erro ao consultar {t}: {e}")

    html = f"""
    <html><head><meta charset="utf-8"><title>Leverage IA – Dividendos EUA</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"></head>
    <body class="p-4"><h1>Dividendos EUA (Futuros)</h1>
    <form><input name="q" placeholder="Filtrar ticker" value="{filtro}"><button>Buscar</button></form>
    <table class="table table-striped mt-3"><thead><tr>
    <th>Ativo</th><th>Data Ex</th><th>Pagamento</th><th>Valor</th></tr></thead><tbody>
    {all_rows or "<tr><td colspan='4'>Nenhum dividendo encontrado</td></tr>"}
    </tbody></table>
    <p class="text-muted">Dados via <a href="https://finnhub.io">Finnhub</a>.</p></body></html>"""
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
