from PySide6 import QtCore, QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):
    def __init__(self,cities, calc_gps_func, get_charger_gps, calc_shortest_path, rebuild_charger_network, car_range) -> None:
        super().__init__()
        self.vehicle_range = car_range
        self.layout = QtWidgets.QGridLayout(self)
        self.charger_list = sorted(city[:-3].replace('_',' ') + ', ' + city[-2:] for city in cities)
        self.starting_charger = "Select Starting Charger"
        self.ending_charger = "Select Destination Charger"


        self.setWindowTitle('EV Trip Planner')


        def range_edit_clicked(s):
            dlg = RangeUpdate(self.vehicle_range)

            if dlg.exec():
                # print('success')
                self.vehicle_range = dlg.range_val
                range_label.setText(f'{self.vehicle_range} mi. range')
                rebuild_charger_network(self.vehicle_range)
                # print(self.vehicle_range)
            else:
                print('Vehicle Range Not Updated')

        # Range Edit button and label
        range_button = QtWidgets.QPushButton("Update Range")
        range_label = QtWidgets.QLabel(f'{self.vehicle_range} mi. range')
        range_button.clicked.connect(range_edit_clicked)
        range_widget = QtWidgets.QWidget()

        range_edit_layout = QtWidgets.QVBoxLayout()
        range_edit_layout.addWidget(range_label)
        range_edit_layout.addWidget(range_button)


        range_widget.setLayout(range_edit_layout)


        #----------Header Widget and Layout --------------#
        header_widget = QtWidgets.QWidget()
        start_label = QtWidgets.QLabel()
        end_label = QtWidgets.QLabel()
        distance_label = QtWidgets.QLabel()

        #--------------------------------------------------#



        #--------Main Content Widget and Layout ----------#
        main_content_widget = QtWidgets.QWidget()
        main_content_layout = QtWidgets.QHBoxLayout()


        # Two city seletors and adding the list of cities to each of them
        start_selector = QtWidgets.QListWidget()
        end_selector = QtWidgets.QListWidget()
        results_widget = QtWidgets.QTextBrowser()

        gen_button = QtWidgets.QPushButton("Generate Path")

        start_selector.addItem("Select Starting Charger")
        start_selector.addItems(self.charger_list)
        start_selector.setCurrentRow(0)

        end_selector.addItem("Select Destination Charger")
        
        end_selector.addItems(self.charger_list)
        end_selector.setCurrentRow(0)


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


        # int,ok =    QtWidgets.QInputDialog().getInt(self,"Input Range", "Vehicle Range", QtWidgets.QLineEdit.Normal, QtCore.QDir().home().dirName())
            
        # Adding header widget and main content widet to the the parent layout
        self.layout.addWidget(start_label,0,0)
        self.layout.addWidget(end_label,0,1)
        self.layout.addWidget(distance_label,0,2)
        self.layout.addWidget(range_widget,0,3)
        self.layout.addWidget(start_selector,1,0)
        self.layout.addWidget(end_selector,1,1)
        self.layout.addWidget(results_widget,1,2)
        self.layout.addWidget(gen_button,1,3)

        self.setLayout(self.layout)


  
class RangeUpdate(QtWidgets.QDialog):
    def __init__(self, init_range):
        super().__init__()
        self.range_val = init_range
        self.setWindowTitle("Update Range")
        

        Qbtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(Qbtn)
        self.buttonBox.accepted.connect(self.update_val)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Input new vehicle range:")

        self.range_input = QtWidgets.QInputDialog()
        self.range_input.setOption(QtWidgets.QInputDialog.NoButtons)
        self.range_input.setInputMode(QtWidgets.QInputDialog.IntInput)
        self.range_input.setIntRange(50,1000)
        self.range_input.setIntValue(self.range_val)

        intEditLine = self.range_input.findChild(QtWidgets.QLineEdit)
        intEditLine.setPlaceholderText(str(self.range_val))



        self.layout.addWidget(message)
        self.layout.addWidget(self.range_input)

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def update_val(self):
        self.range_val = self.range_input.intValue()
        self.accept()




