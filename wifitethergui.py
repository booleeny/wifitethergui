import sys
import subprocess
from PyQt4 import QtCore, QtGui, uic

Ui_MainWindow, QtBaseClass = uic.loadUiType("tethergui.ui")
Ui_Dialog, QtBaseClass = uic.loadUiType("tethergui_popup.ui")


class Popup(QtGui.QDialog, Ui_Dialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        Ui_Dialog.__init__(self)
        self.setupUi(self)

class Wifitethergui(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Activate Statusbar
        self.statusBar()

        # BUTTONS
        self.pushButton_ceckhostedtrue.clicked.connect(self.checkhosttrue)
        self.pushButton_start_hotspot.clicked.connect(self.starthotspot)
        self.pushButton_stop_hotspot.clicked.connect(self.stophotspot)
        self.pushButton_info.clicked.connect(self.info)
        self.actionAbout.triggered.connect(self.openabout)

    def openabout(self):
        QtGui.QMessageBox.about(self, "About",
                                "Working on Win 8,8.1,10\nShare your wired network (LAN) as WiFi Hotspot/AccessPoint.\n\nby booleeny")

    def checkhosttrue(self):
        cmd_dos = subprocess.check_output('netsh wlan show drivers', shell=False)
        cmd_win = cmd_dos.decode("cp850")
        self.textEdit.setText(cmd_win)

        substring_de = "Unterstützte gehostete Netzwerke  : Ja"
        substring_en = "Hosted network supported  : Yes"
        check_de = substring_de in cmd_win
        check_en = substring_en in cmd_win
        if check_de:
            self.statusBar().showMessage("Hosted Networks are possible with this network card.")
        elif check_en:
            self.statusBar().showMessage('Hosted Networks are possible with this network card.')
        else:
            self.statusBar().showMessage("ERROR: Hosted networks are NOT possible with this network card.")

    def info(self):
        self.popup = Popup()
        self.popup.show()
        # subprocess.call('control.exe ncpa.cpl')

    def starthotspot(self):
        ssid = str(self.lineEdit_ssid.text())
        pwd = str(self.lineEdit_pwd.text())
        if len(pwd) < 8:
            self.textEdit.setText("ERROR:\nPassword must have at least 8 characters (max. 63).\n"
                                  "Current passwort \"" + pwd + "\" is " + str(len(pwd)) + " characters long.\n")
        else:
            subprocess.call("netsh wlan set hostednetwork mode=allow ssid=" + ssid + " key=" + pwd, shell=False)
            subprocess.call('netsh wlan start hostednetwork')
            self.textEdit.setText("SSID set to: " + ssid)
            self.textEdit.setText("Password set to: " + pwd)
            subprocess.call('control.exe ncpa.cpl')
            self.textEdit.setText("WiFi Hotspot started. Don't forget to enable sharing.")
            self.popup = Popup()
            self.popup.show()

    # subprocess.call('control.exe ncpa.cpl')

    def stophotspot(self):
        subprocess.call("netsh wlan set hostednetwork mode=disallow")
        subprocess.call("netsh wlan stop hostednetwork")
        self.textEdit.setText("WLAN Hotspot stopped.")


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Wifitethergui()
    window.show()
    sys.exit(app.exec_())
