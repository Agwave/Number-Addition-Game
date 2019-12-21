import copy
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from objects.generate_matrix import Matrix

class MainWindow(QtWidgets.QWidget):

    def __init__(self, m):
        super().__init__()
        self.matrix = m.matrix
        self.load = m.load
        self.initUI()

    main_close_signal = QtCore.pyqtSignal()

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
                QtWidgets.QMessageBox.information(self, "正确", "恭喜你成功通过游戏")
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
        if cur_index <= n*(n-1):
            if not self.num_buttoms[cur_index+n].styleSheet() == "background-color: yellow":
                index.append(cur_index+n)
        if cur_index % n != 0:
            if not self.num_buttoms[cur_index-1].styleSheet() == "background-color: yellow":
                index.append(cur_index-1)
        return index

    def closeEvent(self, QCloseEvent):
        reply = QtWidgets.QMessageBox.question(self,
                                               '退出',
                                               "是否要返回初始界面？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.main_close_signal.emit()
        else:
            QCloseEvent.ignore()


if __name__ == '__main__':
    m = Matrix(4)
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow(m)
    sys.exit(app.exec_())