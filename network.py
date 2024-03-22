from math import radians, cos, sin, asin, sqrt
import heapq

class Network:
    """Represents the graph for the Charger network. Each node is a Charger class and the network holds the nodes within a dictionary"""
    def __init__(self) -> None:
        self.chargers = {}
        self.charger_csv_info = ()

    def print_network(self):
        """Helper function that prints out all the chargers in the networks and their edges to other nearby chargers"""
        for name, charger in self.chargers.items():
            print(name + " " +  str(charger.edges))

    def print_charger(self,charger_name):
        """Takes in a charger name and prints out the chargers edges if it exists"""
        if charger_name not in self.chargers:
            print("No charger for " + charger_name)
        else:
            print(charger_name + " " + str(self.chargers[charger_name].edges))

    def get_charger_by_id(self, id):
        """Getter method for retrieving a Charger in the network with a provided id"""
        for charger in self.chargers.values():
            if charger.id == id:
                return charger
            
    def get_gps_coords_by_name(self, name_1, name_2):
        """Used in the GUI, takes in the name of 2 chargers and gets the GPS coords that are stored within self.chargers dictionary"""
        lat1,lon1 = self.chargers[name_1].lat, self.chargers[name_1].lon
        lat2, lon2 = self.chargers[name_2].lat, self.chargers[name_2].lon

        return (lat1, lon1, lat2, lon2)

    def build_network(self):
        """Takes in a dataframe and a list of column names and creates a Charger class and adds it to the network's dictionay of chargers"""
        charger_count = 0

        csv_frame, col_names = self.charger_csv_info[0], self.charger_csv_info[1]
        

        for index,row in csv_frame.iterrows():
            name,latitude,longitude = row[col_names[0]], row[col_names[1]], row[col_names[2]]

            if name not in self.chargers:
                self.chargers[name] = Charger(charger_count, latitude, longitude, name)
                charger_count += 1
   
        print(charger_count, "chargers were added to the network")


    def rebuild_network(self, updated_car_range):
        """This is called in the front-end when the user updates the vehicles range within the GUI."""        
        self.chargers = {}
        self.build_network()
        self.add_edges_to_network(updated_car_range)


    def add_edges_to_network(self, max_car_range):
        """Loops through all the chargers that have been added to the network and connects them if the chargers are within the vehicles max range that is passed in"""

        for name1,charger1 in self.chargers.items():
                for name2,charger2 in self.chargers.items():

                    if name1 != name2:
                        dist = round(self.calc_gps_distance(charger1.lat, charger1.lon, charger2.lat,charger2.lon),1)

                        # If the distance between the two Chargers is within 50mi maximum range of the car, then we make an edge between those two Chargers
                        if dist < max_car_range and dist > 50: 
                            charger1.edges.append((dist,charger2.name))
                            charger2.edges.append((dist,charger1.name))


    def calc_gps_distance(self, lat1, lon1, lat2, lon2):
        """Calculates the distance between two GPS coordinates using the Haversine formula that its into account the curvature of the earth"""
        lat1, lon1, lat2, lon2 = map(radians, [lat1,lon1,lat2,lon2])

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 3956 # Radius of earth in miles

        return c * r
    

    
    def calculate_shortest_path(self, start, end):
        """Uses Djikstra's algorithm to determine the shortest path between two chargers. Takes in a name for a starting charger and a name for an ending charger.
        Returns a list that contains the names of all the chargers in the path that was taken to get from start to finish"""
        if start not in self.chargers or end not in self.chargers:
            print("Invalid Charger Name")
            return
        else:

            start_id = self.chargers[start].id
            end_id = self.chargers[end].id
            visited = set() #set to keep track of nodes we have already visited

            # Array to hold all the distances to all the Chargers
            distances = [float('inf')] * len(self.chargers)

            # Array to hold the path we take to get to the end point
            previous = [float('inf')]*len(self.chargers)

            # Set source node distance to 0
            distances[start_id] = 0

            queue = [(0,start_id)]

            # Loop through priority queue and updating distances between adjacent nodes
            while queue:
                curr_dist,curr_id = heapq.heappop(queue)

                if curr_id in visited:
                    continue

                visited.add(curr_id)

                # If we have not reached our destination then continue updating adjacent Charger distances 
                if curr_id != end_id:
                    curr_charger = self.get_charger_by_id(curr_id)

                    for dist,name in curr_charger.edges:
                        adj_charger_id = self.chargers[name].id

                        if adj_charger_id in visited:
                            continue

                        # Checking if we need to update the distance to adjacent charger
                        if distances[adj_charger_id] > distances[curr_id] + dist:
                            distances[adj_charger_id] = distances[curr_id] + dist
                            previous[adj_charger_id] = curr_id #update path for Charger we just updated

                            # Push onto the priorty queue the distance to the adjacent Charger and the Charger id
                            heapq.heappush(queue,(distances[adj_charger_id],adj_charger_id))

                else:
                    # We have reached our destination node

                    final_path = [] # keeps track of our path that we will use to display to the user
                    curr_path_id = end_id #new variable to keep track of our curent path, this gets updated as we work our way through the array to find our patg

                    while previous[curr_path_id] != float('inf'):
                        final_path.append(self.get_charger_by_id(curr_path_id).name)
                        curr_path_id = previous[curr_path_id]

                    # Adding the starting charger for printing purposes later
                    final_path.append(start)

                    return self.print_shortest_path(start,end, final_path) 
                

    def format_name_gui(self, name):
        """Formats charger name to be displayed on the GUI"""
        return name[:-3].replace('_',' ') + ', ' + name[-2:]
                

    def print_shortest_path(self, starting_charger, ending_charger, path_stack):
        """Takes the stack that is returned fromt he calculate_shortest_path method and then prints out the path and the charging times at each Charger"""
        prev = starting_charger
        result = ""
        count = 1
        while path_stack:
            curr = path_stack.pop()

            if curr == starting_charger or curr == ending_charger:
                if curr == starting_charger:
                    result += f'Start - {self.format_name_gui(curr)}'
                    result += "\n\n Charging Stops:\n"
                elif curr == ending_charger:
                    result += "\n"
                    result += f'End - {self.format_name_gui(curr)}'


                continue

            charging_time, distance_traveled = self.calculate_charging_time(prev,curr)
            
            result += f'{count}) {self.format_name_gui(curr)} \n     {int(distance_traveled)} miles Traveled \n     {charging_time} min. of Charging'
            result += "\n"
            count +=1
            prev = curr

        return result


    def calculate_charging_time(self, charger_1_name, charger_2_name):
        """Takes in two charger names and calculates the charging time. Returns the calculated charging time as well as the distance travelled between the two Chargers"""
        charger_1, charger_2  = self.chargers[charger_1_name], self.chargers[charger_2_name]

        lat1,lon1 = charger_1.lat, charger_1.lon
        lat2,lon2 = charger_2.lat, charger_2.lon

        distance = round(self.calc_gps_distance(lat1,lon1,lat2,lon2),1)
        
        charging_time_min = round((distance/498)*60,1) # charging at 800km /hr or 498mi /hr

        return (charging_time_min, distance)


        
class Charger:
    """An individual Charger in the Network. Represents a node within the graph"""
    def __init__(self,id,lat,lon,name) -> None:
        self.name = name
        self._id = id
        self._lat = lat
        self._lon = lon
        self._edges = []

    def __str__(self) -> str:
        return f"Name: {self.name} Latitude: {self.lat} Longitude: {self.lon}"
    
    @property
    def id(self):
        return self._id
    
    @property
    def lat(self):
        return self._lat
    

    @property
    def lon(self):
        return self._lon
    

    @property
    def edges(self):
        return self._edges

    def print_edges(self):
        print(self.edges)

    def add_edge(self, distance, dest_charger):
        self.edges.append((distance,dest_charger))
    

