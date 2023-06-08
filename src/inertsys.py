import csv
import numpy as np
import math
import pygame
from scipy import integrate
from scipy.misc import derivative
import matplotlib.pyplot as plt
import time
from pykalman import KalmanFilter
from scipy.signal import savgol_filter
# WIN = pygame.display.set_mode((2340, 780))
# COLOR = (200, 200, 200)

freq = 1/30 #Hz

# def draw_window(x):
#     WIN.fill((0, 0, 0))

#     pygame.draw.rect(WIN, COLOR, (x*100 + 500, 500, 5, 5))

#     pygame.display.update()

# def s():

#     d = []

#     for i in range(3000):
#         d.append([i, math.sin(math.pi/1000*i)])
    
#     return np.array(d)
def savitzky_golay_filter(data, window_size, polyorder):
    filtered_data = savgol_filter(data, window_size, polyorder)
    return filtered_data

def f(a, b, freq):
    kx = (b - a) / freq
    bx = a
    # print("Func -> y = {}x + {}".format(kx, bx))

    return ((kx, bx))

def integrand(x, k, b):
    return k*x + b

def kalman_filter(data):
    kf = KalmanFilter()
    filtered_data = kf.em(data).smooth(data)[0]
    return filtered_data

def i(data, freq, p):
    vel = 0

    out = [[0,0]]

    for i in range(len(data)-1):
        I = integrate.quad(integrand, 0, freq, args=f(data[i][p], data[i+1][p], freq))
        vel += I[0]

        out.append([i+1, vel])
    


    # print(vel)
    return np.array(out)

def main():

    file = open("filter.csv")
    data = csv.reader(file)

    next(data)
    acc = np.array([[0,0]])

    for r in data:
        d = np.array([[float(r[0].split(";")[1]),float(r[0].split(";")[2])]])
        acc = np.r_[acc, d]

    b = np.reshape(savitzky_golay_filter(acc[:, 0], 3, 1), (-1,1))
    # b = kalman_filter(acc[:, 0])
    
    print(b)

    out = i(b, freq, 0)

    # print(out)

    velout = i(out, freq, 1)
    # print(velout)

    # a = i(s(), freq, 1)
    # k = i(a, freq, 1)

    # plt.plot(a[:, 0], a[:, 1], color='r')
    # plt.plot(s()[:, 0], s()[:, 1], color='g')
    # plt.plot(k[:, 0], k[:, 1], color='y')

    plt.plot(velout[:, 0], velout[:, 1], color='r', label='s')
    plt.plot(out[:, 0], out[:, 1], color='g', label='v')
    plt.plot(acc[:, 0], color='b', label='a')
    plt.plot(b, color='y', label='filtered')
    plt.title('Графік швидкості/Графік переміщення')
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')
    plt.legend()
    plt.grid()

    # plt.ylim([-0.5, 0.5])
    # plt.xlim([0, 1000])
    plt.show()



if __name__ == "__main__":
    main()