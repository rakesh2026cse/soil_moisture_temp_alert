import Adafruit_DHT
import RPi.GPIO as GPIO
import sqlite3
import time
from datetime import datetime
from config import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(SOIL_SENSOR_PIN, GPIO.IN)

DHT_SENSOR = Adafruit_DHT.DHT11

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            moisture_status TEXT,
            timestamp TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def read_sensors():
    moisture = GPIO.input(SOIL_SENSOR_PIN)  # 0 = dry, 1 = wet
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, TEMP_SENSOR_PIN)
    return temperature, "Dry" if moisture == 0 else "Wet"

def insert_data(temp, moisture_status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("INSERT INTO sensor_data (temperature, moisture_status, timestamp) VALUES (?, ?, ?)",
              (temp, moisture_status, timestamp))

    # Trigger alerts
    if moisture_status == "Dry":
        msg = f"🌱 Soil is dry. Irrigation needed at {timestamp}"
        c.execute("INSERT INTO alerts (message, timestamp) VALUES (?, ?)", (msg, timestamp))
    elif temp is not None and temp > TEMP_THRESHOLD:
        msg = f"🔥 High temperature alert ({temp:.1f}°C) at {timestamp}"
        c.execute("INSERT INTO alerts (message, timestamp) VALUES (?, ?)", (msg, timestamp))

    conn.commit()
    conn.close()

def run():
    init_db()
    while True:
        temp, moisture = read_sensors()
        if temp is not None:
            print(f"[{datetime.now()}] Temp: {temp:.1f}°C | Soil: {moisture}")
            insert_data(temp, moisture)
        else:
            print("Temperature sensor read failed.")
        time.sleep(SENSOR_INTERVAL)

if __name__ == "__main__":
    run()
