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

def draw_window(coordinate):
    
    run = True

    for i in range(coordinate.shape[1]):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return 0
        pygame.time.Clock().tick(50)
        # WIN.fill((0, 0, 0))
        pygame.draw.rect(WIN, COLOR, (coordinate[0][i]* 200 + 1000, 500 - coordinate[1][i]* 200, 5, 5))
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

def integral(data, freq):
    vel = 0

    out = [0]

    for i in range(len(data)-1):
        I = integrate.quad(integrand, 0, freq, args=f(data[i], data[i+1], freq))
        vel += I[0]

        out.append(vel)
    
    return np.array(out)

def read_data(file_name):
    file = open(file_name)
    data = csv.reader(file)

    next(data)
    acc = np.array([[0,0,0]])

    for r in data:
        d = np.array([[float(r[0].split(";")[1]), float(r[0].split(";")[2]) * 10, float(r[0].split(";")[3]) * 10 ]])
        acc = np.r_[acc, d]
    
    return acc

def get_displacement(accel):

    data = [0,0,0]

    for i in range(3):
        filtred_accel = savitzky_golay_filter(accel[:, i], 3, 1) #x
        velocity = integral(filtred_accel, freq)
        displacement = integral(velocity, freq)

        data[i] = displacement

        if i == 1:
            plot_data(accel, filtred_accel, velocity, displacement)

    return np.array(data)

def plot_data(accel, filtred_accel, velocity, displacement):
    a = integrate.cumtrapz(accel[:, 1], None, freq,initial=0)

    plt.plot(a, color='black', label='velocity new')
    plt.plot(displacement, color='r', label='displacement')
    plt.plot(velocity, color='b', label='velocity')
    plt.plot(accel[:, 1], color='g', label='accel')
    plt.plot(filtred_accel, color='y', label='filtred accel')
    plt.title('Графік швидкості/Графік переміщення')
    plt.xlabel('time')
    plt.ylabel('m/ms^2/(m/s)')
    plt.legend()
    plt.grid()
    plt.show()

def main():

    accel = read_data("Aaa.csv")

    coordinate = get_displacement(accel)

    draw_window(coordinate)


if __name__ == "__main__":
    main()