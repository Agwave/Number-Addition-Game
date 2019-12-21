import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from objects.generate_matrix import Matrix
from ui.mainWindow import MainWindow
from objects.music import Music

class SettingWindow(QtWidgets.QWidget):

    def __init__(self, music):
        super().__init__()
        self.music = music
        self.music.play()
        self.initUI()

    def initUI(self):
        self._set_overall_situation()
        self._create_form()
        self._create_start_bottom()

    def _set_overall_situation(self):
        self.setWindowTitle("游戏设置")
        self.setGeometry(0, 0, 300, 200)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowMinimizeButtonHint| Qt.WindowCloseButtonHint)
        self.center()
        self.use_palette()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def use_palette(self):
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(),
                             QtGui.QBrush(QtGui.QPixmap("./picture_files/green_background.jpeg")))
        self.setPalette(window_pale)

    def _create_form(self):
        self.form_layout = QtWidgets.QFormLayout()
        label1 = QtWidgets.QLabel("迷宫大小")
        self.combobox = QtWidgets.QComboBox(self)
        self.combobox.addItems(["5×5", "7×7", "9×9", "11×11", "13×13", "15×15", "17×17"])
        label2 = QtWidgets.QLabel("音乐音量")
        self.slider = self._get_slider()
        self.form_layout.addRow(label1, self.combobox)
        self.form_layout.addRow(label2, self.slider)
        self.setLayout(self.form_layout)

    def _get_slider(self):
        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setSingleStep(1)
        slider.setValue(50)
        slider.valueChanged.connect(self._slider_change)
        return slider

    def _create_start_bottom(self):
        self.start_bottom = QtWidgets.QPushButton("开始游戏", self)
        self.start_bottom.resize(60, 30)
        self.start_bottom.move(120, 120)
        self.start_bottom.clicked.connect(self._generate_numbers)

    def _generate_numbers(self):
        self.setting_to_main()

    def setting_to_main(self):
        size = self.combobox.currentIndex() * 2 + 5
        m = Matrix(size)
        main_window = MainWindow(m)
        main_window.show()
        self.setHidden(True)
        main_window.main_close_signal.connect(self.main_to_setting)

    def main_to_setting(self):
        self.setHidden(False)

    def _slider_change(self):
        volumn = self.slider.value()/100.0
        self.music.set_volumn(volumn)
