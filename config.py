# config.py

# GPIO pin setup
SOIL_SENSOR_PIN = 17  # For digital soil sensor
TEMP_SENSOR_PIN = 4   # DHT11 connected to GPIO4

# Alert thresholds
MOISTURE_DRY = 0      # Digital LOW = Dry
TEMP_THRESHOLD = 35   # °C threshold for temperature warning

# Time interval between sensor reads (in seconds)
SENSOR_INTERVAL = 15

DB_NAME = "database.db"
