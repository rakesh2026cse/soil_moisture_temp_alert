from flask import Flask, render_template
import sqlite3
from config import DB_NAME

app = Flask(__name__)

@app.route("/")
def home():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Fetch latest reading
    c.execute("SELECT temperature, moisture_status, timestamp FROM sensor_data ORDER BY id DESC LIMIT 1")
    latest = c.fetchone()

    # Fetch last 5 alerts
    c.execute("SELECT message, timestamp FROM alerts ORDER BY id DESC LIMIT 5")
    alerts = c.fetchall()

    conn.close()
    return render_template("index.html", latest=latest, alerts=alerts)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")  # Accessible from other devices on network
