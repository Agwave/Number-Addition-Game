from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

class MainWindow(QtWidgets.QWidget):

    def __init__(self, m, game_time, game_num):
        super().__init__()
        self.matrix = m.matrix
        self.game_time = game_time
        self.game_num = game_num
        self.close_flag = True
        self.initUI()

    main_close_signal = QtCore.pyqtSignal()
    main_regen_signal = QtCore.pyqtSignal(int)

    def initUI(self):
        self._set_overall_situation()
        self._create_num_buttoms()
        self._create_confirm_buttom()
        self.show()

    def _set_overall_situation(self):
        self.setWindowTitle("加法数字游戏")
        self.length = 50 * len(self.matrix)
        width = self.length + 100
        height = self.length + 200
        self.setGeometry(0, 0, width, height)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowMinimizeButtonHint| Qt.WindowCloseButtonHint)
        self._create_arrow()
        self.center()
        self.use_palette()
        self._create_time_label()

    def _create_arrow(self):
        lable1 = QtWidgets.QLabel(self)
        lable2 = QtWidgets.QLabel(self)
        lable1.setGeometry(0, 50, 50, 50)
        lable2.setGeometry(self.length+50, self.length, 50, 50)
        pix = QtGui.QPixmap("./picture_files/arrow.jpeg")
        lable1.setPixmap(pix)
        lable2.setPixmap(pix)
        lable1.setScaledContents(True)
        lable2.setScaledContents(True)

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def use_palette(self):
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(),
                             QtGui.QBrush(QtGui.QPixmap("./picture_files/blue_micro.jpeg")))
        self.setPalette(window_pale)

    def _create_time_label(self):
        self.time_label = MyLabel(self)
        self.time_label.move(50, self.length+70)
        self.time_label.set_sec(self.game_time)
        self.time_label.my_start_time(1000)
        self.time_label.timeout_signal.connect(self._game_fail)

    def _create_num_buttoms(self):
        self.num_buttoms = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                b = QtWidgets.QPushButton(str(int(self.matrix[i][j])), self)
                b.resize(50, 50)
                b.move(j*50+50, i*50+50)
                b.clicked.connect(lambda:self.set_color(self.sender()))
                self.num_buttoms.append(b)
        self.num_buttoms[0].setStyleSheet("background-color: yellow")
        self.index = [0]
        self.next_selectable_b_index = self._get_next_selectable_b_index()

    def _create_confirm_buttom(self):
        self.confirm_buttom = QtWidgets.QPushButton("确认", self)
        self.confirm_buttom.resize(60, 30)
        self.confirm_buttom.move(self.length/2+20, self.length+70)
        self.confirm_buttom.clicked.connect(self.process_commit)

    def process_commit(self):
        if not self.num_buttoms[-1].styleSheet() == "background-color: yellow":
            QtWidgets.QMessageBox.information(self, "错误", "你还未到达出口")
        else:
            flag = True
            commit_list = []
            for ind in self.index:
                b = self.num_buttoms[ind]
                commit_list.append(int(b.text()))
            for i in range(2, len(commit_list)):
                if commit_list[i] != (commit_list[i-1] + commit_list[i-2]) % 10:
                    flag = False
                    break
            if flag:
                self.close()
                time_comsuming = int(self.time_label.text())
                QtWidgets.QMessageBox.information(
                    self, "正确", "恭喜你成功通过游戏,耗时{}秒".format(self.game_time-time_comsuming))
            else:
                QtWidgets.QMessageBox.information(self, "错误", "你的选择有误，请重新确认")
            print("commit_list", commit_list)

    def set_color(self, b):
        if b == self.num_buttoms[0]:
            return
        elif b.styleSheet() == "background-color: yellow" and b == self.num_buttoms[self.index[-1]]:
            b.setStyleSheet("background-color: white")
            self.index.pop()
        elif not b.styleSheet() == "background-color: yellow":
            bottom_selectable = False
            for i in self.next_selectable_b_index:
                if self.num_buttoms[i] == b:
                    bottom_selectable = True
                    self.index.append(i)
                    break
            if bottom_selectable:
                b.setStyleSheet("background-color: yellow")
        self.next_selectable_b_index = self._get_next_selectable_b_index()
        print("self.index", self.index)

    def _get_next_selectable_b_index(self):
        n = len(self.matrix)
        cur_index = self.index[-1]
        index = []
        if cur_index >= n:
            if not self.num_buttoms[cur_index-n].styleSheet() == "background-color: yellow":
                index.append(cur_index-n)
        if cur_index % n != n-1:
            if not self.num_buttoms[cur_index+1].styleSheet() == "background-color: yellow":
                index.append(cur_index+1)
        if cur_index < n*(n-1):
            if not self.num_buttoms[cur_index+n].styleSheet() == "background-color: yellow":
                index.append(cur_index+n)
        if cur_index % n != 0:
            if not self.num_buttoms[cur_index-1].styleSheet() == "background-color: yellow":
                index.append(cur_index-1)
        return index

    def _game_fail(self):
        self.game_num -= 1
        if self.game_num == 0:
            QtWidgets.QMessageBox.information(self, "游戏结果", "游戏时间超时。3次机会已使用完毕，游戏失败。")
        else:
            QtWidgets.QMessageBox.information(
                self, "提示", "游戏时间超时，你还有{}次机会，点击确认开始下一次机会".format(self.game_num))
            self.close_flag = False
        self.close()

    def closeEvent(self, QCloseEvent):
        if self.close_flag or self.game_num == 0:
            if self.game_num != 0:
                self.time_label.killTimer(self.time_label.time_id)
            self.main_close_signal.emit()
        else:
            self.main_regen_signal.emit(self.game_num)
        self.close()

class MyLabel(QtWidgets.QLabel):

    def __init__(self, *args, **kwargs):  # 这里是要传递参数的，这个表达是通用适配所有的类型
        super(MyLabel, self).__init__(*args, **kwargs)  # 先执行父类的方法
        self.setStyleSheet("font-size:72px")

    timeout_signal = QtCore.pyqtSignal()

    def set_sec(self, sec):
        self.setText(str(sec))

    def my_start_time(self, ms=1000):
        self.time_id = self.startTimer(ms)

    def timerEvent(self, QTimeEvent):
        cur_sec = int(self.text())
        cur_sec -= 1
        self.setText(str(cur_sec))
        if cur_sec == 0:
            self.killTimer(self.time_id)
            self.timeout_signal.emit()

