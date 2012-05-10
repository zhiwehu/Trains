__author__ = 'jeffrey'

import unittest
from trains import Assistant, City, Route

class TestAssistant(unittest.TestCase):
    def setUp(self):
        # Init cities
        a = City("A")
        b = City("B")
        c = City("C")
        d = City("D")
        e = City("E")

        # Init routes
        Route(a, b, 5)
        Route(b, c, 4)
        Route(c, d, 8)
        Route(d, c, 8)
        Route(d, e, 6)
        Route(a, d, 5)
        Route(c, e, 2)
        Route(e, b, 3)
        Route(a, e, 7)

        # Hire an assistant
        self.assistant = Assistant()

        # The assistant need to study cities
        self.assistant.add_cities([a, b, c, d, e])

    def test_get_distance(self):
        self.assertEqual(9, self.assistant.get_distance("A-B-C"))
        self.assertEqual(5, self.assistant.get_distance("A-D"))
        self.assertEqual(13, self.assistant.get_distance("A-D-C"))
        self.assertEqual(22, self.assistant.get_distance("A-E-B-C-D"))
        self.assertEqual("NO SUCH ROUTE", self.assistant.get_distance("A-E-D"))

    def test_cal_max_stops_routes(self):
        self.assistant.routes = []
        self.assertEqual(0, len(self.assistant.routes))
        self.assistant.cal_max_stops_routes("C", "C", 3)
        self.assertEqual(2, len(self.assistant.routes))

    def test_print_exact_stops_routes(self):
        self.assertEqual(3, len(self.assistant.get_exact_stops_routes("A", "C", 4)))

    def test_cal_shortest_route(self):
        # The shortest route of city A to city C
        self.assistant.reset_shortest_route()
        self.assertEqual(-1, self.assistant.shortest_distance)
        self.assertEqual("", self.assistant.shortest_route)
        self.assistant.cal_shortest_route("A", "C")
        self.assertEqual(9, self.assistant.shortest_distance)

        # The shortest route of city A to city C
        self.assistant.reset_shortest_route()
        self.assertEqual(-1, self.assistant.shortest_distance)
        self.assertEqual("", self.assistant.shortest_route)
        self.assistant.cal_shortest_route("B", "B")
        self.assertEqual(9, self.assistant.shortest_distance)

    def test_cal_all_routes(self):
        self.assistant.routes = []
        self.assertEqual(0, len(self.assistant.routes))
        self.assistant.cal_all_routes("C", "C")
        self.assertEqual(7, len(self.assistant.routes))

if __name__ == "__main__":
    unittest.main()