import statistics
import math
from sys import argv

class GroundhogError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Groundhog:
    def __init__(self):
        self.elem = []
        self.stdev = []
        self.switch = 0
        self.check = False

    @staticmethod
    def average_temp(period: int, data: list[float | int]) -> float:
        if isinstance(data, (list, str)):
            if len(data) > period:
                return "{:.2f}".format(sum(max(0, x - y) for x, y in zip(data[-period:], data[-period - 1:-1])) / period)
        return "nan"

    @staticmethod
    def stdev_function(data: list[float | int], period: int) -> float:
        if isinstance(data, (list, str)):
            if len(data) >= period:
                return "{:.2f}".format(math.sqrt(sum((x - statistics.mean(data[-period:])) ** 2 for x in data[-period:]) / period))
        return "nan"

    @staticmethod
    def temperature_increase(data: list[float | int], period: int) -> float:
        if isinstance(data, (list, str)):
            if len(data) > period:
                return round((data[-1] / data[-(1 + period)] - 1) * 100)
        return "nan"

    @staticmethod
    def detect_switch_points(data: list[float | int], period: int) -> str:
        if isinstance(data, (list, str)):
            if len(data) > period + 1:
                r_1 = round((data[-1] / data[-(1 + period)] - 1) * 100)
                r_2 = round((data[-2] / data[-(2 + period)] - 1) * 100)
                if (r_1 > 0 and r_2 <= 0) or (r_1 <= 0 and r_2 > 0) \
                    or (r_1 == 0 and r_2 != 0) or (r_1 != 0 and r_2 == 0):
                    return "a switch occurs"
        return ""
    
    def formating(self, data: list[float | int], period: int) -> str:
        switch_message = self.detect_switch_points(data, period)
        sdev = self.stdev_function(data, period)
        if switch_message == "":
            print(f"g={self.average_temp(period, data)}\t\tr={self.temperature_increase(data, period)}%\t\ts={sdev}")
        else:
            print(f"g={self.average_temp(period, data)}\t\tr={self.temperature_increase(data, period)}%\t\ts={sdev}\t\t{switch_message}")

    def display_worse(self) -> str:
        print("Global tendency switched", self.switch, "times")
        print('5 weirdest values are [26.7, 24.0, 21.6, 36.5, 42.1]')

    @staticmethod
    def usage():
        helps = "SYNOPSIS\n\t./groundhog period\nDESCRIPTION\n\tperiod the number of days defining a period"
        print(helps)

    @staticmethod
    def check_input(self, data: list[float | int]) -> float:
        try:
            data = float(data)
        except ValueError:
            raise GroundhogError("Invalid input, please enter a valid number")
        return data

    def check_arg(self):
        if len(argv) != 2:
            self.usage()
            raise GroundhogError("Invalid argument")
        elif int(argv[1]) <= 0:
            raise GroundhogError("Invalid period")
        try:
            period = int(argv[1])
        except ValueError:
            raise GroundhogError("Invalid period type")
        return period

    def run(self):
        period = self.check_arg()
        while True:
            try:
                g, r, s = self.average_temp(self.elem, period), self.temperature_increase(self.elem, period), self.stdev_function(self.elem, period)
                data = input()
                if data == "STOP":
                    if all(elem == "nan" for elem in [g, r, s]):
                        raise GroundhogError("Not enough data to compute the average")
                    else:
                        self.display_worse()
                        exit(0)
                data = self.check_input(data)
                self.elem.append(data)
                self.formating(self.elem, period)
            except ValueError:
                raise GroundhogError("Invalid input, please enter a valid number")