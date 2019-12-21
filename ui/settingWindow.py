from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from objects.generate_matrix import Matrix
from ui.mainWindow import MainWindow

class SettingWindow(QtWidgets.QWidget):

    def __init__(self, music):
        super().__init__()
        self.initUI()
        self.music = music
        self.music.play()

    def initUI(self):
        self._set_overall_situation()
        self._create_form()
        self._create_start_bottom()

    def _set_overall_situation(self):
        self.setWindowTitle("游戏设置")
        self.setGeometry(0, 0, 300, 170)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowMinimizeButtonHint| Qt.WindowCloseButtonHint)
        self._center()
        self._use_palette()

    def _center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _use_palette(self):
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(),
                             QtGui.QBrush(QtGui.QPixmap("./picture_files/green_background.jpeg")))
        self.setPalette(window_pale)

    def _create_form(self):
        self.form_layout = QtWidgets.QFormLayout()
        label1 = QtWidgets.QLabel("迷宫大小")
        self.combobox_size = QtWidgets.QComboBox(self)
        self.combobox_size.addItems(["5×5", "7×7", "9×9", "11×11", "13×13", "15×15", "17×17"])
        label2 = QtWidgets.QLabel("音乐音量")
        self.slider = self._get_slider()
        label3 = QtWidgets.QLabel("游戏难度")
        self.combobox_time = QtWidgets.QComboBox(self)
        self.combobox_time.addItems(["简单", "普通", "困难", "地狱"])
        self.form_layout.addRow(label1, self.combobox_size)
        self.form_layout.addRow(label2, self.slider)
        self.form_layout.addRow(label3, self.combobox_time)
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
        self.mat_size = self.combobox_size.currentIndex() * 2 + 5
        self.game_time = (4 - self.combobox_time.currentIndex()) * 15 * (self.combobox_size.currentIndex() + 1)
        m = Matrix(self.mat_size)
        main_window = MainWindow(m, self.game_time, 3)
        main_window.show()
        self.setHidden(True)
        main_window.main_close_signal.connect(self.main_to_setting)
        main_window.main_regen_signal.connect(self.regen_game)

    def main_to_setting(self):
        self.setHidden(False)

    def regen_game(self, game_num):
        m = Matrix(self.mat_size)
        main_window = MainWindow(m, self.game_time, game_num)
        main_window.show()
        main_window.main_close_signal.connect(self.main_to_setting)
        main_window.main_regen_signal.connect(self.regen_game)

    def _slider_change(self):
        volumn = self.slider.value()/100.0
        self.music.set_volumn(volumn)

    def closeEvent(self, QCloseEvent):
        reply = QtWidgets.QMessageBox.question(self,
                                               '退出',
                                               "确定要退出游戏吗？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.close()
        else:
            QCloseEvent.ignore()
