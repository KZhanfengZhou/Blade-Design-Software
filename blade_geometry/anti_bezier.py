# 并没有使用此文件，因为准备改成b样条

import numpy as np
import matplotlib.pyplot as plt
from bezier import Curve


def upbezier(array):
    P = array

    # 升阶后的控制点个数
    n = P.shape[0] + 1

    # 创建新的控制点矩阵Q
    Q = np.zeros((n, 2))
    Q[0] = P[0]
    Q[n - 1] = P[-1]

    # 计算中间控制点
    for i in range(1, n - 1):
        Q[i] = (i / n) * P[i - 1] + ((n - i) / n) * P[i - 1]

    t = np.linspace(0, 1, 100)
    B = np.zeros((len(t), 2))
    for i in range(len(t)):
        for j in range(n):
            B[i] = B[i] + Q[j] * np.math.factorial(n - 1) / (np.math.factorial(j) * np.math.factorial(n - j - 1)) * t[
                i] ** j * (1 - t[i]) ** (n - j - 1)

    return B


#
# def casteljau(points, t):
#     """
#     递归地计算 t 时刻的点位
#     """
#     if len(points) == 1:
#         return points[0]
#     else:
#         new_points = []
#         for i in range(len(points) - 1):
#             x = (1 - t) * points[i][0] + t * points[i + 1][0]
#             y = (1 - t) * points[i][1] + t * points[i + 1][1]
#             new_points.append((x, y))
#         return casteljau(new_points, t)
#
#
# def downbezier(points, degree):
#     """
#     将给定的贝塞尔曲线的阶降低到 degree
#     """
#     while len(points) > degree + 1:
#         # 从最后一段开始
#         for i in range(len(points) - 1, 0, -1):
#             # 计算中间节点
#             x = 0.5 * (points[i - 1][0] + points[i][0])
#             y = 0.5 * (points[i - 1][1] + points[i][1])
#             mid_point = (x, y)
#
#             # 更新点集
#             points[i] = mid_point
#         # 移除最后一个点
#         points = np.delete()
#     return points


def downbezier(array):
    P = array

    # 降阶后的控制点个数
    n = P.shape[0] - 1

    # degree = len(array) - 1
    # curve = Curve(array, degree=degree)
    #
    # # 将曲线划分为两部分，即在 t = 0.5 的位置上断开
    # t = 0.5
    # left_nodes, right_nodes = curve.subdivide(t)
    #
    # # 可以检查左半部分是否为更低的阶数
    # left_curve = Curve(left_nodes, degree=degree - 1)
    # Q = np.array(left_curve.nodes)
    # 创建新的控制点矩阵Q
    Q = np.zeros((n, 2))

    # 计算新的控制点
    for i in range(n):
        Q[i] = (i + 1) / (n + 1) * P[i] + (n - i) / (n + 1) * P[i + 1]

    # 绘制原始贝塞尔曲线
    t = np.linspace(0, 1, 100)
    B = np.zeros((len(t), 2))
    for i in range(len(t)):
        for j in range(n):
            B[i] = B[i] + Q[j] * np.math.factorial(n) / (np.math.factorial(j) * np.math.factorial(n - j)) * t[
                i] ** j * (1 - t[i]) ** (n - j)
    return B


def de_casteljau(points, t):
    """
    计算de Casteljau算法的贝塞尔曲线上的点
    :param points: 控制点列表，每个控制点应该是一个numpy数组
    :param t: 参数值（0 <= t <= 1）
    :return: 贝塞尔曲线上的点，作为一个numpy数组返回
    """
    n = len(points)
    b = np.copy(points)
    for r in range(1, n):
        for i in range(n - r):
            b[i] = (1 - t) * b[i] + t * b[i + 1]
    return b[0]


#
# p0 = np.array([0., 0.])
# p1 = np.array([1., 3.])
# p2 = np.array([4., 0.])
# p3 = np.array([5., 5.])
# points = [p0, p1, p2, p3]


def bezier(points, n_points):  # 计算贝塞尔曲线上的点
    t_values = np.linspace(0, 1, n_points)
    curve_points = np.array([de_casteljau(points, t) for t in t_values])
    #
    # 绘制贝塞尔曲线和控制点

    return curve_points

# # curve_points = bezier(points, 50)
# curve_points = downbezier(np.array(points))
# print(curve_points)
# x, y = curve_points.T
# plt.plot(x, y, label='Bezier Curve')
# x, y = np.array(points).T
# plt.scatter(x, y, label='Control Points')
# plt.legend()
# plt.show()
