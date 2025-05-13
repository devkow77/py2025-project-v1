from datetime import datetime
from sensors.sensor import Sensor
import time
import numpy as np
import threading
from sensors.humidity_sensor import HumiditySensor
from sensors.temperature_sensor import TemperatureSensor


class PressureSensor(Sensor):
    def __init__(self, name="Pressure Sensor", unit="hPa", min_value=950, max_value=1050, frequency=1):
        super().__init__(name, unit, min_value, max_value, frequency)
        self.reading_thread = None
        self.stop_thread = False
        self.temperature_dependency = True
        self.humidity_dependency = True
        self.temperature_sensor = None
        self.humidity_sensor = None

    # Funkcja do odczytu ciśnienia na podstawie temperatury i wilgotności
    def read_loop(self, temp_sensor=None, humidity_sensor=None, delay=0):
        interval = 1 / self.frequency

        while not self.stop_thread:
            now = datetime.now()

            # ustaw temperature z czujnika, domyslnie 20
            temperature = temp_sensor.get_last_value() if temp_sensor else 20

            # ustaw wilgotnosc z czujnika, domyslnie 1000
            humidity = humidity_sensor.get_last_value() if humidity_sensor else 1000

            # Korekta ciśnienia na podstawie temperatury i wilgotności
            adjustment = (temperature - 20) * 0.3 + (humidity - 50) * 0.2
            base_value = np.random.uniform(self.min_value, self.max_value)
            value = round(np.clip(base_value + adjustment, self.min_value, self.max_value), 1)

            self.last_value = value
            self.last_read_time = now

            print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} = {self.last_value}{self.unit}")
            time.sleep(interval)

    # Funkcja uruchamiająca wątek z odczytem ciśnienia
    def start_reading(self, temp_sensor=None, humidity_sensor=None, delay=0):
        time.sleep(delay)
        if not self.active:
            raise Exception(f"Sensor {self.name} is off.")
        if self.reading_thread and self.reading_thread.is_alive():
            return
        self.stop_thread = False
        self.reading_thread = threading.Thread(target=self.read_loop, args=(temp_sensor, humidity_sensor, delay))
        self.reading_thread.start()

    # Funkcja wyłączająca wątek z odczytem ciśnienia
    def stop_reading(self):
        self.stop_thread = True
        if self.reading_thread:
            self.reading_thread.join()

    # Metoda umożliwiająca ustawienie czujników temperatury i wilgotności
    def set_temperature_sensor(self, temp_sensor):
        self.temperature_sensor = temp_sensor

    def set_humidity_sensor(self, humidity_sensor):
        self.humidity_sensor = humidity_sensor


if __name__ == '__main__':
    pressureSensor = PressureSensor(frequency=0.5)
    humiditySensor = HumiditySensor(frequency=0.5)
    tempSensor = TemperatureSensor(frequency=0.5)

    # Ustawiamy czujniki temperatury i wilgotności w PressureSensor
    pressureSensor.set_temperature_sensor(tempSensor)
    pressureSensor.set_humidity_sensor(humiditySensor)

    # Włączenie czujników i rozpoczęcie odczytu
    tempSensor.start()
    humiditySensor.start()
    pressureSensor.start()

    tempSensor.start_reading()
    humiditySensor.start_reading(temp_sensor=tempSensor, delay=0.1)
    pressureSensor.start_reading(temp_sensor=tempSensor, humidity_sensor=humiditySensor, delay=0.2)

    time.sleep(10)

    # Zakończenie odczytów
    pressureSensor.stop_reading()
    humiditySensor.stop_reading()
    tempSensor.stop_reading()

    pressureSensor.stop()
    humiditySensor.stop()
    tempSensor.stop()

