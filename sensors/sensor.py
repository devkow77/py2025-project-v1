import numpy as np
from datetime import datetime

class Sensor:
    # automatyczne id
    _id_counter = 1

    def __init__(self, name, unit, min_value, max_value, frequency=1, active=False, last_value=None, start_time = None, last_read_time=None):
        self.sensor_id = Sensor._id_counter
        Sensor._id_counter += 1

        if frequency > 10:
            raise Exception("Maximum frequency is 10Hz!")

        self.name = name
        self.unit = unit
        self.min_value = min_value
        self.max_value = max_value
        self.frequency = frequency
        self.active = active
        self.last_value = last_value
        self.start_time = start_time
        self.last_read_time = last_read_time

    # funkcja wyswietlajaca pomiar temperatury
    def read_value(self):
        if not self.active:
            raise Exception(f"Sensor {self.name} is off.")

        now = datetime.now()
        value = round(np.random.uniform(self.min_value, self.max_value), 1)

        self.last_value = value
        self.last_read_time = now

        print(f"{now.strftime("%Y-%m-%d %H:%M:%S")} = {value}{self.unit}")

    # funkcja kalibrujaca wynik
    def calibrate(self, calibration_factor):
        if self.last_value is None:
            self.read_value()

        self.last_value *= calibration_factor
        return self.last_value

    # funkcja zwracajaca ostatni pomiar tempetury
    def get_last_value(self):
        if self.last_value is None:
            return self.read_value()

        return f"{self.last_value}{self.unit}"

    # funkcja uruchamiajaca sensor
    def start(self):
        self.start_time = datetime.now()
        self.active = True

    # funkcja wylaczajaca sensor
    def stop(self):
        self.active = False

    # funkcja zwracajaca opis sensora
    def __str__(self):
        return f"Sensor(id={self.sensor_id}, name={self.name}, unit={self.unit}, active={self.active})"




