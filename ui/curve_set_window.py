import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QSpinBox, \
    QPushButton, QLineEdit
import numpy as np


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.setWindowTitle("造型曲线设置")
        self.parent = parent  # 保存父窗口的引用
        self.setup_ui()
        self.on_curve_changed("贝塞尔曲线")

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)

        # 构型曲线下拉栏
        curve_label = QLabel("构型曲线:")
        self.curve_combo = QComboBox()
        self.curve_combo.addItem("贝塞尔曲线")
        self.curve_combo.addItem("B样条曲线")
        self.curve_combo.currentTextChanged.connect(self.on_curve_changed)

        # 参数输入框
        self.param1_label = QLabel("叶背曲线中段控制点数量:")
        self.param1_spinbox = QSpinBox()
        self.param1_spinbox.setValue(6)
        self.param1_spinbox.textChanged.connect(self.on_num_changed)

        self.param2_label = QLabel("叶盆曲线中段控制点数量:")
        self.param2_spinbox = QSpinBox()
        self.param2_spinbox.setValue(5)
        self.param2_spinbox.textChanged.connect(self.on_num_changed)

        self.param3_label = QLabel("叶背曲线节点向量:")
        self.param3_edit = QLineEdit()

        self.param4_label = QLabel("叶盆曲线节点向量:")
        self.param4_edit = QLineEdit()

        # 确定按钮
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.on_ok_clicked)

        layout.addWidget(curve_label)
        layout.addWidget(self.curve_combo)
        layout.addSpacing(10)
        layout.addWidget(self.param1_label)
        layout.addWidget(self.param1_spinbox)
        layout.addWidget(self.param2_label)
        layout.addWidget(self.param2_spinbox)
        layout.addWidget(self.param3_label)
        layout.addWidget(self.param3_edit)
        layout.addWidget(self.param4_label)
        layout.addWidget(self.param4_edit)
        layout.addSpacing(20)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def get_node_vec(self, num):
        n = num + 3
        k = 3
        nV = np.zeros(n + k + 2)
        for i in range(k + 1):
            nV[i] = 0
            nV[n + k + 1 - i] = 1
        for i in range(k + 1, n + 1):
            nV[i] = nV[i - 1] + 1 / (n - k + 1)
        vec = ''
        for i in range(len(nV) - 1):
            vec = vec + str(nV[i]) + ' '
        vec = vec + str(nV[len(nV) - 1])
        return vec

    def on_num_changed(self, num):
        if self.curve_combo.currentText() == '贝塞尔曲线':
            return
        else:
            self.param3_edit.setText(self.get_node_vec(int(self.param1_spinbox.value())))
            self.param4_edit.setText(self.get_node_vec(int(self.param2_spinbox.value())))

    def on_curve_changed(self, curve_type):
        if curve_type == "贝塞尔曲线":
            self.param3_label.hide()
            self.param3_edit.hide()
            self.param4_label.hide()
            self.param4_edit.hide()
        else:
            self.param3_edit.setText(self.get_node_vec(int(self.param1_spinbox.value())))
            self.param4_edit.setText(self.get_node_vec(int(self.param2_spinbox.value())))
            self.param3_label.show()
            self.param3_edit.show()
            self.param4_label.show()
            self.param4_edit.show()

    def on_ok_clicked(self):
        curve_type = 1 if self.curve_combo.currentText() == '贝塞尔曲线' else 2

        param1 = int(self.param1_spinbox.value())
        param2 = int(self.param2_spinbox.value())
        if curve_type == 1:
            self.parent.on_settings_changed(curve_type, param1, param2)
        else:
            param3 = [float(x) for x in self.param3_edit.text().split(' ')]
            param4 = [float(x) for x in self.param4_edit.text().split(' ')]
            # 将参数传递给主窗口的槽函数
            self.parent.on_settings_changed(curve_type, param1, param2, param3, param4)
        # curve 1:贝塞尔曲线 2:B样条曲线
        self.accept()
