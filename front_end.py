from PySide6 import QtCore, QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):
    def __init__(self,cities, calc_gps_func, get_charger_gps, calc_shortest_path) -> None:
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.charger_list = sorted(city[:-3].replace('_',' ') + ', ' + city[-2:] for city in cities)
        self.starting_charger = "Select Starting Charger"
        self.ending_charger = "Select Destination Charger"


        self.setWindowTitle('EV Trip Planner')

        #----------Header Widget and Layout --------------#
        header_widget = QtWidgets.QWidget()
        start_label = QtWidgets.QLabel()
        end_label = QtWidgets.QLabel()
        distance_label = QtWidgets.QLabel()


        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addWidget(start_label)
        header_layout.addWidget(end_label)
        header_layout.addWidget(distance_label)
      

        header_widget.setLayout(header_layout)
        #--------------------------------------------------#


        #--------Main Content Widget and Layout ----------#
        main_content_widget = QtWidgets.QWidget()
        results_widget = QtWidgets.QTextBrowser()
        main_content_layout = QtWidgets.QHBoxLayout()


        # Two city seletors and adding the list of cities to each of them
        start_selector = QtWidgets.QListWidget()
        end_selector = QtWidgets.QListWidget()
        gen_button = QtWidgets.QPushButton("Generate Path")

        start_selector.addItem("Select Starting Charger")
        start_selector.addItems(self.charger_list)
        start_selector.setCurrentRow(0)

        end_selector.addItem("Select Destination Charger")
        
        end_selector.addItems(self.charger_list)
        end_selector.setCurrentRow(0)


        main_content_layout.addWidget(start_selector)
        main_content_layout.addWidget(end_selector)
        main_content_layout.addWidget(results_widget)
        main_content_layout.addWidget(gen_button)
        main_content_widget.setLayout(main_content_layout)

     
        #----------------------------------------------#

        def format_name_network(name):
            """Helper function that formats the name of a Charger so it can be sent back to the Network class to be used. Replaces spaces with underscores"""
            return name.replace(', ','_').replace(' ','_')

        def calculate_shortest_path():
            if (self.starting_charger != "Select Starting Charger" and self.ending_charger != "Select Destination Charger")  and (self.starting_charger != self.ending_charger):
                
                res = calc_shortest_path(format_name_network(self.starting_charger), format_name_network(self.ending_charger))
                results_widget.setText(res)


        def calculate_distance():
                """Calculates the distance and displays it when the user changes the Charger selection. 
                Uses get_charger_gps and get_charger_gps functions passed into the Widget from the Network class"""
                lat1,lon1, lat2, lon2 = get_charger_gps(format_name_network(self.starting_charger), format_name_network(self.ending_charger) )

                dist = '{:,}'.format(int(calc_gps_func(lat1,lon1,lat2,lon2)))
                distance_label.setText(f'{dist} miles')


        def start_selection(charger_val):
            self.starting_charger = charger_val.text()
            start_label.setText(f"Starting:  {self.starting_charger}")

            if self.starting_charger != "Select Starting Charger" and self.ending_charger != "Select Destination Charger":
                calculate_distance()

            
        def end_selection(charger_val):
            self.ending_charger = charger_val.text()
            end_label.setText(f"Ending:  {self.ending_charger}" )

            if self.starting_charger != "Select Starting Charger" and self.ending_charger != "Select Destination Charger":
                calculate_distance()

        


        # Enable signal for selecting on both the start charger and the end charger
        start_selector.itemClicked.connect(start_selection)
        end_selector.itemClicked.connect(end_selection)
        gen_button.clicked.connect(calculate_shortest_path)
               
            
        # Adding header widget and main content widet to the the parent layout
        self.layout.addWidget(header_widget)
        self.layout.addWidget(main_content_widget)






        

    # @QtCore.Slot()
    # def generate_path(self,start,end):
    #     if (start != "Select Starting Charger" and end != "Select Destination Charger") and (start != end):
             
    #     else:
    #          pass
        


  





