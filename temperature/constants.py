# ─── Temperature App Constants ───────────────────────
# Only used within the temperature app


class TemperatureStatus:
    """Possible temperature reading statuses"""
    OK         = 'OK'
    ALARM_HIGH = 'ALARM_HIGH'   # Temperature > MAX
    ALARM_LOW  = 'ALARM_LOW'    # Temperature < MIN


class TemperatureThreshold:
    """
    Temperature limits for alarm triggering.
    Must match firmware TEMP_MAX and TEMP_MIN values.
    """
    MAX = 8.0   # Upper limit in Celsius
    MIN = 1.0   # Lower limit in Celsius


class TemperatureConfig:
    """Configuration for temperature monitoring"""
    MEASURE_INTERVAL = 60    # seconds between readings
    MAX_RETRIES      = 3     # HTTP retry attempts


class DS18B20:
    """
    DS18B20 sensor hardware specifications.
    Physical measurement range of the sensor.
    """
    MIN_RANGE = -55.0   # Minimum measurable temperature
    MAX_RANGE = 125.0   # Maximum measurable temperature