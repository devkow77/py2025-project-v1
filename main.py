from sensors.humidity_sensor import HumiditySensor
from sensors.light_sensor import LightSensor
from sensors.pressure_sensor import PressureSensor
from sensors.temperature_sensor import TemperatureSensor
import time

if __name__ == "__main__":
    temperatureSensor = TemperatureSensor()
    humiditySensor = HumiditySensor()
    pressureSensor = PressureSensor()
    lightSensor = LightSensor()

    humiditySensor.set_temperature_sensor(temperatureSensor)
    pressureSensor.set_temperature_sensor(temperatureSensor)
    pressureSensor.set_humidity_sensor(humiditySensor)

    sensors = [temperatureSensor, humiditySensor, pressureSensor, lightSensor]

    # wlaczenie sensorow
    for sensor in sensors:
        sensor.start()
    # uruchomienie sensorow
    for sensor in sensors:
        sensor.start_reading()
        time.sleep(1)

