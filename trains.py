__author__ = "Jeffrey"

class City:
    def __init__(self, city_name):
        self.city_name = city_name
        # Route list which start from this city
        self.start_routes = []

    def add_start_route(self, route):
        self.start_routes.append(route)

    def get_distance(self, end_city):
        distance = 0
        for route in self.start_routes:
            if route.end_city == end_city:
                distance = route.distance
                break
        if distance:
            return distance
        else:
            raise Exception("NO SUCH ROUTE")

class Route:
    def __init__(self, start_city, end_city, distance):
        self.start_city = start_city
        self.end_city = end_city
        self.distance = distance
        start_city.add_start_route(self)

class Computer:
    def __init__(self):
        self.cities = {}
        self.routes = []

    def add_city(self, city):
        self.cities[city.city_name] = city

    def add_cities(self, city_list):
        for city in city_list:
            self.add_city(city)

    def get_city(self, city_name):
        return self.cities[city_name]

    def get_distance(self, route):
        """
        Get distance of the route.

        @param route: route string such as 'ABC'
        """
        total_distance = 0
        try:
            if route:
                city_list = list(route)
                start_city = self.get_city(city_list.pop(0))
                while city_list:
                    end_city = self.get_city(city_list.pop(0))
                    distance = start_city.get_distance(end_city)
                    total_distance = total_distance + distance
                    start_city = end_city
        except Exception as e:
            return e.message
        return total_distance

class Assistant:
    def __init__(self, computer):
        self.computer = computer

    def get_distance(self, route):
        return self.computer.get_distance(route)

    def get_exact_stops_routes(self, start_city_name, end_city_name, extra_stops):
        """
        Return the route list from start_city to end_city with extra stops.

        @param start_city_name: start city name
        @param end_city_name: end city name
        @param extra_stops: extra stops
        """
        last_route_paths = [start_city_name, ]
        for stop in range(extra_stops):
            route_paths = []
            for route_path in last_route_paths:
                city = self.computer.get_city(route_path[-1])
                for route in city.start_routes:
                    new_route_path = route_path + route.end_city.city_name
                    route_paths.append(new_route_path)
                # Please care about this need to copy|clone a list, can not assignment
            last_route_paths = route_paths[:]

        routes = []
        for route in last_route_paths:
            if route.endswith(end_city_name):
                routes.append(route)
        return routes

    def check_value(self, route, value):
        return False

    def handle_route(self, route):
        self.computer.routes.append(route)

    def cal_routes(self, start_city_name, end_city_name, value=0):
        """
        Calculate all routes from start city to end city which max value
        The logic to check the max_value is in sub class
        The result save to self.computer.routes.

        @param start_city_name: start city name
        @param end_city_name: end city name
        """
        self.computer.routes = []
        self.cal_routes_i(start_city_name, end_city_name, value)

    def cal_routes_i(self, start_city_name, end_city_name, value):
        if self.check_value(start_city_name, value):
            return

        if len(start_city_name) > 1 and start_city_name.endswith(end_city_name):
            self.handle_route(start_city_name)

        end_city = self.computer.get_city(start_city_name[-1])
        for route in end_city.start_routes:
            self.cal_routes_i(start_city_name + route.end_city.city_name, end_city_name, value)

class CalMaxDistanceAssistant(Assistant):
    def __init__(self, computer):
        Assistant.__init__(self, computer)

    def check_value(self, route, value):
        """
        Check if the distance of route less than max distance of value
        """
        return self.get_distance(route) >= value

class CalMaxStopsAssistant(Assistant):
    def __init__(self, computer):
        Assistant.__init__(self, computer)

    def check_value(self, route, value):
        """
        Check if the route has more than max stop of value
        """
        return (len(route) - 1) > value

class CalShortestAssistant(Assistant):
    def __init__(self, computer):
        Assistant.__init__(self, computer)

    def check_value(self, route, value):
        return route[1:].count(route[-1]) > 1

    def handle_route(self, route):
        if self.computer.routes:
            old_route = self.computer.routes[0]
            if self.get_distance(route) < self.get_distance(old_route):
                self.computer.routes[0] = route
        else:
            self.computer.routes.append(route)

if __name__ == "__main__":
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
    assistant = CalMaxStopsAssistant(computer)

    # Please tell me the distance of route A-B-C
    print assistant.get_distance("ABC")

    # How much distance of route A-D ?
    print assistant.get_distance("AD")

    # And how much of A-D-C
    print assistant.get_distance("ADC")

    # And A-E-B-C-D ?
    print assistant.get_distance("AEBCD")

    # A-E-D ?
    print assistant.get_distance("AED")

    # The # of trips between city C and C with a max stops 3
    assistant.cal_routes("C", "C", 3)
    print len(assistant.computer.routes)

    # Print how many routes between city A to C and extra stops if 4
    routes = assistant.get_exact_stops_routes("A", "C", 4)
    print len(routes)

    # Hire another assistant for calculate shortest distance
    assistant = CalShortestAssistant(computer)
    # The shortest route of city A to city C
    assistant.cal_routes("A", "C")
    print assistant.get_distance(computer.routes[0])
    # The shortest route of city B to city B
    assistant.cal_routes("B", "B")
    print assistant.get_distance(computer.routes[0])

    # The # of different routes from city C to C with distance less then 30
    # Hire an assistant for calculate max distance
    assistant = CalMaxDistanceAssistant(computer)
    assistant.cal_routes("C", "C", 30)
    print len(computer.routes)