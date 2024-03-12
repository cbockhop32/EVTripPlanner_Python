import pandas as pd
import network
import front_end
import sys


def main(*args):
    car_range = 300 # car range in miles


    # Get charger list from CSV file and add labels within pandas df
    col_names = ['City','Latitude','Longitude']
    df = pd.read_csv('network.csv', names= col_names, header=None)

    cities = df['City'].tolist()

    # Initialize new network and then build network of chargers
    new_network = network.Network()
    new_network.build_network(df,col_names)
    new_network.add_edges_to_network(car_range)

    # Qapplication instance (can pass command line args if you want)
    app = front_end.QtWidgets.QApplication()
    widget = front_end.MyWidget(cities, new_network.calc_gps_distance, new_network.get_gps_coords_by_name, new_network.calculate_shortest_path)
    widget.resize(1000, 600)
    widget.show()

    # new_network.calculate_shortest_path(starting_charger, ending_charger)

    sys.exit(app.exec())

    

if __name__ == '__main__':
    main(*sys.argv[1:])


