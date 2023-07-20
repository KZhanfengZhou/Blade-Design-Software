# Author: Wang tianyi
# github: https://github.com/tian1wang

import sys
from PyQt5.QtWidgets import QApplication
from ui import beginWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = beginWindow.beginWindow()
    ui.show()
    sys.exit(app.exec_())

# pyinstaller -F -w -i C:\Users\13270\PycharmProjects\blade_design_sco2\ui\source\favicon.ico C:\Users\13270\PycharmProjects\blade_design_sco2\show_my_window.py

# 二分中弧线算法需要判断和本线相交01

# 分析算法 怎么继承原来的输入
# 凹侧好像有问题，偏置线出错

# 控制点个数可调，需要配好初始值

# 厚度分布的方向判定也有问题,需要改 而且用偏置线法好像不太合适
# 中弧线前段会出现小波动。
