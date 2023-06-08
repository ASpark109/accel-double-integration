import csv
import numpy as np
import math
import pygame
from scipy import integrate
import matplotlib.pyplot as plt
from pykalman import KalmanFilter
from scipy.signal import savgol_filter

WIN = pygame.display.set_mode((2340, 780))
COLOR = (200, 200, 200)

freq = 1/30 #Hz

def draw_window(x):
    WIN.fill((0, 0, 0))

    pygame.draw.rect(WIN, COLOR, (x*100 + 500, 500, 5, 5))

    pygame.display.update()

def savitzky_golay_filter(data, window_size, polyorder):
    filtered_data = savgol_filter(data, window_size, polyorder)
    return filtered_data

def f(a, b, freq):
    kx = (b - a) / freq
    bx = a

    return ((kx, bx))

def integrand(x, k, b):
    return k*x + b

def kalman_filter(data):
    kf = KalmanFilter()
    filtered_data = kf.em(data).smooth(data)[0]
    return filtered_data

def integral(data, freq, p):
    vel = 0

    out = [[0,0]]

    for i in range(len(data)-1):
        I = integrate.quad(integrand, 0, freq, args=f(data[i][p], data[i+1][p], freq))
        vel += I[0]

        out.append([i+1, vel])
    
    return np.array(out)

def read_data(file_name):
    file = open(file_name)
    data = csv.reader(file)

    next(data)
    acc = np.array([[0,0]])

    for r in data:
        d = np.array([[float(r[0].split(";")[1]),float(r[0].split(";")[2])]])
        acc = np.r_[acc, d]
    
    return acc

def main():

    accel = read_data("filter.csv")

    filtred_accel = np.reshape(savitzky_golay_filter(accel[:, 0], 3, 1), (-1,1))

    velocity = integral(filtred_accel, freq, 0)
    displacement = integral(velocity, freq, 1)


    plt.plot(displacement[:, 0], displacement[:, 1], color='r', label='s')
    plt.plot(velocity[:, 0], velocity[:, 1], color='g', label='v')
    plt.plot(accel[:, 0], color='b', label='a')
    plt.plot(filtred_accel, color='y', label='filtered')
    plt.title('Графік швидкості/Графік переміщення')
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')
    plt.legend()
    plt.grid()
    plt.show()



if __name__ == "__main__":
    main()