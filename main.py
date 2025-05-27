from logger.logger import Logger
from sensors.humidity_sensor import HumiditySensor
from sensors.light_sensor import LightSensor
from sensors.pressure_sensor import PressureSensor
from sensors.temperature_sensor import TemperatureSensor
import time

if __name__ == "__main__":
    # Jeden wspólny logger
    logger = Logger("config.json")
    logger.start()  # startujemy raz na początku

    # Sensory
    temperatureSensor = TemperatureSensor(logger=logger)
    humiditySensor = HumiditySensor(logger=logger)
    pressureSensor = PressureSensor(logger=logger)
    lightSensor = LightSensor(logger=logger)

    # Ustawienie zależności
    humiditySensor.set_temperature_sensor(temperatureSensor)
    pressureSensor.set_temperature_sensor(temperatureSensor)
    pressureSensor.set_humidity_sensor(humiditySensor)

    sensors = [temperatureSensor, humiditySensor, pressureSensor, lightSensor]

    # Start sensorów
    for s in sensors:
        s.start()
    for s in sensors:
        s.start_reading()
        time.sleep(1)

    # Czekamy np. 20s
    time.sleep(20)

    # Zatrzymujemy odczyty i zamykamy loggera
    for s in sensors:
        s.stop_reading()
        s.stop()

    logger.stop()  # zamykamy logger na koniec


