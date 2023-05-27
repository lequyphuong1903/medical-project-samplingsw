import sys
import os
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.widgets import SliderBase
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import json
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMessageBox, QFileDialog
from PyQt5.QtWidgets import QLineEdit, QCheckBox, QComboBox, QDoubleSpinBox, QTextEdit
from PyQt5.QtWidgets import  QHBoxLayout, QVBoxLayout, QScrollArea, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, QTime, QDateTime
from collections import OrderedDict

#GUI gnerate
class Canvas(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(6, 2))
        super().__init__(fig)
        self.setParent(parent.sigplt)
    def plt(self, t):
        self.ax.clear()
        self.ax.plot(t)
        self.ax.grid()
        self.draw()

class bang_1(QtWidgets.QMainWindow):
    def __init__(self):
        super(bang_1, self).__init__()
        loadUi("Bang_1.ui", self)
        self.sigplt = Canvas(self)  # Create an instance of MyWidget

#Initial
app = QApplication(sys.argv)
welcome = bang_1()
welcome.patient_list.setColumnWidth(0, 271)
widget = QtWidgets.QStackedWidget()
widget.setFixedHeight(896)
widget.setFixedWidth(919)
widget.addWidget(welcome)
data_list = ["date", "name", "birthday", "gender", "code", "eat_30", "fatigue", "choppy", "vomic", "weight", "height",
             "pulse_1", "SBP_1", "DBP_1", "smoke",
             "alcohol", "sleep_time", "that_nguc", "tang_huyet_ap", "tieu_duong", "suy_tim", "heart_op_1", "van_tim",
             "DMV_1", "vessel_1", "ho_van_tim", "ho_van_DMC",
             "ho_van_2_la", "ho_van_3_la", "loan_nhip", "nhip_nhanh_tren_that", "block_nhi_that", "rung_nhi", "PVC",
             "PAC", "bloc_trai", "block_phai", "pulse_2", "SPO2", "SBP_2",
             "DBP_2", "xoan_dinh", "rung_that", "xoang_nhanh", "f_xoang_nhanh", "that_nhanh", "f_that_nhanh",
             "rung_nhi_2", "so_luong", "dap_ung", "tim_cham", "f_tim_cham", "cham_xoang",
             "block_nhi_that_1", "block_nhi_that_2", "mobitz_1", "mobitz_2", "block_nhi_that_3", "xvdm", "xvdmv",
             "ngoai_thu_tam_nhi", "ngoai_thu_tam_that", "block_that_trai", "block_that_phai"]
flush_data = OrderedDict()
app_obj = {a: getattr(welcome, a) for a in data_list}
#Variable
new_flag = True
current_Table = ""
link = os.path.join(os.path.dirname(__file__), 'Data')

#Functions
#   Update the patient list
def patient_list(path):
    file_list = [f for f in os.listdir(path) if f.endswith('.json')]
    welcome.patient_list.clearContents()
    welcome.patient_list.setRowCount(0)
    for i, file_name in enumerate(file_list):
        welcome.patient_list.insertRow(i)
        welcome.patient_list.setItem(i, 0, QtWidgets.QTableWidgetItem(file_name))

#   Update the data
def show_data(data):
    global app_obj
    for child in app_obj:
        if isinstance(app_obj[child], QLineEdit):
            app_obj[child].setText(data[app_obj[child].objectName()])
        elif isinstance(app_obj[child], QCheckBox):
            app_obj[child].setChecked(data[app_obj[child].objectName()])
        elif isinstance(app_obj[child], QDoubleSpinBox):
            app_obj[child].setValue(data[app_obj[child].objectName()])
        elif isinstance(app_obj[child], QComboBox):
            app_obj[child].setCurrentText(data[app_obj[child].objectName()])

#   Store data
def store_data():
    global app_obj
    data = OrderedDict()
    for child in app_obj:
        if isinstance(app_obj[child], QLineEdit):
            data[app_obj[child].objectName()] = app_obj[child].text()
        elif isinstance(app_obj[child], QCheckBox):
            data[app_obj[child].objectName()] = app_obj[child].isChecked()
        elif isinstance(app_obj[child], QDoubleSpinBox):
            data[app_obj[child].objectName()] = app_obj[child].value()
        elif isinstance(app_obj[child], QComboBox):
            data[app_obj[child].objectName()] = app_obj[child].currentText()
    return data

#   Json file read
def read_file(file_name):
    script_dir = os.path.dirname(__file__)
    data_dir = os.path.join(script_dir, 'Data')
    f = open(os.path.join(data_dir, file_name), 'r')
    data = json.load(f)
    return data

#   Json file write
def write_file(file_name, data):
    script_dir = os.path.dirname(__file__)
    data_dir = os.path.join(script_dir, 'Data')
    f = open(os.path.join(data_dir, file_name), 'w')
    json.dump(data, f)

#   Startup
def startup():
    global new_flag
    global current_Table
    global link
    global flush_data
    global ecg_signal
    global ppg_signal
    global ecg_check
    global ppg_check
    ppg_check = True
    ecg_check = False
    ecg_signal = []
    ppg_signal = []
    flush_data = store_data()
    patient_list(link)

startup()

#   Callbacks
#   Table choose
def table_choose(item):
    global new_flag
    global current_Table
    global link
    global ecg_check
    global ppg_check
    global ppg_signal
    global ecg_signal
    file_name = welcome.patient_list.item(item.row(), item.column()).text()
    current_Table = file_name
    data = read_file(file_name)
    ecg_signal = data["ECG_SIG"]
    ppg_signal = data["PPG_SIG"]
    show_data(data)
    if (ecg_check == True):
        if ecg_signal == []:
            welcome.sigplt.plt([])
            return
        id = welcome.ECGSpin.value()
        welcome.sigplt.plt(ecg_signal[id-1])
    elif (ppg_check == True):
        welcome.sigplt.plt(ppg_signal)
    show_data(data)
welcome.patient_list.itemClicked.connect(table_choose)

#   New button
def New_button():
    global new_flag
    global current_Table
    global link
    global flush_data
    show_data(flush_data)
    new_flag = True
    current_Table = ""

welcome.New.clicked.connect(New_button)

#   Save button
def Save_button():
    global new_flag
    global current_Table
    global link
    global ppg_signal
    global ecg_signal
    data = store_data()
    data["ECG_SIG"] = ecg_signal
    data["PPG_SIG"] = ppg_signal
    file_name = data['code'] + "_" + data['name'] + ".json"
    if (file_name == "_.json"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Chưa nhập tên và mã số")
        msg.setWindowTitle("Cảnh báo")
        msg.exec_()
    else:
        if new_flag != True:
            if file_name != current_Table:
                remove_file = os.path.join(link, current_Table)
                if os.path.exists(remove_file):
                    os.remove(remove_file)
        write_file(file_name, data)
        new_flag = False
        current_Table = file_name
        patient_list(link)
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Information)
        message_box.setText("Saved successfully")
        message_box.exec_()

welcome.Save.clicked.connect(Save_button)

#   Restore button
def Restore_button():
    global current_Table
    data = read_file(current_Table)
    show_data(data)

welcome.Restore.clicked.connect(Restore_button)

# Load ECG
def ECG_Signal():
    global ecg_signal
    dialog = QFileDialog()
    file_path, _ = dialog.getOpenFileName()
    if file_path.endswith(".xml"):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Information)
        message_box.setWindowTitle("Selected status")
        message_box.setText("Load ECG signal successfully")
        message_box.exec_()
    else:
        error_message = "Invalid file selected. Please choose an XML file."
        QMessageBox.critical(None, "Error", error_message)
        return
    tree = ET.parse(file_path)
    root = tree.getroot()
    # Find the element with the specified namespace
    namespace = "{urn:hl7-org:v3}"
    for element in root.iter():
        if element.tag == f"{namespace}digits":
            element_text = element.text
            value = [int(num) for num in element_text.split()]
            ecg_signal.append(value)
    id = welcome.ECGSpin.value()
    welcome.sigplt.plt(ecg_signal[id - 1])
welcome.ECG_Signal.clicked.connect(ECG_Signal)

# Load PPG
def PPG_Signal():
    global ppg_signal
    dialog = QFileDialog()
    file_path, _ = dialog.getOpenFileName()
    if file_path.endswith(".csv"):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Information)
        message_box.setWindowTitle("Selected status")
        message_box.setText("Load PPG signal successfully")
        message_box.exec_()
    else:
        error_message = "Invalid file selected. Please choose a CSV file."
        QMessageBox.critical(None, "Error", error_message)
        return
    data_frame = pd.read_csv(file_path)
    ppg = data_frame.values.tolist()
    ppg_signal.extend(ppg)
    welcome.sigplt.plt(ppg_signal)
welcome.PPG_Signal.clicked.connect(PPG_Signal)

# Plot PPG
def plotppg():
    global ppg_signal
    global ppg_check
    global ecg_check
    ppg_check = True
    ecg_check = False
    welcome.sigplt.plt(ppg_signal)
welcome.PPG_Plot.clicked.connect(plotppg)

# Plot ECG
def plotecg():
    global ecg_signal
    global ppg_check
    global ecg_check
    ppg_check = False
    ecg_check = True
    if ecg_signal == []:
        error_message = "Please input ECG."
        QMessageBox.critical(None, "Error", error_message)
        return
    id = welcome.ECGSpin.value()
    welcome.sigplt.plt(ecg_signal[id - 1])

welcome.ECG_Plot.clicked.connect(plotecg)

welcome.ECGSpin.valueChanged.connect(plotecg)


def text_change():
    global link
    text = welcome.searchbox.text()
    if (text == ""):
        patient_list(link)
    else:
        file_list = [f for f in os.listdir(link) if f.endswith('.json')]
        matches = []
        for file in file_list:
            if text in file:
                matches.append(file)
        welcome.patient_list.clearContents()
        welcome.patient_list.setRowCount(0)
        for i, file_name in enumerate(matches):
            welcome.patient_list.insertRow(i)
            welcome.patient_list.setItem(i, 0, QtWidgets.QTableWidgetItem(file_name))

welcome.searchbox.textChanged.connect(text_change)



widget.show()
sys.exit(app.exec_())
