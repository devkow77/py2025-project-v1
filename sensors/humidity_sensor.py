from datetime import datetime
from sensors.sensor import Sensor
import time
import numpy as np
import threading
from sensors.temperature_sensor import TemperatureSensor


class HumiditySensor(Sensor):
    def __init__(self, name="Humidity Sensor", unit="%", min_value=0, max_value=100, frequency=1):
        super().__init__(name, unit, min_value, max_value, frequency)
        self.reading_thread = None
        self.stop_thread = False
        self.temperature_dependency = True

    # funkcja ktora odczytuje wilgotnosc na podstawie temperatury
    def read_loop(self, temp_sensor = None, delay=0):
        interval = 1 / self.frequency

        while not self.stop_thread:
            now = datetime.now()
            # tymczasowa wartosc, pobieranie z temperature_sensor ostatecznie
            temperature = temp_sensor.get_last_value() if temp_sensor else 20
            # korekta wilgotnosci na podstawie temperatury
            adjustment = np.clip((30 - temperature) * 1.5, 0, 100) if self.temperature_dependency else 0

            base_value = np.random.uniform(40, 70)
            value = round(np.clip(base_value + np.random.normal(0, 5) + adjustment, 0, 100), 1)

            self.last_value = value
            self.last_read_time = now

            print(f"{now.strftime("%Y-%m-%d %H:%M:%S")} = {value}{self.unit}")
            time.sleep(interval)

    # funkcja ktora uruchamia watek z odczytywaniem wilgotnosci
    def start_reading(self, temp_sensor=None, delay=0):
        time.sleep(delay)
        if not self.active:
            raise Exception(f"Sensor {self.name} is off.")
        if self.reading_thread and self.reading_thread.is_alive():
            return
        self.stop_thread = False
        self.reading_thread = threading.Thread(target=self.read_loop, args=(temp_sensor, delay))
        self.reading_thread.start()

    # funkcja wylaczenia watku z odczytywaniem wilgotnosci
    def stop_reading(self):
        self.stop_thread = True
        if self.reading_thread:
            self.reading_thread.join()


if __name__ == '__main__':
    humiditySensor = HumiditySensor()
    humiditySensor2 = HumiditySensor(name="Humidity Sensor 2", frequency=1)
    tempSensor = TemperatureSensor()

    # wyswietlenie argumentow klas (automatyczna aktualizacja id)
    print(humiditySensor.__str__())
    print(humiditySensor2.__str__())

    # humiditySensor.start_reading() wyrzucenie Exception: Sensor Humidity Sensor is off.

    # wlaczenie czujnika wilgotnosci i temperatur, odczytywanie pomiarow , po 5s zakoncz pomiary i wylacz oba czujniki
    tempSensor.start()
    humiditySensor2.start()

    tempSensor.start_reading()
    humiditySensor2.start_reading(temp_sensor=tempSensor, delay=0.1)

    time.sleep(5)

    humiditySensor2.stop_reading()
    tempSensor.stop_reading()
    humiditySensor2.stop()
    tempSensor.stop()



