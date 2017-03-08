
class Car:

    def __init__(self, model, battery, consumption):
        self.model = model

        # Capacity in kWh of the battery
        self.battery = battery

        # Consumption in kWh per 100 km
        self.consumption = consumption

    def math_distance_max(self, percent):
        battery = (self.battery / 100) * (100 - percent)
        return (battery / self.consumption) * 100
