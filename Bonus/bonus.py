#!/usr/bin/env python3

from sys import argv
import statistics, math
from sys import exit, stdout

class Anomaly:
    @staticmethod
    def moving_average(data: list[float | int], period: int) -> float:
        try:
            if isinstance(data, (list, str)):
                if len(data) >= period:
                    return "{:.2f}".format(sum(data[-period:]) / period)
        except (ZeroDivisionError, IndexError, FloatingPointError):
            return None
        return None

    @staticmethod
    def standard_deviation(data: list[float | int], period: int) -> float:
        try:
            if isinstance(data, (list, str)):
                if len(data) >= period:
                    return "{:.2f}".format(math.sqrt(sum((x - statistics.mean(
                        data[-period:])) ** 2 for x in data[-period:]) / period))
        except (ZeroDivisionError, IndexError, FloatingPointError):
            return None
        return None
    
    @staticmethod
    def normalize(data: list[float | int], mov_avg: list[float | int], stdev: list[float | int]) -> float:
        try:
            upper_bb = float(mov_avg[-1]) + (2 * float(stdev[-1]))
            lower_bb = float(mov_avg[-1]) - (2 * float(stdev[-1]))
            equalize = (data[-1] - lower_bb) / (upper_bb - lower_bb)
            return equalize
        except (IndexError, ZeroDivisionError):
            return None

class GroundhogError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Groundhog:
    def __init__(self):
        self.elem = []
        self.switch = 0
        self.tab = []
        self.tab1 = []
        self.check = True
        self.curr = True

    @staticmethod
    def average_temp(period: int, data: list[float | int]) -> float:
        try:
            if isinstance(data, (list, str)):
                if len(data) > period:
                    return f'{sum(max(0, x - y) for x, y in zip(data[-period:], data[-period - 1:-1])) / period:.2f}'
        except ZeroDivisionError:
            pass
        return "nan"

    @staticmethod
    def stdev_function(data: list[float | int], period: int) -> float:
        try:
            if isinstance(data, (list, str)):
                if len(data) >= period:
                    return f'{math.sqrt(sum((x - statistics.mean(data[-period:])) ** 2 for x in data[-period:]) / period):.2f}'
        except ZeroDivisionError:
            pass
        return "nan"

    def temperature_increase(self, data: list[float | int], period: int) -> float:
        if isinstance(data, (list, str)):
            if len(data) > period:
                current_r = data[-1]
                window_r = data[-(1 + period)]
                if window_r == 0:
                    temperature_increase = ((current_r - window_r) / 1) * 100
                elif window_r < 0:
                    temperature_increase = (current_r - window_r) / -window_r * 100
                else:
                    temperature_increase = (current_r / window_r - 1) * 100
                return f'{temperature_increase:.0f}'
        return "nan"

    def detect_switch_points(self, data: list[float | int], period: int) -> str:
        try:
            if isinstance(data, (list, str)):
                if len(data) > period:
                    r_1 = self.temperature_increase(data, period)
                    self.tab.append(int(r_1))
                    self.curr = False if self.tab[-1] < 0 else True
                    if self.curr != self.check:
                        self.check = self.curr
                        self.switch += 1
                        return "a switch occurs"
        except (ZeroDivisionError, IndexError):
            return ""
        return ""

    def formating(self, data: list[float | int], period: int) -> str:
        switch_message = self.detect_switch_points(data, period)
        sdev = self.stdev_function(data, period)
        if switch_message == "":
            print(f"g={self.average_temp(period, data)}\t\tr={self.temperature_increase(data, period)}%\t\ts={sdev}")
        else:
            print(f"g={self.average_temp(period, data)}\t\tr={self.temperature_increase(data, period)}%\t\ts={sdev}\t\t{switch_message}")

    @staticmethod
    def usage():
        print("SYNOPSIS\n\t./groundhog period\nDESCRIPTION\n\tperiod the number of days defining a period")

    @staticmethod
    def check_input(data: list[float | int]) -> float:
        try:
            data = float(data)
        except ValueError:
            raise GroundhogError("Invalid Type")
        return data

    @staticmethod
    def check_arg() -> int:
        if len(argv) != 2:
            raise GroundhogError("Invalid argument")
        try:
            period = int(argv[1])
            if period < 0:
                raise GroundhogError("Invalid period")
        except ValueError:
            raise GroundhogError("must be an integer")
        return period

    @staticmethod
    def weirdest(normalised: list[float], data: list[float | int], period: int) -> str:
        normalised = list(abs(x - .5) for x in normalised)
        top_5 = sorted(normalised)[-5:]
        fdata = list(data[normalised.index(x) + period - 1] for x in top_5)
        fdata = fdata[::-1]
        
        with open("file/aberration.txt", "w") as file:
            file.write("\n".join(str(x) for x in fdata))
        
        print(f"5 weirdest values are {fdata}")

    def calculate_data(self, period: int, abbrev: Anomaly,
        mov_avg: list[float], stdev: list[float], normalised: 
        list[float]) -> tuple[float, float, float, list[float], list[float], list[float]]:
        g, r, s = self.average_temp(self.elem, period), self.temperature_increase(self.elem, period), self.stdev_function(self.elem, period)
        mov_avg.append(abbrev.moving_average(self.elem, period))
        stdev.append(abbrev.standard_deviation(self.elem, period))
        mov_avg = list(filter(None, mov_avg))
        stdev = list(filter(None, stdev))
        equalize = abbrev.normalize(self.elem, mov_avg, stdev)
        if equalize is not None:
            normalised.append(equalize)
        return g, r, s, mov_avg, stdev, normalised

    def handle_input(self, g, r, s, normalised, period):
        data = input()
        if data == "STOP":
            if all(elem == "nan" for elem in [g, r, s]):
                raise GroundhogError("Not enough data to compute the average")
            else:
                print(f"Global tendency switched {self.switch} times")
                self.weirdest(normalised, self.elem, period)
                exit(0)
        data = self.check_input(data)
        self.elem.append(data)
        self.formating(self.elem, period)

    def run(self):
        period = self.check_arg()
        abbrev = Anomaly()
        mov_avg = []
        stdev = []
        normalised = []
        while True:
            try:
                g, r, s, mov_avg, stdev, normalised = self.calculate_data(period, abbrev, mov_avg, stdev, normalised)
                self.handle_input(g, r, s, normalised, period)
            except ValueError:
                raise GroundhogError("Invalid input, please enter a valid number")

if __name__ == '__main__':
    try:
        Groundhog().run()
    except GroundhogError as e:
        stdout.write(str(type(e).__name__) + ": {}\n".format(e))
        exit(84)
