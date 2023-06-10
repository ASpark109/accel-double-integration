#Обробка помилок
    #Коректне читання даних
    #Інтегрування пустих данних

import numpy as np
import csv
from scipy import integrate
import matplotlib.pyplot as plt
import pygame
import sys
from colorama import init
from colorama import Fore, Style

class dblinteg:

    def __init__(self):
        init()
        self.__private_step = 1
        self.__private_input_data = None

        self.__private_velocity = None
        self.__private_displacement = None

        self.__private_separator = ','
        self.__private__visualise_scale = 1

    def set_step(self, n):

        if n > 0:
            self.__private_step = n
        else:
            print(Fore.YELLOW + Style.BRIGHT + "[Warning]" + Style.RESET_ALL + ": The number must be greater than zero the step is set to 1")

    def get_step(self):
        return self.__private_step
    
    def get_input_data(self):
        return self.__private_input_data
    
    def get_integrated_data(self):
        return self.__private_displacement
    
    def get_velocity(self):
        return self.__private_velocity
    
    def get_separator(self):
        return self.__private_separator
    
    def get_scale(self):
        return self.__private__visualise_scale
    
    def set_scale(self, n):

        if n > 0:
            self.__private_separator = n
        else:
            print(Fore.YELLOW + Style.BRIGHT + "[Warning]" + Style.RESET_ALL + ": The number must be greater than zero the scale is set to 1")
    
    def set_separator(self, c):

        if len(c) == 1:
            self.__private_separator = c
        else:
            print(Fore.YELLOW + Style.BRIGHT + "[Warning]" + Style.RESET_ALL + ": A separator character can consist of only one character. Set to ;")

    def readf(self, file_name):

        try:
            file = open(file_name)
        except FileNotFoundError:
            msg = Fore.RED + Style.BRIGHT + "[ERROR]" + Style.RESET_ALL + ": Sorry, the file "+ file_name + " does not exist."
            print(msg)   
            sys.exit(1) 

        rdata = csv.reader(file, delimiter = self.__private_separator)

        next(rdata)
        acc = np.array([[0,0,0]])

        for r in rdata:
            d = np.array([[float(r[1]), float(r[2]), float(r[3])]])
            acc = np.r_[acc, d]

        self.__private_input_data = acc
    
    def dblintegral(self):

        disp_data = []
        vel_data = []

        for i in range(3):
            vel_data.append(self.__private_integral(self.__private_input_data[:, i]))
            disp_data.append(self.__private_integral(vel_data[i]))

        self.__private_velocity = np.array(vel_data)
        self.__private_displacement = np.array(disp_data)
    
    def __private_integrand(self, x, k, b):
        return k*x + b
    
    def __private_f(self, a, b):
        k = (b - a) / self.__private_step
        b = a

        return ((k, b))

    def __private_integral(self, data):
        vel = 0

        out = [0]

        for i in range(len(data)-1):
            I = integrate.quad(self.__private_integrand, 0, self.__private_step, args=self.__private_f(data[i], data[i+1]))
            vel += I[0]

            out.append(vel)
        
        return np.array(out)

    def plot_data(self, n = 0):

        plt.figure(figsize=(20,10))
        plt.subplot(1, 2, 1)
        plt.plot(self.__private_velocity[n], color='b', label='velocity (m/s)')
        plt.plot(self.__private_input_data[:, n], color='g', label='acceleration (m^2/s)')
        plt.xlabel('time')
        plt.legend()
        plt.grid()
        plt.title('Acceleration/Velocity')
        
        plt.subplot(1, 2, 2)
        plt.plot(self.__private_displacement[n], color='orange', label='displacement (m)')
        plt.xlabel('time')
        plt.legend()
        plt.grid()
        plt.title('Displacement')

        plt.show()

    def visualise(self):

        WIDTH = 2340
        HEIGHT = 780

        scale = 1

        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        
        for i in range(self.__private_displacement.shape[1]):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return 0
            pygame.time.Clock().tick(90)
            WIN.fill((0, 0, 0))
            pygame.draw.rect(WIN, 'white', (self.__private_displacement[0][i]*scale + WIDTH/2, HEIGHT/2 - self.__private_displacement[1][i]*scale, 5, 5))
            pygame.display.update()