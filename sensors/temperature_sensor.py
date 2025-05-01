from datetime import datetime
from sensors.sensor import Sensor
import time
import numpy as np
import threading

class TemperatureSensor(Sensor):
    def __init__(self, name="Temperature Sensor", unit="°C", min_value=-15, max_value=35, frequency=1):
        super().__init__(name, unit, min_value, max_value, frequency)
        self.reading_thread = None
        self.stop_thread = None

        # zakres temperatur na podstawie pory roku i pory dnia
        self.temperature_ranges = {
            'winter': {
                'night': (-15, -5),
                'day': (-5, 2),
                'evening': (-10, -3)
            },
            'spring': {
                'night': (0, 5),
                'day': (10, 18),
                'evening': (6, 12)
            },
            'summer': {
                'night': (15, 20),
                'day': (25, 35),
                'evening': (18, 25)
            },
            'autumn': {
                'night': (5, 10),
                'day': (10, 18),
                'evening': (7, 12)
            }
        }

    # funkcja zwracajaca pore roku na podstawie arg aktualnego miesiaca
    def get_season(self, month):
        if month in [12,1,2]:
            return 'winter'
        elif month in [3,4,5]:
            return 'spring'
        elif month in [6,7,8]:
            return 'summer'
        else:
            return 'autumn'

    # funkcja zwracajaca pore dnia na podstawie arg aktulnej godziny
    def get_time_period(self, hour):
        if 0 <= hour < 8:
            return 'night'
        elif 8 <= hour < 16:
            return 'day'
        else:
            return 'evening'

    # funkcja ktora odczytuje temperature we wskazanej czestotliwosci
    def read_loop(self):
        interval = 1 / self.frequency
        while not self.stop_tread:
            now = datetime.now()
            season = self.get_season(now.month)
            period = self.get_time_period(now.hour)

            temp_min, temp_max = self.temperature_ranges[season][period]
            value = round(np.random.uniform(temp_min, temp_max), 1)
            self.last_value = value
            self.last_read_time = now

            print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} = {value}{self.unit}")
            time.sleep(interval)

    # funkcja ktora uruchamia watek z odczytywaniem temperatur
    def start_reading(self):
        # sprawdz czy sensor nie jest wlaczony
        if not self.active:
            raise Exception(f"Sensor {self.name} is off.")
        # sprawdz czy watek juz istnieje oraz jest aktywny a jezeli tak to nie uruchamiaj po raz drugi.
        if self.reading_thread and self.reading_thread.is_alive():
            return
        self.stop_tread = False
        self.reading_thread = threading.Thread(target=self.read_loop)
        self.reading_thread.start()

    # funkcja wylaczenia watku z odczytywaniem temperatury
    def stop_reading(self):
        self.stop_tread = True
        # upewnia zeby zablokowac wykonanie dalszego kodu w glownym watku dopoki wskazany watek sie nie zakonczy.
        if self.reading_thread:
            self.reading_thread.join()



