import os
import requests
from flask import Flask, request
import json

app = Flask(__name__)

TD_APIKEY = os.environ.get("TD_APIKEY", "")  # configure essa variável no Render

def fetch_us_dividends(symbol):
    url = f"https://api.twelvedata.com/dividends?symbol={symbol}&apikey={TD_APIKEY}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def index():
    symbol = request.args.get("q", "AAPL").upper()

    data = fetch_us_dividends(symbol)

    # Resposta crua exibida no navegador para depuração
    html = f"""
    <html><head><meta charset="utf-8"><title>LEVERAGE IA</title></head>
    <body style="font-family:sans-serif; padding:20px">
        <h1>Consulta de Dividendos (Twelve Data)</h1>
        <form>
            <input name="q" placeholder="Digite o ticker americano" value="{symbol}">
            <button type="submit">Buscar</button>
        </form>
        <h2>Resposta da API:</h2>
        <pre>{json.dumps(data, indent=2)}</pre>
    </body></html>
    """
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
