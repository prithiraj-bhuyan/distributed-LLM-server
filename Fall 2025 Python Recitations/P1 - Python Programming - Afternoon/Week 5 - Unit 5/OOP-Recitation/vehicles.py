# Base Class (basic blueprint)
class Vehicle:
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed  # in mph

    def move(self):
        print(f"{self.name} moves at {self.speed} mph.")

# Inherit the base class to create 2 different vehicle classes
class Tank(Vehicle):
    def __init__(self, name, speed, armor_thickness):
        super().__init__(name, speed)
        self.armor_thickness = armor_thickness

    def fire(self):
        print(f"{self.name} fires its cannon! 💥")

class Humvee(Vehicle):
    def __init__(self, name, speed, troop_capacity):
        super().__init__(name, speed)
        self.troop_capacity = troop_capacity

    def transport_troops(self):
        print(f"{self.name} transports {self.troop_capacity} soldiers.")

# Composition Example
# Create classes of features you want to use inside of a Car (we wont be inheriting them since Radio is not a Vehicle, it is just a feature inside a vehicle)
class Radio:
    def __init__(self, range_km):
        self.range_km = range_km

    def communicate(self):
        print(f"Communicating with HQ within {self.range_km} km.")

class Weapon:
    def __init__(self, weapon_type):
        self.weapon_type = weapon_type

    def use(self):
        print(f"Firing {self.weapon_type}!")

# Compose (fit-in) the features into a Vehicle
class ArmoredCar(Vehicle):
    def __init__(self, name, speed, weapon, radio):
        super().__init__(name, speed)
        self.weapon = weapon      # composition
        self.radio = radio        # composition

    def attack(self):
        self.weapon.use()

    def call_support(self):
        self.radio.communicate()


# Use the stuff we created
if __name__ == "__main__":
    tank = Tank("M1 Abrams", 45, "120mm armor")
    humvee = Humvee("Humvee", 60, 4)
    armored_car = ArmoredCar("LAV-25", 55, Weapon("25mm autocannon"), Radio(50))

    tank.move()
    tank.fire()

    humvee.move()
    humvee.transport_troops()

    armored_car.move()
    armored_car.attack()
    armored_car.call_support()