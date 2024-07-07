import statistics, math
from sys import argv
from .anomaly import Anomaly

class GroundhogError(Exception):
    """GroundhogError class to handle exceptions
    
    Parameters
    ----------
        Exception (class): Inherit from Exception class
        
    Raises
    ------
        GroundhogError: Raise an exception with a message
        
    Returns
    -------
        str: Return a string message
    """
    def __init__(self, message):
        """Initialize the GroundhogError class
        
        Parameters
        ----------
            message (str): The message to display
            
        Returns
        -------
            None
        """
        self.message = message
        super().__init__(self.message)

class Groundhog:
    """ Groundhog class to handle the groundhog program
    
    Parameters
    ----------
        object (class): Inherit from object class
        
    Returns
    -------
        None
    """
    def __init__(self):
        """ Initialize the Groundhog class
        
        Parameters
        ----------
            None
        
        Returns
        -------
            None
        """
        self.elem = []
        self.switch = 0
        self.tab = []
        self.tab1 = []
        self.check = True
        self.curr = True

    @staticmethod
    def average_temp(period: int, data: list[float | int]) -> float:
        """average_temp function to calculate the average temperature

        Parameters
        ----------
            period (int): The period to calculate the average
            data (list[float  |  int]): The data to calculate the average

        Logic
        -----
            1. Check if the data is a list or a string
            2. Check if the length of the data is greater than the period
            3. Calculate the average temperature (sum of the difference between the current
            element and the previous element divided by the period)
            4. Return the average temperature

        Returns
        -------
            float: Return the average temperature
        """
        try:
            if isinstance(data, (list, str)):
                if len(data) > period:
                    return f'{sum(max(0, x - y) for x, y in zip(data[-period:], data[-period - 1:-1])) / period:.2f}'
        except ZeroDivisionError:
            pass
        return "nan"

    @staticmethod
    def stdev_function(data: list[float | int], period: int) -> float:
        """stdev_function function to calculate the standard deviation

        Parameters
        ----------
            data (list[float  |  int]): The data to calculate the standard deviation
            period (int): The period to calculate the standard deviation

        Logic
        -----
            1. Check if the data is a list or a string
            2. Check if the length of the data is greater than the period
            3. Calculate the standard deviation (square root of the sum of the square of
            the difference between the data and the mean divided by the period)
            4. Return the standard deviation

        Returns
        -------
            float: Return the standard deviation
        """
        try:
            if isinstance(data, (list, str)):
                if len(data) >= period:
                    return f'{math.sqrt(sum((x - statistics.mean(data[-period:])) ** 2 for x in data[-period:]) / period):.2f}'
        except ZeroDivisionError:
            pass
        return "nan"

    def temperature_increase(self, data: list[float | int], period: int) -> float:
        """temperature_increase function to calculate the temperature increase

        Parameters
        ----------
            data (list[float  |  int]): The data to calculate the temperature increase
            period (int): The period to calculate the temperature increase
        
        Logic
        -----
            1. Check if the data is a list or a string
            2. Check if the length of the data is greater than the period
            3. Calculate the temperature increase
            4. Return the temperature increase

        Returns
        -------
            float: Return the temperature increase
        """
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
        """detect_switch_points function to detect the switch points

        Parameters
        ----------
            data (list[float  |  int]): The data to detect the switch points
            period (int): The period to detect the switch points

        Logic
        -----
            1. Check if the data is a list or a string
            2. Check if the length of the data is greater than the period
            3. Calculate the temperature increase
            4. Return a message if a switch occurs

        Returns
        -------
            str: Return a message if a switch occurs
        """
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
        """formating function to display the formatted data

        Parameters
        ----------
            data (list[float  |  int]): The data to display
            period (int): The period to display

        Logic
        -----
            1. Detect the switch points
            2. Calculate the standard deviation
            3. Display the formatted metrics

        Returns
        -------
            str: Return the formatted metrics
        """
        switch_message = self.detect_switch_points(data, period)
        sdev = self.stdev_function(data, period)
        if switch_message == "":
            print(f"g={self.average_temp(period, data)}\t\tr={self.temperature_increase(data, period)}%\t\ts={sdev}")
        else:
            print(f"g={self.average_temp(period, data)}\t\tr={self.temperature_increase(data, period)}%\t\ts={sdev}\t\t{switch_message}")

    @staticmethod
    def usage():
        """
        usage function to display the usage of the program
        """
        print("SYNOPSIS\n\t./groundhog period\nDESCRIPTION\n\tperiod the number of days defining a period")

    @staticmethod
    def check_input(data: list[float | int]) -> float:
        """ check_input function to check the input data

        Parameters
        ----------
            data (list[float  |  int]): The data to check

        Raises
        ------
            GroundhogError: Raise an exception if the data is invalid

        Returns
        -------
            float: Return the data
        """
        try:
            data = float(data)
        except ValueError:
            raise GroundhogError("Invalid Type")
        return data

    @staticmethod
    def check_arg() -> int:
        """ check_arg function to check the argument

        Raises
        ------
            GroundhogError: Raise an exception if the argument is invalid
            GroundhogError: Raise an exception if the period is invalid
            GroundhogError: Raise an exception if the period type is invalid

        Returns
        -------
            int: Return the period
        """
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
        """ weirdest function to display the weirdest values

        Parameters
        ----------
            normalised (list[float]): list of normalised data
            data (list[float  |  int]): The input data
            period (int): The period of the data

        Logic
        -----
            1. Normalise the data
            2. Calculate the weirdest values
            3. Display the weirdest values
            4. How are the weirdest values calculated? 
            The weirdest values are calculated by sorting
            the normalised data in ascending order and then
            selecting the last 5 values based on their index in the list of inputs.

        Returns
        -------
            str: Return the weirdest values
        """
        normalised = list(abs(x - .5) for x in normalised)
        top_5 = sorted(normalised)[-5:]
        fdata = list(data[normalised.index(x) + period - 1] for x in top_5)
        if fdata == []:
            fdata = data[0:5]
        else:
            fdata = fdata[::-1]
        print(f"5 weirdest values are {fdata}")

    def calculate_data(self, period: int, abbrev: Anomaly,
        mov_avg: list[float], stdev: list[float], normalised: 
        list[float]) -> tuple[float, float, float, list[float], list[float], list[float]]:
        """ calculate_data function to calculate the data

        Parameters
        ----------
            period (int): The period of the data
            abbrev (Anomaly): The Anomaly class
            mov_avg (list[float]): The moving average
            stdev (list[float]): The standard deviation
            normalised (list[float]): The normalised data

        Returns
        -------
            tuple[float, float, float, list[float], list[float], list[float]]: Return the calculated data
        """
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
        """ Run function to execute the groundhog program.

        Raises
        ------
            GroundhogError: Raise an exception if the data is invalid.
            GroundhogError: Raise an exception if the average is not enough.
        """
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