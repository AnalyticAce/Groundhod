import statistics, math
from sys import argv

class Anomaly:
    """Anomaly class to handle the anomaly program
    
    Parameters
    ----------
        object (class): Inherit from object class
    
    Methods
    -------
        moving_average(data: list[float | int], period: int) -> float
        standard_deviation(data: list[float | int], period: int) -> float
        normalize(data: list[float | int], mov_avg: list[float | int], stdev: list[float | int]) -> float

    Returns
    -------
        None
    """
    @staticmethod
    def moving_average(data: list[float | int], period: int) -> float:
        """moving_average function to calculate the moving average

        Parameters
        ----------
            data (list[float  |  int]): The data to calculate the moving average
            period (int): The period to calculate the moving average

        Logic
        -----
            1. Check if the data is a list or a string
            2. Check if the length of the data is greater than the period
            3. Calculate the moving average (sum of the last n elements / n)
            4. Return the moving average

        Returns
        -------
            float: Return the moving average
        """
        try:
            if isinstance(data, (list, str)):
                if len(data) >= period:
                    return "{:.2f}".format(sum(data[-period:]) / period)
        except (ZeroDivisionError, IndexError, FloatingPointError):
            return None
        return None

    @staticmethod
    def standard_deviation(data: list[float | int], period: int) -> float:
        """standard_deviation function to calculate the standard deviation

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
                    return "{:.2f}".format(math.sqrt(sum((x - statistics.mean(
                        data[-period:])) ** 2 for x in data[-period:]) / period))
        except (ZeroDivisionError, IndexError, FloatingPointError):
            return None
        return None
    
    @staticmethod
    def normalize(data: list[float | int], mov_avg: list[float | int], stdev: list[float | int]) -> float:
        """ normalize function to normalize the data

        Parameters
        ----------
            data (list[float  |  int]): The data to normalize
            mov_avg (list[float  |  int]): The moving average
            stdev (list[float  |  int]): The standard deviation

        Logic
        -----
            1. Calculate the upper bollinger band
            2. Calculate the lower bollinger band
            3. Calculate the equalize
                (data - lower bollinger band) / (upper bollinger band - lower bollinger band)
            4. Return the normalized data
            5. Normalizing the data is important because it brings all the data to a similar scale.
            6. This is important because the data can have different scales and this can affect the model.

        Returns
        -------
            float: Return the normalized data
        """
        try:
            upper_bb = float(mov_avg[-1]) + (2 * float(stdev[-1]))
            lower_bb = float(mov_avg[-1]) - (2 * float(stdev[-1]))
            equalize = (data[-1] - lower_bb) / (upper_bb - lower_bb)
            return equalize
        except (IndexError, ZeroDivisionError):
            return None
