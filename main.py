import sys

from PyQt5 import QtWidgets
from ui.settingWindow import SettingWindow
from objects.music import Music

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    music = Music()
    setting_window = SettingWindow(music)
    setting_window.show()
    sys.exit(app.exec_())