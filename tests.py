__author__ = 'jeffrey'

import unittest
from trains import CalMaxDistanceAssistant, CalMaxStopsAssistant, CalShortestAssistant, City, Route, Computer

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

        # Use a computer to load all cities and routes data
        computer = Computer()
        computer.add_cities([a, b, c, d, e])

        # Hire an assistant
        self.max_dis_assistant = CalMaxDistanceAssistant(computer)

        # Hire an assistant
        self.max_stops_assistant = CalMaxStopsAssistant(computer)

        # Hire an assistant
        self.shortest_route_assistant = CalShortestAssistant(computer)

    def test_get_distance(self):
        self.assertEqual(9, self.max_dis_assistant.get_distance("ABC"))
        self.assertEqual(5, self.max_dis_assistant.get_distance("AD"))
        self.assertEqual(13, self.max_dis_assistant.get_distance("ADC"))
        self.assertEqual(22, self.max_dis_assistant.get_distance("AEBCD"))
        self.assertEqual("NO SUCH ROUTE", self.max_dis_assistant.get_distance("AED"))

    def test_cal_max_stops_routes(self):
        self.max_stops_assistant.cal_routes("C", "C", 3)
        self.assertEqual(2, len(self.max_stops_assistant.computer.routes))

    def test_print_exact_stops_routes(self):
        self.assertEqual(3, len(self.max_dis_assistant.get_exact_stops_routes("A", "C", 4)))

    def test_cal_shortest_route(self):
        # The shortest route of city A to city C
        self.shortest_route_assistant.cal_routes("A", "C")
        self.assertEqual(9, self.shortest_route_assistant.get_distance(self.shortest_route_assistant.computer.routes[0]))

        self.shortest_route_assistant.cal_routes("B", "B")
        self.assertEqual(9, self.shortest_route_assistant.get_distance(self.shortest_route_assistant.computer.routes[0]))

    def test_cal_all_routes(self):
        self.max_dis_assistant.cal_routes("C", "C", 30)
        self.assertEqual(7, len(self.max_dis_assistant.computer.routes))

if __name__ == "__main__":
    unittest.main()