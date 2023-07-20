import math

from ui.chushi_designed import Ui_chushi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
import numpy as np
import matplotlib
from blade_geometry import Bias_line

matplotlib.use('Qt5Agg')

from blade_geometry import figure_operation, camber_operation, file_operation, calcu
from design_calculation import data_list

from ui import main_leaf
from ui import newwindow
from ui import gongkuang
from ui import canshu
import matplotlib.pyplot as plt

import time


class beginWindow(QtWidgets.QMainWindow, Ui_chushi):
    """
    初始窗口"""
    main = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.pushButton.clicked.connect(self.close)
        self.pushButton_new.clicked.connect(self.analyse_start)
        self.pushButton_new_2.clicked.connect(self.design_start)
        self.pushButton_read.clicked.connect(self.openFile)
        self.pushButton_open.clicked.connect(self.open)

    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, caption='打开文件', directory='./', filter='ALL(*.*);;TEXT(*.txt)',
                                            initialFilter='TEXT(*.txt)')
        if fname[0] != '':
            camber, pp, ps, opt = file_operation.txtinput(str(fname[0]))
            if opt is False:  # 这里直接对ppps赋值，进入主界面后依然会被覆盖
                camber_operation.control_point = camber
                self.main = main_leaf.blade_designer(1, None, pp, ps)
            else:
                data_list.Z_num = opt[0]
                data_list.Zr = opt[1]
                camber_operation.control_point = camber[0][0][0][0]
                figure_operation.TE_radius = camber[0][0][0][2][1]
                figure_operation.blade_dis = camber[0][0][0][3]
                figure_operation.lim = camber[0][0][0][0][2, 0] / 20  # 最后一个控制点的x轴就是叶片宽度
                camber_operation.lim = camber[0][0][0][0][2, 0] / 20
                self.main = main_leaf.blade_designer(2, camber, pp, ps)

            self.setVisible(False)  # 隐藏主界面
            self.main.setVisible(True)

    def analyse_start(self):
        fname = QFileDialog.getOpenFileName(self, caption='打开文件', directory='./', filter='TEXT(*.txt)')

        if fname[0] != '':
            # 这里要把叶片的级数 计算站数提取出来，并且读取叶片信息。
            self.z, self.zr, self.n, self.re_p, self.re_s = file_operation.analyse_input(str(fname[0]))
            self.init_array()
            # 在这里计算几何参数并填入
            for i in range(self.z):
                for j in range(2):
                    for k in range(self.zr):
                        rep = np.array(self.re_p[(i * 2 + j) * self.zr + k])
                        res = np.array(self.re_s[(i * 2 + j) * self.zr + k])
                        xp = rep[:, 2]
                        yp = rep[:, 1]
                        rep = np.column_stack((xp, yp))
                        xs = res[:, 2]
                        ys = res[:, 1]
                        res = np.column_stack((xs, ys))
                        # meanline = calcu.offset_meanline(rep, res)
                        meanline = Bias_line.meanline(rep, res)

                        # fig = plt.figure(f'{(i * 2 + j) * self.zr + k}')
                        # ax = fig.add_subplot(1, 1, 1)
                        # ax.plot(rep[:, 0], rep[:, 1])
                        # ax.plot(res[:, 0], res[:, 1])
                        # plt.plot(meanline[:, 0], meanline[:, 1])
                        plt.show()

                        if j == 0:
                            data_list.Stator_Beta1_g[i][k] = 90 - math.atan(
                                (meanline[2, 1] - rep[0, 1]) / (meanline[2, 0] - rep[0, 0])) / math.pi * 180  # 静叶进口几何角
                            data_list.Stator_Beta2_g[i][k] = 90 + math.atan(
                                (meanline[-3, 1] - rep[-1, 1]) / (
                                        meanline[-3, 0] - rep[-1, 0])) / math.pi * 180  # 静叶出口几何角
                            print(data_list.Stator_Beta1_g[i][k])
                            print(data_list.Stator_Beta2_g[i][k])
                            data_list.Stator_Gamma[i][k] = math.atan(
                                math.fabs(rep[0, 0] - rep[-1, 0]) / math.fabs(
                                    rep[0, 1] - rep[-1, 1])) / math.pi * 180  # 静叶安装角

                            # data_list.Stator_Cmax[i][k] = result[3] / 1000  # 静叶最大厚度
                            data_list.Stator_r1[i][k] = math.fabs((math.atan(
                                (rep[1, 1] - rep[0, 1]) / (rep[1, 0] - rep[0, 0])) - math.atan(
                                (res[0, 1] - res[1, 1]) / (res[0, 0] - res[1, 0]))) / (math.sqrt(
                                (rep[1, 0] - rep[0, 0]) ** 2 + (rep[1, 1] - rep[1, 0]) ** 2)))  # 静叶前缘半径
                            data_list.Stator_r2[i][k] = math.fabs((math.atan(
                                (rep[-2, 1] - rep[-1, 1]) / (rep[-2, 0] - rep[-1, 0])) - math.atan(
                                (res[-1, 1] - res[-2, 1]) / (res[-1, 0] - res[-2, 0]))) / (math.sqrt(
                                (rep[-2, 0] - rep[-1, 0]) ** 2 + (rep[-2, 1] - rep[-1, 0]) ** 2)))  # 静叶尾缘半径
                            data_list.Stator_t[i][k] = math.pi * 2 * self.re_p[(i * 2 + j) * self.zr][0][0] / self.n[
                                i * 2 + j]  # 静叶节距
                            data_list.Stator_z[i][k] = self.n[i * 2 + j]  # 静叶叶片数
                            data_list.Stator_B[i][k] = math.fabs(rep[0, 0] - rep[-1, 0])  # 静叶叶宽
                        else:
                            data_list.Rotor_Beta1_g[i][k] = 90 - math.atan(
                                (meanline[2, 1] - rep[0, 1]) / (meanline[2, 0] - rep[0, 0])) / math.pi * 180  # 动叶进口几何角
                            data_list.Rotor_Beta2_g[i][k] = 90 + math.atan(
                                (meanline[-3, 1] - rep[-1, 1]) / (
                                        meanline[-3, 0] - rep[-1, 0])) / math.pi * 180  # 动叶出口几何角
                            print(data_list.Rotor_Beta1_g[i][k])
                            print(data_list.Rotor_Beta2_g[i][k])
                            data_list.Rotor_Gamma[i][k] = math.atan(
                                math.fabs(rep[0, 0] - rep[-1, 0]) / math.fabs(
                                    rep[0, 1] - rep[-1, 1])) / math.pi * 180  # 动叶安装角
                            # data_list.Rotor_Cmax[i][k] = result[3] / 1000  # 动叶最大厚度
                            data_list.Rotor_r1[i][k] = math.fabs((math.atan(
                                (rep[1, 1] - rep[0, 1]) / (rep[1, 0] - rep[0, 0])) - math.atan(
                                (res[0, 1] - res[1, 1]) / (res[0, 0] - res[1, 0]))) / (math.sqrt(
                                (rep[1, 0] - rep[0, 0]) ** 2 + (rep[1, 1] - rep[1, 0]) ** 2)))  # 动叶前缘半径
                            data_list.Rotor_r2[i][k] = math.fabs((math.atan(
                                (rep[-2, 1] - rep[-1, 1]) / (rep[-2, 0] - rep[-1, 0])) - math.atan(
                                (res[-1, 1] - res[-2, 1]) / (res[-1, 0] - res[-2, 0]))) / (math.sqrt(
                                (rep[-2, 0] - rep[-1, 0]) ** 2 + (rep[-2, 1] - rep[-1, 0]) ** 2)))  # 动叶尾缘半径
                            data_list.Rotor_t[i][k] = math.pi * 2 * self.re_p[(i * 2 + j) * self.zr][0][0] / self.n[
                                i * 2 + j]  # 动叶节距
                            data_list.Rotor_z[i][k] = self.n[i * 2 + j]  # 动叶叶片数
                            data_list.Rotor_B[i][k] = math.fabs(rep[0, 0] - rep[-1, 0])  # 动叶叶宽

            self.z_now = 0
            self.zr_now = 0
            self.opt_now = 0
            self.data_window = canshu.canshu(self.z_now, self.zr_now, self.opt_now, 'w')
            self.data_window.pushButton_yepian.setEnabled(False)
            # tmp = '静叶' if self.opt_now == 0 else '动叶'
            tmp = f'当前参数为第{self.z_now + 1}级' + f'第{self.zr_now + 1}计算站'
            self.data_window.label.setText(tmp)
            self.data_window.returnResultSignal.connect(self.handle_data_window_result)
            self.data_window.show()

    def init_array(self):
        data_list.Z_num = self.z
        data_list.Zr = self.zr
        data_list.One_dimension_init(self.z)
        data_list.used_radial_and_geom_data_init(self.z, self.zr)

    def handle_data_window_result(self, result):
        z = result[-3]
        zr = result[-2]
        opt = result[-1]
        # if opt == 0:
        #     data_list.Stator_Beta1_g[z][zr] = result[0]  # 静叶进口几何角
        #     data_list.Stator_Beta2_g[z][zr] = result[1]  # 静叶出口几何角
        #     data_list.Stator_Gamma[z][zr] = result[2]  # 静叶安装角
        #     data_list.Stator_Cmax[z][zr] = result[3] / 1000  # 静叶最大厚度
        #     data_list.Stator_r1[z][zr] = result[4] / 1000  # 静叶前缘半径
        #     data_list.Stator_r2[z][zr] = result[5] / 1000  # 静叶尾缘半径
        #     data_list.Stator_t[z][zr] = result[6] / 1000  # 静叶节距
        #     data_list.Stator_z[z][zr] = result[7]  # 静叶叶片数
        #     data_list.Stator_B[z][zr] = result[8] / 1000  # 静叶叶宽
        # else:
        #     data_list.Rotor_Beta1_g[z][zr] = result[0]  # 动叶进口几何角
        #     data_list.Rotor_Beta2_g[z][zr] = result[1]  # 动叶出口几何角
        #     data_list.Rotor_Gamma[z][zr] = result[2]  # 动叶安装角
        #     data_list.Rotor_Cmax[z][zr] = result[3] / 1000  # 动叶最大厚度
        #     data_list.Rotor_r1[z][zr] = result[4] / 1000  # 动叶前缘半径
        #     data_list.Rotor_r2[z][zr] = result[5] / 1000  # 动叶尾缘半径
        #     data_list.Rotor_t[z][zr] = result[6] / 1000  # 动叶节距
        #     data_list.Rotor_z[z][zr] = result[7]  # 动叶叶片数
        #     data_list.Rotor_B[z][zr] = result[8] / 1000  # 动叶叶宽

        if z == 0 and zr == 0 and opt == 0:  # 一维设计只要取一次
            # data_list.Z_num = result[9]  # 初始级数
            data_list.Tt0M[z] = result[10]  # 级进口总温
            data_list.pt0M[z] = result[11]  # 级进口总压
            data_list.p2M[z] = result[12]  # 级出口静压
            data_list.omagaM[z] = result[13]  # 反动度
            data_list.Dm1M[z] = result[14]  # 静叶平均直径
            data_list.alph0M[z] = result[15]  # 静叶进口气流角
            data_list.alph1M[z] = result[16]  # 静叶出口气流角
            data_list.c1M[z] = result[17]  # 静叶出口实际速度
            data_list.Lamda1M[z] = result[18]  # 静叶出口马赫数
            data_list.T1_mixM[z] = result[19]  # 静叶出口静温
            data_list.p1M[z] = result[20]  # 静叶出口静压
            data_list.l1M[z] = result[21]  # 静叶出口叶高

            data_list.Dm2M[z] = result[22]  # 动叶平均直径
            data_list.Beta1M[z] = result[23]  # 动叶进口相对气流角
            data_list.w1M[z] = result[24]  # 动叶进口相对速度
            data_list.Lamda11M[z] = result[25]  # 动叶进口相对马赫数
            data_list.Beta2M[z] = result[26]  # 动叶出口相对气流角
            data_list.w2M[z] = result[27]  # 动叶出口相对速度
            data_list.Lamda12M[z] = result[28]  # 动叶出口相对马赫数
            data_list.alph12M[z] = result[29]  # 动叶出口绝对气流角
            data_list.l2M[z] = result[30]  # 动叶出口叶高
            data_list.Bz1M[z] = result[31]  # 静叶中径处叶宽
            data_list.Bz2M[z] = result[32]  # 动叶中径处叶宽
            data_list.ACM[z] = result[33]  # 轴向间隙
            data_list.LM[z] = result[34]  # 通流部分长度

        # data_list.Tt0M[z] = result[35]  # 静叶进口总温
        # data_list.pt0M[z] = result[36]  # 静叶进口总压
        # self.data_window.lineEdit_Eff_20.setText('90')  # 静叶进口气流角
        data_list.c1i[z][zr] = result[38]  # 静叶出口绝对速度
        data_list.alpha1i[z][zr] = result[39]  # 静叶出口气流角
        data_list.Lambda1i[z][zr] = result[40]  # 静叶出口马赫数
        data_list.T1i[z][zr] = result[41]  # 静叶出口静温
        data_list.p1i[z][zr] = result[42]  # 静叶出口静压
        data_list.Beta1i[z][zr] = result[43]  # 动叶进口相对气流角

        data_list.w1i[z][zr] = result[44]  # 动叶进口相对速度
        data_list.Ma_w1i[z][zr] = result[45]  # 动叶进口相对马赫数
        data_list.w2i[z][zr] = result[46]  # 动叶出口相对速度
        data_list.Beta2i[z][zr] = result[47]  # 动叶出口气流角
        data_list.RLambda2i[z][zr] = result[48]  # 动叶出口相对马赫数
        data_list.T2i[z][zr] = result[49]  # 动叶出口静温
        data_list.p2i[z][zr] = result[50]  # 动叶出口静压
        data_list.Radial_omega[z][zr] = result[51]  # 反动度

        self.zr_now = self.zr_now + 1
        if self.zr_now == self.zr:
            self.zr_now = 0
            # self.opt_now = self.opt_now + 1
            # if self.opt_now == 2:
            #     self.opt_now = 0
            self.z_now = self.z_now + 1
        if self.z_now != self.z:
            self.data_window = canshu.canshu(self.z_now, self.zr_now, self.opt_now, 'w')
            self.data_window.pushButton_yepian.setEnabled(False)
            # tmp = '静叶' if self.opt_now == 0 else '动叶'
            tmp = f'当前参数为第{self.z_now + 1}级' + f'第{self.zr_now + 1}计算站'
            self.data_window.label.setText(tmp)
            self.data_window.z = self.z_now
            self.data_window.zr = self.zr_now
            self.data_window.opt = self.opt_now
            self.data_window.returnResultSignal.connect(self.handle_data_window_result)
            self.data_window.show()
            # self.data_window.setVisible(True)
        else:
            self.main = main_leaf.blade_designer(3)
            self.setVisible(False)  # 隐藏主界面
            self.main.setVisible(True)

    def design_start(self):
        self.main = gongkuang.gongkuang()
        self.setVisible(False)  # 隐藏主界面
        self.main.setVisible(True)

    def open(self):
        camber = np.array([[1.97803159, 1.53044833], [11.34468, -0.899818], [14.4335762, -9.90096959]])
        pp = np.array(
            [[1.97803159, 1.53044833], [2.28734559, 2.71255756], [5.97517806, 5.94936882], [9.42264596, 6.49978646],
             [10.50168597, 2.47052067], [12.5460801, 0.57288884], [12.80091383, -2.83838773],
             [13.62560187, -5.24045493], [13.85311348, -7.73692925], [14.47831949, -9.80933095]])
        ps = np.array(
            [[1.97803159, 1.53044833], [1.66871759, 0.3483391], [3.79754413, -0.75141551], [6.45725958, -0.69525079],
             [9.06433283, -1.33214082], [10.81007736, -3.24439291], [12.10524057, -5.45044471],
             [13.62782363, -7.48984497], [14.34180203, -9.85650496]])
        camber_operation.control_point = camber
        figure_operation.pp = pp
        figure_operation.ps = ps
        self.main = main_leaf.blade_designer(1)
        self.setVisible(False)  # 隐藏主界面
        self.main.setVisible(True)
