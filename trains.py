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

class Assistant:
    def __init__(self):
        self.cities = {}
        self.reset_shortest_route()
        self.routes = []

    def add_city(self, city):
        self.cities[city.city_name] = city

    def add_cities(self, city_list):
        for city in city_list:
            self.add_city(city)

    def get_city(self, city_name):
        return self.cities[city_name]

    def reset_shortest_route(self):
        self.shortest_distance = -1
        self.shortest_route = ""

    def get_distance(self, route):
        """
        Get distance of the route.

        @param route: route string which split by '-', such as 'A-B-C'
        """
        total_distance = 0
        try:
            if route:
                city_list = route.split("-")
                start_city = self.get_city(city_list.pop(0))
                while city_list:
                    end_city = self.get_city(city_list.pop(0))
                    distance = start_city.get_distance(end_city)
                    total_distance = total_distance + distance
                    start_city = end_city
        except Exception as e:
            return e.message
        return total_distance

    def cal_max_stops_routes(self, start_city_name, end_city_name, max_stops):
        """
        Calculate how many routes can from first city of route_path to end_city.
        The routes will be saved to self.routes list

        @param start_city_name: the route path string, such as 'ABC'
        @param end_city_name: the end city name string
        """
        if (len(start_city_name) - 1) > max_stops:
            return

        if len(start_city_name) > 1 and start_city_name.endswith(end_city_name):
            self.routes.append(start_city_name)

        end_city = self.get_city(start_city_name[-1])
        for route in end_city.start_routes:
            self.cal_max_stops_routes(start_city_name + route.end_city.city_name, end_city_name, max_stops)

    def get_exact_stops_routes(self, start_city_name, end_city_name, extra_stops):
        """
        Return the route list from start_city to end_city with extra stops.

        @param start_city_name: start city name
        @param end_city_name: end city name
        @param extra_stops: extra stops
        """
        last_route_paths = [start_city_name,]
        for stop in range(extra_stops):
            route_paths = []
            for route_path in last_route_paths:
                city = self.get_city(route_path[-1])
                for route in city.start_routes:
                    new_route_path = route_path + route.end_city.city_name
                    route_paths.append(new_route_path)
            # Please care about this need to copy a list, can not assignment
            last_route_paths = route_paths[:]

        routes = []
        for route in last_route_paths:
            if route.endswith(end_city_name):
                routes.append(route)
        return routes

    def cal_shortest_route(self, start_city_name, end_city_name, distance=0):
        """
        Calculate the shortest route from start city to end city.
        The result will be save into self.shortest_route and self.shortest_distance

        @param start_city_name: start city name
        @param end_city_name: end city name
        """
        if start_city_name.endswith(end_city_name) and distance > 0 and (
        distance < self.shortest_distance or self.shortest_distance == -1):
            self.shortest_route = start_city_name
            self.shortest_distance = distance

        end_city = self.get_city(start_city_name[-1])
        for route in end_city.start_routes:
            if route.end_city.city_name in start_city_name[1:]:
                # Check if the end city name has been in start_city_name, means repeat route, will not calculate.
                continue
            self.cal_shortest_route(start_city_name + route.end_city.city_name, end_city_name, distance + route.distance)

    def cal_all_routes(self, start_city_name, end_city_name, distance=0, max_distance=30):
        """
        Calculate all routes from start city to end city which max distance less then 30.
        The result save to self.routes.

        @param start_city_name: start city name
        @param end_city_name: end city name
        """
        if distance >= max_distance:
            return

        if distance > 0 and start_city_name.endswith(end_city_name):
            self.routes.append("%s : %d" % (start_city_name, distance))

        end_city = self.get_city(start_city_name[-1])
        for route in end_city.start_routes:
            self.cal_all_routes(start_city_name + route.end_city.city_name, end_city_name, distance + route.distance)

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

    # Hire an assistant
    assistant = Assistant()

    # The assistant need to study cities
    assistant.add_cities([a, b, c, d, e])

    # Please tell me the distance of route A-B-C
    print assistant.get_distance("A-B-C")

    # How much distance of route A-D ?
    print assistant.get_distance("A-D")

    # And how much of A-D-C
    print assistant.get_distance("A-D-C")

    # And A-E-B-C-D ?
    print assistant.get_distance("A-E-B-C-D")

    # A-E-D ?
    print assistant.get_distance("A-E-D")

    # The # of trips between city C and C with a max stops 3
    assistant.routes = []
    assistant.cal_max_stops_routes("C", "C", 3)
    print assistant.routes
    print len(assistant.routes)

    # Print how many routes between city A to C and extra stops if 4
    routes = assistant.get_exact_stops_routes("A", "C", 4)
    print routes
    print len(routes)

    # The shortest route of city A to city C
    assistant.reset_shortest_route()
    assistant.cal_shortest_route("A", "C")
    print assistant.shortest_distance

    # The shortest route of city B to city B
    assistant.reset_shortest_route()
    assistant.cal_shortest_route("B", "B")
    print assistant.shortest_distance

    # The # of different routes from city C to C with distance less then 30
    assistant.routes = []
    assistant.cal_all_routes("C", "C")
    print assistant.routes
    print len(assistant.routes)