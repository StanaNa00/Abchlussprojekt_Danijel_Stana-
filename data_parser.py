import pandas as pd
import numpy as np

class GPSDataParser:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = pd.DataFrame()

    def load_data(self):
        # Lese die CSV Datei ein. Achte auf das Trennzeichen ';'
        self.data = pd.read_csv(self.filepath, sep=';')
        
        # Konvertiere die Zeit-Spalte in DateTime-Objekte (falls sie als String vorliegen)
        self.data['time'] = pd.to_datetime(self.data['time'])
        
        # Berechne Zeitdifferenz in Sekunden
        self.data['delta_t'] = self.data['time'].diff().dt.total_seconds().fillna(0)
        
        self._calculate_distances()
        return self.data

    def _calculate_distances(self):
        """Berechnet die Distanz zwischen zwei GPS-Punkten mit der Haversine-Formel."""
        # Radius der Erde in Metern
        R = 6371000 
        
        # Umwandlung von Grad in Radiant
        lat1 = np.radians(self.data['lat'].shift(1))
        lat2 = np.radians(self.data['lat'])
        lon1 = np.radians(self.data['lon'].shift(1))
        lon2 = np.radians(self.data['lon'])
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        # Haversine Formel
        a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
        c = 2 * np.arcsin(np.sqrt(a))
        
        # Distanz in die Spalte eintragen (erster Wert ist 0)
        self.data['delta_s'] = (R * c).fillna(0)