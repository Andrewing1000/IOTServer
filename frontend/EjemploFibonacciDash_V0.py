# app.py

from flask import Flask, render_template, jsonify
from datetime import datetime
import requests

app = Flask(__name__)

# Function to make SQL queries
def make_query(query):
    url = 'http://localhost:8080/tienda/run-sql-query/'
    data = {'query': query}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to execute query. Status code: {response.status_code}")
            print(f"Error: {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

# Function to obtain data for the graph
def obtener_datos():
    resultados = make_query("SELECT * FROM tienda_fibonacci")
    n = []
    Fibonacci = []
    Conerror = []
    Error = []

    for fila in resultados:
        n.append(fila['id'])
        Fibonacci.append(fila['fibonaccic'])
        Conerror.append(fila['conruido'])
        Error.append(fila['error'])

    return n, Fibonacci, Conerror, Error

# Main route that loads the dashboard
@app.route('/')
def index():
    return render_template('index.html')

# Route to update chart data
@app.route('/datos_grafico', methods=['GET'])
def datos_grafico():
    n, Fibonacci, Conerror, Error = obtener_datos()

    # Prepare the data for Plotly
    data = [
        {
            'x': n,
            'y': Fibonacci,
            'mode': 'lines+markers',
            'name': 'Serie de Fibonacci (Fibonacci)'
        },
        {
            'x': n,
            'y': Conerror,
            'mode': 'lines+markers',
            'name': 'Con Error (Conerror)'
        },
        {
            'x': n,
            'y': Error,
            'mode': 'lines',
            'name': 'Error',
            'line': {'color': 'red', 'dash': 'dash'}
        }
    ]

    layout = {
        'title': f'Gráfico en tiempo real - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        'xaxis_title': 'ID (n)',
        'yaxis_title': 'Valores de la serie',
        'legend': {'x': 0, 'y': 1},
        'margin': {'l': 40, 'r': 40, 't': 40, 'b': 40}
    }

    graph_json = {
        'data': data,
        'layout': layout
    }

    return jsonify(graph_json)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
