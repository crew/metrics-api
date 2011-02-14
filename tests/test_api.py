import unittest
from crew.metrics import api


class TestAPIExceptions(unittest.TestCase):

    def test_crew_metrics_exception(self):
        api.CrewMetricsException()
        api.CrewMetricsException('Exception String')
        api.CrewMetricsException(Exception('Wrapped'))


if __name__ == '__main__':
    unittest.main()
