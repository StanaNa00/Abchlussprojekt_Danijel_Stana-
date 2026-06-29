from battery_base import BatteryBase
from lifepo4_battery import LiFePO4BatteryPack
from motor_base import Motor

from plotting_utils import plot_current_profile, plot_voltage_profile, plot_voltage_and_current_profile




class BatterySimulator:
    """Simple simulator for a battery pack. The simulator applies a current profile to the battery pack and records the voltage profile."""

    def __init__(self, battery: BatteryBase, motor: Motor) -> None:
        self.battery = battery
        self.motor = motor
        self.voltage_profile = []

    def simulate(self, get_current_draw: list[float], duration_profile: list[float]) -> None:
        self.voltage_profile = []
        self.voltage_profile.append(self.battery.voltage())

        for i, t in zip(get_current_draw, duration_profile):
            self.battery.apply_current(current=i, duration=t)
            self.voltage_profile.append(self.battery.voltage(current=i))



if __name__ == "__main__":
    load_current = [3.0, 11.0, 4.0, -1.5, 1.0]
    load_durations = [300.0, 240.0, 90.0, 150.0, 120.0]
    power_profile_w = [115, 420, 150, -60, 38, 300, 0.0, 435, -75, 111]
    duration_s = [300.0, 240.0, 90.0, 150.0, 120.0, 300.0, 60.0, 30.0, 120.0, 180.0]

    plot_current_profile(current_profile=power_profile_w, duration_profile=duration_s)

    params = {"capacity_nom_Ah": 10.0, "initial_soc": 0.7, "Vmin": 32.0, "Vmax": 42.0}
    battery = LiFePO4BatteryPack(**params)
    motor = Motor()
    sim = BatterySimulator(battery, motor)
    sim.simulate(power_profile_w, duration_s)
    print(battery)

    plot_voltage_profile(voltage_profile=sim.voltage_profile, duration_profile=duration_s)
    plot_voltage_and_current_profile(sim.voltage_profile, power_profile_w, duration_s)

    input("Press Enter to continue...")
