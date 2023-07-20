from ui.canshu_designed import Ui_canshu
from PyQt5 import QtWidgets
import matplotlib
from PyQt5 import QtCore

matplotlib.use('Qt5Agg')


class canshu(QtWidgets.QMainWindow, Ui_canshu):
    returnResultSignal = QtCore.pyqtSignal(list)

    def __init__(self, z, zr, opt, mode='r'):  # mode为w时需要把所有参数返回
        super().__init__()
        self.setupUi(self)
        self.widget1.setVisible(False)
        self.widget2.setVisible(False)
        self.pushButton_yiwei.clicked.connect(self.switch1)
        self.pushButton_jingxiang.clicked.connect(self.switch2)
        self.pushButton_yepian.clicked.connect(self.switch3)
        self.pushButton_confirm.clicked.connect(self.data_confirm)
        self.z = z
        self.zr = zr
        self.opt = opt
        self.mode = mode

    def data_confirm(self):
        ret = []
        if self.opt == 0:
            ret.append(float(self.lineEdit_Eff_26.text()))  # 静叶进口几何角 0
            ret.append(float(self.lineEdit_k_12.text()))  # 静叶出口几何角
            ret.append(float(self.lineEdit_omaga_16.text()))  # 静叶安装角
            ret.append(float(self.lineEdit_alph2z_24.text()))  # 静叶最大厚度
            ret.append(float(self.lineEdit_faiz_12.text()))  # 静叶前缘半径
            ret.append(float(self.lineEdit_taoz_12.text()))  # 静叶尾缘半径
            ret.append(float(self.lineEdit_Maz_25.text()))  # 静叶节距
            ret.append(float(self.lineEdit_alph2z_25.text()))  # 静叶叶片数
            ret.append(float(self.lineEdit_taoz_13.text()))  # 静叶叶宽 8
        else:
            ret.append(float(self.lineEdit_Eff_25.text()))  # 动叶进口几何角 0
            ret.append(float(self.lineEdit_k_11.text()))  # 动叶出口几何角
            ret.append(float(self.lineEdit_omaga_15.text()))  # 动叶安装角
            ret.append(float(self.lineEdit_alph2z_22.text()))  # 动叶最大厚度
            ret.append(float(self.lineEdit_faiz_11.text()))  # 动叶前缘半径
            ret.append(float(self.lineEdit_taoz_11.text()))  # 动叶尾缘半径
            ret.append(float(self.lineEdit_Maz_24.text()))  # 动叶节距
            ret.append(float(self.lineEdit_alph2z_23.text()))  # 动叶叶片数
            ret.append(float(self.lineEdit_taoz_14.text()))  # 动叶叶宽 8

        if self.mode == 'w':  # 加上一维设计和径向参数
            ret.append(int(self.lineEdit_Z_2.text()))  # 初始级数 9
            ret.append(float(self.lineEdit_Z.text()))  # 级进口总温
            ret.append(float(self.lineEdit_G_10.text()) * 1000)  # 级进口总压
            ret.append(float(self.lineEdit_Efft0_5.text()) * 1000)  # 级出口静压
            ret.append(float(self.lineEdit_Eff_14.text()))  # 反动度
            ret.append(float(self.lineEdit_pz_7.text()) / 1000)  # 静叶平均直径
            ret.append(float(self.lineEdit_Tt0_8.text()))  # 静叶进口气流角 15
            ret.append(float(self.lineEdit_pz_8.text()))  # 静叶出口气流角
            ret.append(float(self.lineEdit_Maz_14.text()))  # 静叶出口实际速度
            ret.append(float(self.lineEdit_n_5.text()))  # 静叶出口马赫数
            ret.append(float(self.lineEdit_omaga_10.text()))  # 静叶出口静温
            ret.append(float(self.lineEdit_xaz_10.text()) * 1000)  # 静叶出口静压
            ret.append(float(self.lineEdit_alph2z_14.text()) / 1000)  # 静叶出口叶高 21

            ret.append(float(self.lineEdit_Tt0_5.text()) / 1000)  # 动叶平均直径 22
            ret.append(float(self.lineEdit_G_9.text()))  # 动叶进口相对气流角
            ret.append(float(self.lineEdit_pz_5.text()))  # 动叶进口相对速度
            ret.append(float(self.lineEdit_Tt0_6.text()))  # 动叶进口相对马赫数
            ret.append(float(self.lineEdit_pz_6.text()))  # 动叶出口相对气流角
            ret.append(float(self.lineEdit_Efft0_4.text()))  # 动叶出口相对速度
            ret.append(float(self.lineEdit_Eff_13.text()))  # 动叶出口相对马赫数
            ret.append(float(self.lineEdit_Maz_13.text()))  # 动叶出口绝对气流角
            ret.append(float(self.lineEdit_n_4.text()) / 1000)  # 动叶出口叶高 30
            ret.append(float(self.lineEdit_omaga_9.text()) / 1000)  # 静叶中径处叶宽
            ret.append(float(self.lineEdit_xaz_9.text()) / 1000)  # 动叶中径处叶宽
            ret.append(float(self.lineEdit_alph2z_13.text()) / 1000)  # 轴向间隙
            ret.append(float(self.lineEdit_alph2z_15.text()) / 1000)  # 通流部分长度 34

            ret.append(float(self.lineEdit_G_12.text()))  # 静叶进口总温 35
            ret.append(float(self.lineEdit_Eff_19.text()) * 1000)  # 静叶进口总压
            ret.append(float(self.lineEdit_Eff_20.text()))  # 静叶进口气流角
            ret.append(float(self.lineEdit_Eff_17.text()))  # 静叶出口绝对速度
            ret.append(float(self.lineEdit_Maz_17.text()))  # 静叶出口气流角
            ret.append(float(self.lineEdit_k_8.text()))  # 静叶出口马赫数 40
            ret.append(float(self.lineEdit_R_8.text()))  # 静叶出口静温
            ret.append(float(self.lineEdit_omaga_12.text()) * 1000)  # 静叶出口静压
            ret.append(float(self.lineEdit_xaz_12.text()))  # 动叶进口相对气流角 43

            ret.append(float(self.lineEdit_Eff_18.text()))  # 动叶进口相对速度 44
            ret.append(float(self.lineEdit_faiz_8.text()))  # 动叶进口相对马赫数
            ret.append(float(self.lineEdit_rouz_8.text()))  # 动叶出口相对速度
            ret.append(float(self.lineEdit_taoz_8.text()))  # 动叶出口气流角
            ret.append(float(self.lineEdit_fRz_z_8.text()))  # 动叶出口相对马赫数
            ret.append(float(self.lineEdit_Maz_18.text()))  # 动叶出口静温
            ret.append(float(self.lineEdit_pt0_8.text()) * 1000)  # 动叶出口静压 50
            ret.append(float(self.lineEdit_alph2z_18.text()))  # 反动度 51

        ret.append(self.z)
        ret.append(self.zr)
        ret.append(self.opt)
        self.returnResultSignal.emit(ret)
        # if self.mode == 'w':
        #     self.setVisible(False)
        # else:
        self.close()

    def switch1(self):
        self.widget.setVisible(True)
        self.widget1.setVisible(False)
        self.widget2.setVisible(False)

    def switch2(self):
        self.widget1.setVisible(True)
        self.widget.setVisible(False)
        self.widget2.setVisible(False)

    def switch3(self):
        self.widget2.setVisible(True)
        self.widget1.setVisible(False)
        self.widget.setVisible(False)
        if self.opt == 0:
            self.widget_dong.setVisible(False)
            self.widget_jing.setVisible(True)
        else:
            self.widget_dong.setVisible(True)
            self.widget_jing.setVisible(False)
