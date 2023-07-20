import numpy as np
from numpy.linalg import norm
from matplotlib import pyplot as plt
from shapely.geometry import LineString

# global plot to be used
fig, ax = plt.subplots()
sc = 0


# Transform data inside re_p.txt and re_s.txt into curve in numPy array
# def txt2curve(file_name):
#     curve = []
#     with open(file_name) as data:
#         while True:
#             dataline = data.readline()
#             if not dataline:
#                 break
#             row = dataline.split(" ")
#             point = []
#             for string in row:
#                 point.append(float(string.split("\n")[0]))
#             curve.append(point)
#     return np.array(curve)


# Print the turbine curve of type NumPy array with two rows.
# def print_curve():
#     ax.plot(re_p[:, 0], re_p[:, 1])
#     ax.plot(re_s[:, 0], re_s[:, 1])
#     plt.show()
#     return


# Normalize a vector.
def normalize(v):
    return v / norm(v)


# Get the normal vector of each point on the curve.
def get_normal(curve):
    global sc
    normals = [None]
    n = len(curve)
    for i in range(1, n - 1):
        next = normalize(curve[i + 1] - curve[i])
        last = normalize(curve[i] - curve[i - 1])
        if norm(next - last) < 0.001 * sc:
            vec = np.zeros(2)
            vec[0] = next[1]
            vec[1] = -next[0]
        else:
            vec = next - last
        vec = normalize(vec)
        normals.append(vec)
    normals[0] = normals[1]
    normals.append(normals[n - 2])
    return np.array(normals)


# Print one of the turbine curves and its steps of offset. For test only.
# def print_step():
#     ax.plot(re_p[:, 0], re_p[:, 1], 'b')
#     ax.plot(re_s[:, 0], re_s[:, 1], 'r')
#     one_step = re_p + get_dir_normal(re_p, re_s) * 3 * ref_scale(re_p)
#     ax.plot(one_step[:, 0], one_step[:, 1], 'g')
#     one_step = re_s + get_dir_normal(re_s, re_p) * 3 * ref_scale(re_s)
#     ax.plot(one_step[:, 0], one_step[:, 1], 'y')
#     plt.show()
#     return


# Determine the "scale" of the curve; being referred by the offset step length, etc.
def ref_scale(curve):
    sum = 0
    for i in range(1, len(curve)):
        sum += norm(curve[i] - curve[i - 1])
    sum /= len(curve)
    return sum


# ref_p exists:
# Check if the vector is pointing "towards" the curve or "away from" the curve: v1 is the point and v2 is the normal
# towards: return 1
# away: return -1
# ref_p is None:
# Check if two vectors are pointing in the same direction. Same: return 1, different: return -1
def check_direction(v1, v2, ref_p=None):
    if ref_p is None:
        if v1.dot(v2) > 0:
            return 1
        else:
            return -1
    else:
        if np.dot(v2, ref_p - v1) > 0:
            return 1
        return -1


# Get normal vectors on a curve with direction always pointing towards the reference curve.
def get_dir_normal(vec, ref, first=False):
    normals = get_normal(vec)
    n = len(vec)
    m = len(ref)
    for i in range(1, n - 1):
        if first:
            # This means that the normal needs to be checked wrt difference between current curve and reference curve
            normals[i] *= check_direction(vec[i], normals[i], ref[int(i * m / n)])
        else:
            # This means that the normal needs to be checked wrt initial normal
            normals[i] *= check_direction(normals[i], ref[int(i * m / n)])
    normals[0] = normals[1]
    normals[n - 1] = normals[n - 2]
    return normals


def dynamic_step(i, curve):
    global sc
    return (0.1 + (1 - np.exp(-0.1 * i)) * 0.1) * sc


# Refactor the curve so that it does not turn into weird shapes
def refactor(curve):
    n = len(curve)
    for i in range(int(n / 2), 0, -1):
        left = curve[i - 1] - curve[i]
        right = curve[i + 1] - curve[i]
        if left.dot(right) > 0.0001 * sc:
            for j in range(i + 1, 0, -1):
                curve[j - 1] = 2 * curve[j] - curve[j + 1]
            break
    for i in range(int(n / 2) + 1, n - 1):
        left = curve[i - 1] - curve[i]
        right = curve[i + 1] - curve[i]
        if left.dot(right) > 0.0001 * sc:
            for j in range(i - 1, n - 1):
                curve[j + 1] = 2 * curve[j] - curve[j - 1]
            break
    return curve


def sort_fn(item):
    return item[1]


def meanline_sort(curve, end_point):
    start_point = np.array([0.0, 0.0])
    ref_point = (np.array(start_point) + np.array(end_point)) / 2
    points_w_angle = []
    points = []
    for point in curve:
        u = point - ref_point
        v = start_point - ref_point
        dot_product = u.dot(v) / (norm(u) * norm(v))

        # 检查点积是否在有效范围内
        if -1 <= dot_product <= 1:
            angle = np.arccos(dot_product)
        else:
            # 当点积超出有效范围时的处理
            angle = 0.0  # 提供一个默认值或根据需求进行处理

        points_w_angle.append([point, angle])
    points_w_angle_sorted = sorted(points_w_angle, key=sort_fn)
    for point in points_w_angle_sorted:
        points.append(point[0])
    points = np.array(points)
    return points


# Calculate meanline between two curves.
def meanline_calc(init_c1, init_c2, steps=200):
    n = len(init_c1)
    # ax.plot(init_c1[:, 0], init_c1[:, 1], 'b')
    # ax.plot(init_c2[:, 0], init_c2[:, 1], 'b')
    c1 = init_c1  # c1: current upper curve
    c2 = init_c2  # c2: current lower curve
    init_n1 = []  # normal of initial curve
    init_n2 = []
    points = []
    end_point = []
    cross_line1 = []
    cross_line2 = []
    for i in range(steps):
        # Check intersection first
        string1 = LineString(c1)
        string2 = LineString(c2)
        # inter = intersection(string1, string2)
        inter = string1.intersection(string2)
        # Plot intersection points
        if inter.geom_type == "Point":
            points.append([inter.x, inter.y])
            ax.plot(inter.x, inter.y, 'b.')
            if not end_point or norm(end_point) < sc:
                end_point = [inter.x, inter.y]
        elif inter.geom_type == "MultiPoint":
            '''xs = [point.x for point in inter.geoms]
            ys = [point.y for point in inter.geoms]
            ax.plot(xs, ys, 'b.')'''
            pts = [[point.x, point.y] for point in inter.geoms]
            for pt in pts:
                points.append(pt)
                if not end_point or norm(end_point) < sc:
                    end_point = pt
        # Now, update the curves
        if i == 0:
            n1 = get_dir_normal(init_c1, init_c2, True)
            init_n1 = n1
            n2 = get_dir_normal(init_c2, init_c1, True)
            init_n2 = n2
        else:
            n1 = get_dir_normal(c1, init_n1)
            n2 = get_dir_normal(c2, init_n2)
        c1 = c1 + dynamic_step(i, init_c1) * n1
        c2 = c2 + dynamic_step(i, init_c1) * n2
        c1 = refactor(c1)
        c2 = refactor(c2)
        if i % 5 == 0:
            cross_line1.append(c1)
            cross_line2.append(c2)
            # ax.plot(c1[:, 0], c1[:, 1], 'r')
            # ax.plot(c2[:, 0], c2[:, 1], 'g')
    points = np.array(points)
    # ax.plot(points[:, 0], points[:, 1], 'b.')
    points = meanline_sort(points, end_point)
    ax.plot(points[:, 0], points[:, 1], 'r')
    plt.show()
    return points, cross_line1, cross_line2


num = 0


def meanline(re_p, re_s):
    global sc
    # print('asdfasdfasdf')
    # print(re_p)
    # print(re_s)
    global num
    num = num + 1
    fig_name = f'{num}'
    fig = plt.figure(fig_name)
    ax = fig.add_subplot(1, 1, 1)

    re_p_len = len(re_p)
    re_s_len = len(re_s)
    # re_p = re_p[int(0.1 * re_p_len):int(0.9 * re_p_len)]
    # re_s = re_s[int(0.1 * re_s_len):int(0.9 * re_s_len)]

    sc = ref_scale(re_p)
    m, crossline1, crossline2 = meanline_calc(re_p[int(0.15 * re_p_len):int(0.85 * re_p_len)],
                                              re_s[int(0.15 * re_s_len):int(0.85 * re_s_len)])
    # m, crossline1, crossline2 = meanline_calc(re_p, re_s)

    ax.plot(re_p[:, 0], re_p[:, 1], color='blue')
    ax.plot(re_s[:, 0], re_s[:, 1], color='blue')
    ax.plot(m[:, 0], m[:, 1], color='red')
    # for o in (0, 20):
    #     ax.plot(crossline2[o][:, 0], crossline2[o][:, 1])
    #     ax.plot(crossline1[o][:, 0], crossline1[o][:, 1])
    plt.show()

    return m

# re_p = txt2curve("../re_p.txt")
# re_s = txt2curve("../re_s.txt")
# sc = ref_scale(re_p)
# meanline_calc(re_p, re_s)
