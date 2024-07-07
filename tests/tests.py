from code import Groundhog
import unittest

class TestGroundhog(unittest.TestCase):
    def test_average(self):
        print("Testing calculation of average")
        r = [27.7, 31.0, 32.7]
        data = [27.7, 31.0, 32.7, 34.7, 35.9, 37.4, 38.2, 39.5, 40.3]
        data_1 = [27.7, 31.0, 32.7, 34.7, 35.9, 37.4, 38.2, 39.5, 40.3, 42.2]
        period = 7
        self.assertEqual(Groundhog.average_temp(period, r), 'nan')
        self.assertEqual(float(Groundhog.average_temp(period, data)), 1.33)
        self.assertEqual(float(Groundhog.average_temp(period, data_1)), 1.36)
    
    def test_stdev(self):
        print("Testing calculation of stdev")
        data = [27.7, 31.0, 32.7, 34.7, 35.9, 37.4, 38.2, 39.5, 40.3, 42.2]
        data_ = [27.7, 31.0, 32.7, 34.7, 35.9, 37.4, 38.2, 39.5, 40.3, 42.2, 41.3]
        period = 7
        self.assertEqual(float(Groundhog.stdev_function(data, period)), 2.40)
        self.assertEqual(float(Groundhog.stdev_function(data_, period)), 2.06)
    
    def test_temperature_increase(self):
        print("Testing calculation of temperature increase")
        data = [27.7, 31.0, 32.7, 34.7, 35.9, 37.4, 38.2, 39.5, 40.3, 42.2]
        period = 7
        self.assertEqual(float(Groundhog.temperature_increase(data, period)), 29)
        
    def test_detect_switch_points(self):
        print("Testing swith")
        data = [27.7, 31.0, 32.7, 34.7, 35.9, 37.4, 38.2, 39.5, 40.3, 42.2, 41.3, 40.4, 39.8, 38.7, 36.5]
        period = 7
        self.assertEqual(Groundhog.detect_switch_points(data, period), "a switch occurs")
        

if __name__ == "__main__":
    unittest.main()