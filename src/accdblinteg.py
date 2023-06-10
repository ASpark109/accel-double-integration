#Обробка помилок
    #Якщо файл не існує
    #Якщо step задано невірне число
    #Інтегрування пустих данних

import numpy as np
import csv
from scipy import integrate
import matplotlib.pyplot as plt
import pygame

class dblinteg:

    step = 0
    input_data = None

    velocity = None
    displacement = None

    def set_step(self, n):
        self.step = n

    def get_step(self):
        return self.step
    
    def get_input_data(self):
        return self.input_data
    
    def get_integrated_data(self):
        return self.displacement
    
    def get_velocity(self):
        return self.velocity
    
    def readf(self, file_name):

        file = open(file_name)
        rdata = csv.reader(file)

        next(rdata)
        acc = np.array([[0,0,0]])

        for r in rdata:
            d = np.array([[float(r[0].split(";")[1]), float(r[0].split(";")[2]), float(r[0].split(";")[3])]])
            acc = np.r_[acc, d]

        self.input_data = acc
    
    def dblintegral(self):

        disp_data = [0,0,0]
        vel_data = [0,0,0]

        for i in range(3):
            vel_data[i] = self.integral(self.input_data[:, i])
            disp_data[i] = self.integral(vel_data[i])

        self.velocity = np.array(vel_data)
        self.displacement = np.array(disp_data)
    
    def integrand(self, x, k, b):
        return k*x + b
    
    def f(self, a, b):
        kx = (b - a) / self.step
        bx = a

        return ((kx, bx))

    def integral(self, data):
        vel = 0

        out = [0]

        for i in range(len(data)-1):
            I = integrate.quad(self.integrand, 0, self.step, args=self.f(data[i], data[i+1]))
            vel += I[0]

            out.append(vel)
        
        return np.array(out)

    def plot_data(self, n = 0):

        plt.figure(figsize=(20,10))
        plt.subplot(1, 2, 1)
        plt.plot(self.velocity[n], color='b', label='velocity (m/s)')
        plt.plot(self.input_data[:, n], color='g', label='acceleration (m^2/s)')
        plt.xlabel('time')
        plt.legend()
        plt.grid()
        plt.title('Acceleration/Velocity')
        
        plt.subplot(1, 2, 2)
        plt.plot(self.displacement[1], color='orange', label='displacement (m)')
        plt.xlabel('time')
        plt.legend()
        plt.grid()
        plt.title('Displacement')

        plt.show()

    def visualise(self):

        WIDTH = 2340
        HEIGHT = 780

        scale = 10

        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        
        for i in range(self.displacement.shape[1]):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return 0
            pygame.time.Clock().tick(50)
            WIN.fill((0, 0, 0))
            pygame.draw.rect(WIN, 'white', (self.displacement[0][i]*scale + WIDTH/2, HEIGHT/2 - self.displacement[1][i]*scale, 5, 5))
            pygame.display.update()