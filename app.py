import os
import requests
from flask import Flask, request
import json

app = Flask(__name__)

TD_APIKEY = os.environ.get("TD_APIKEY", "")

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

    dividends = data.get("dividends", [])
    rows = ""
    labels = []
    values = []

    for d in dividends:
        date = d.get("ex_date", "—")
        amount = d.get("amount", 0)
        rows += f"<tr><td>{date}</td><td>{amount}</td></tr>"
        labels.append(f'"{date}"')
        values.append(amount)

    html = f"""
    <html><head><meta charset="utf-8"><title>LEVERAGE IA</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: sans-serif; padding: 20px; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
        th {{ background: #f0f0f0; }}
    </style>
    </head>
    <body>
        <h1>Dividendos - {symbol}</h1>
        <form>
            <input name="q" placeholder="Ticker americano" value="{symbol}">
            <button type="submit">Buscar</button>
        </form>
        <table>
            <tr><th>Data Ex</th><th>Valor</th></tr>
            {rows if rows else "<tr><td colspan='2'>Sem dados</td></tr>"}
        </table>
        <canvas id="grafico" width="600" height="200"></canvas>
        <script>
            new Chart(document.getElementById("grafico"), {{
                type: "bar",
                data: {{
                    labels: [{','.join(labels)}],
                    datasets: [{{
                        label: "Dividendos",
                        data: {json.dumps(values)},
                        backgroundColor: "rgba(54, 162, 235, 0.6)"
                    }}]
                }},
                options: {{
                    responsive: true,
                    scales: {{
                        y: {{
                            beginAtZero: true
                        }}
                    }}
                }}
            }});
        </script>
    </body></html>
    """
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
