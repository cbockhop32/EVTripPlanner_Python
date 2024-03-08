import pandas as pd
import network
import sys

car_range = 198

# Get charger list from CSV file and add labels within pandas df
col_names = ['City','Latitude','Longitude']
df = pd.read_csv('network.csv', names= col_names, header=None)

starting_charger, ending_charger = sys.argv[1], sys.argv[2]

# Initialize new network and then build network of chargers
new_network = network.Network()
new_network.build_network(df,col_names)
new_network.add_edges_to_network(car_range)

new_network.calculate_shortest_path(starting_charger, ending_charger)


