from flask import Flask, jsonify, send_file, render_template, send_from_directory
from flask_cors import CORS
import mysql.connector
import matplotlib.pyplot as plt
import io

app = Flask(__name__, static_folder="Front End Webpage", template_folder="Front End Webpage")  # Ensure 'Front End Webpage' folder exists
CORS(app)  # Allow frontend to fetch API data

# Database connection
mycon = mysql.connector.connect(host="localhost", user="root", passwd="My!nst@_1136", database="emissionseye")
sqr = mycon.cursor()

# Homepage route (serves frontend homepage)
@app.route('/')
def home():
    return render_template('index.html')  # Ensure index.html is in the 'templates' folder

# Route for serving static files (CSS, JS, Images)
@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory("Front End Webpage", filename)

# API Endpoint to Fetch History Data
@app.route('/history', methods=['GET'])
def get_history():
    sqr.execute("SELECT Date_Time, Total FROM history")
    data = sqr.fetchall()

    # Convert fetched data into a JSON-friendly format
    history_data = [{"date": row[0], "emission": float(row[1])} for row in data]
    return jsonify(history_data)

# API Endpoint to Generate and Return Graph
@app.route('/history-graph', methods=['GET'])
def get_history_graph():
    sqr.execute("SELECT Date_Time, Total FROM history")
    data = sqr.fetchall()

    if not data:
        return "No Data Available", 404

    dates = [row[0] for row in data]
    emissions = [float(row[1]) for row in data]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, emissions, marker='o', linestyle='-', color='b', label="Emissions Over Time")
    plt.xlabel("Date")
    plt.ylabel("Carbon Emission (kg)")
    plt.title("Carbon Emissions History")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
