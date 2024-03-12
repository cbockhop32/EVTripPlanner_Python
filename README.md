# EVTripPlanner


## Background

This program will take a CSV file that has names and locations (by GPS coordinates: latitude and longitude) and parse the CSV file to create a network of chargers.
Then the user the input two names of chargers within the network/CSV file and the program will return the shortest route between those two points, giving you
the necessary charger stops and charging times at each charger on your way to the destination.

The program assumes that your hypothetical electric car has a fixed range and the path route will be depended on the vehichle's range


## Running the program 

python main.py 

![alt text](imgs/screenshot1.png)


Output:

Hawthorne_CA
Inyokern_CA - 122.7 Miles Traveled - 14.8 Minutes of Charging Time
Las_Vegas_NV - 153.8 Miles Traveled - 18.5 Minutes of Charging Time
St._George_UT - 107.9 Miles Traveled - 13.0 Minutes of Charging Time
Richfield_UT - 141.3 Miles Traveled - 17.0 Minutes of Charging Time
South_Salt_Lake_City_UT - 133.8 Miles Traveled - 16.1 Minutes of Charging Time
Idaho_Falls_ID - 191.1 Miles Traveled - 23.0 Minutes of Charging Time
Bozeman_MT