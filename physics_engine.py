import numpy as np
import pandas as pd

class EBikePhysics:
    def __init__(self, df: pd.DataFrame, m_fahrer=70.0, m_fahrrad=10.0, raddurchmesser_zoll=27.0):
        self.df = df
        # Konstanten aus der Projektangabe
        self.m_fahrer = m_fahrer
        self.m_fahrrad = m_fahrrad
        self.m_ges = self.m_fahrer + self.m_fahrrad
        self.cw_A = 0.5625
        # Umrechnung von 27 Zoll Durchmesser in Radius (Meter)
        self.r_rad = (raddurchmesser_zoll / 2.0) * 0.0254
        self.k_m = 1.5 # Motorconstante in Nm/A
        
        # Weitere physikalische Konstanten
        self.rho = 1.225  # Luftdichte in kg/m^3
        self.g = 9.81     # Erdbeschleunigung in m/s^2

    def calculate_physics(self):
        """Berechnet alle relevanten physikalischen Größen aus den GPS-Daten."""
        
        # 1. Geschwindigkeit
        dt_safe = self.df['delta_t'].replace(0, np.nan)
        self.df['v'] = (self.df['delta_s'] / dt_safe).fillna(0)
        
        # 2. Beschleunigung
        self.df['delta_v'] = self.df['v'].diff().fillna(0)
        self.df['a'] = (self.df['delta_v'] / dt_safe).fillna(0)
        
        # 3. Steigung (aus der Höhenspalte 'ele')
        self.df['delta_h'] = self.df['ele'].diff().fillna(0)
        ds_safe = self.df['delta_s'].replace(0, np.nan)
        # Für die Steigungskraft brauchen wir sin(phi) = Gegenkathete / Hypotenuse
        sin_phi = (self.df['delta_h'] / ds_safe).fillna(0).clip(lower=-1.0, upper=1.0)
        
        # 4. Kräftebilanz aufstellen
        self.df['F_luft'] = 0.5 * self.rho * self.cw_A * (self.df['v'] ** 2)
        self.df['F_steigung'] = self.m_ges * self.g * sin_phi
        self.df['F_beschl'] = self.m_ges * self.df['a']
        
        # Gesamtkraft
        self.df['F_ges'] = self.df['F_luft'] + self.df['F_steigung'] + self.df['F_beschl']
        
        # 5. Motor-Parameter berechnen
        # Mechanische Leistung (P = F * v)
        self.df['P_mech'] = self.df['F_ges'] * self.df['v']
        
        # Drehmoment am Rad (T = F * r)
        self.df['T_motor'] = self.df['F_ges'] * self.r_rad
        
        # Motorstrom (I = T / k_m)
        # .clip(lower=0) bedeutet: Negative Ströme (Bremsen/Bergab) werden ignoriert, 
        # da der Akku standardmäßig nicht rekuperiert (außer du möchtest das später als Erweiterung hinzufügen).
        self.df['I_motor'] = (self.df['T_motor'] / self.k_m).clip(lower=0)
        
        return self.df