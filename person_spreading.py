# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 08:28:25 2020

@author: las
"""

import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import copy

class Person():
    x_max = 100
    y_max = 100
    def __init__(self):
        self.x_location = random.random() * self.x_max
        self.y_location = random.random() * self.y_max
        self.status = "Healthy"
        self.velocity = [0.,0.]
        self.sick_days = 0
        self.number_infected = 0
        self.set_velocity()
    
    
    def set_velocity(self):
        self.velocity = [(random.random()-0.5)/2., (random.random()-0.5)/2.]
    
    
    def set_location(self):
        self.x_location = random.random() * self.x_max
        self.y_location = random.random() * self.y_max
        
    
    def test_travelling(self):
        is_travelling = random.random() < 0.001
        if self.velocity[0] != 0 and is_travelling:
            self.set_location()
    
    def immobilize(self):
        self.velocity = [0,0]
    
    def update_location(self):
        if self.x_location + self.velocity[0] > self.x_max:
            self.velocity[0] = -self.velocity[0]
            
        elif self.x_location + self.velocity[0] < 0:
            self.velocity[0] = -self.velocity[0]
            
        else:
            self.x_location = self.x_location + self.velocity[0]
        
        
        if self.y_location + self.velocity[1] > self.y_max:
            self.velocity[1] = -self.velocity[1]
            
        elif self.y_location + self.velocity[1] < 0:
            self.velocity[1] = -self.velocity[1]
            
        else:
            self.y_location = self.y_location + self.velocity[1]



class Simulation():
    def __init__(self, population, quarintine_start=None, quarintine_end=None):
        self.n_people = len(population)
        self.population = population
        self.quarintine_start = quarintine_start 
        self.quarintine_end = quarintine_end
        self.x_locations = np.zeros(n_people)
        self.y_locations = np.zeros(n_people)
        self.population_health = []
        self.people_infected = []
        self.x_locations_all = []
        self.y_locations_all = []
        self.n_sick = []
        self.n_healthy = []
        self.n_immune = []
        self.colors_all = []
        self.population[0].status = 'Sick' 
        
        
    def run_simulation(self, n_times):
        for t in range(n_times):
            self.x_locations = np.zeros(self.n_people)
            self.y_locations = np.zeros(self.n_people)
            self.population_health = []
            colors = ['b'] * self.n_people
            
            if t == self.quarintine_start:
                self.start_quarentine()
            if t == self.quarintine_end:
                self.end_quarentine()
                
            for i, person in enumerate(self.population):
                person.update_location()                
                self.x_locations[i] = person.x_location    
                self.y_locations[i] = person.y_location
                
            for i, person in enumerate(self.population):
                self.test_for_transmission(person)
                self.population_health.append(person.status)
                if person.status == "Sick":
                    colors[i] = "r"
                elif person.status == "Immune":
                    colors[i] = "g"
                    
            self.x_locations_all.append(self.x_locations)
            self.y_locations_all.append(self.y_locations)
            self.colors_all.append(colors)
            self.n_sick.append(colors.count("r"))
            self.n_healthy.append(colors.count("b"))
            self.n_immune.append(colors.count("g"))
      
        
    def test_for_transmission(self, person):      
        if person.status == "Healthy":
            distance = ((self.x_locations - person.x_location)**2 + (self.y_locations - person.y_location)**2)**0.5
            idxs = np.where(distance < 1.1)[0]
            healthy = True
            for el in idxs:
                if self.population[el].status == "Sick" and healthy:
                    person.status = "Sick"
                    self.population[el].number_infected += 1
                    healthy = False
                    
        if person.status == "Sick":
            if person.sick_days > 100:
                person.status = "Immune"
                self.people_infected.append(person.number_infected)
            else:
                person.sick_days += 1
      
    def start_quarentine(self):          
        for i, person in enumerate(self.population):
            if i%2==0:
                person.immobilize()
    
    def end_quarentine(self):
        for i, person in enumerate(self.population):
            if i%2==0:
                person.set_velocity()
        
                
                
n_people = 500 
n_times = 1000   
people1 = []
people2 = []


for i in range(n_people):
    person = Person()
    people1.append(person)
    people2.append(copy.deepcopy(person))


sim1 = Simulation(people1)
sim1.run_simulation(n_times)

sim2 = Simulation(people2, quarintine_start=200, quarintine_end=500)
sim2.run_simulation(n_times)




n_healthy_1 = np.asarray(sim1.n_healthy)/n_people*100
n_sick_1 = np.asarray(sim1.n_sick)/n_people*100
n_immune_1 = np.asarray(sim1.n_immune)/n_people*100

n_healthy_2 = np.asarray(sim2.n_healthy)/n_people*100
n_sick_2 = np.asarray(sim2.n_sick)/n_people*100
n_immune_2 = np.asarray(sim2.n_immune)/n_people*100


fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(10,5))
scatter = ax1.scatter([], [], color='k', animated=True)
line, = ax1.plot([], [], color='k', linewidth=1)

colors = ['b']*n_people
colors[0] = 'r'

text_color = 'w'
 
def update(num):
     print(num)
     
     if num//20%2 == 0:
         fig.suptitle('THIS IS NOT SCIENCE!', fontsize=18, color='r')
     else:
         fig.suptitle('', fontsize=18, color='r')
         
         
     ax1.cla()
     ax1.clear()    
     ax1.fill_between((0,100),(100,100), color='k')
     ax1.set_title("COVID19 \n No quarantine", color=text_color)
     ax1.scatter(sim1.x_locations_all[num], sim1.y_locations_all[num], color=sim1.colors_all[num], alpha=0.9, s=3)
     ax1.plot(np.arange(num)/10, n_healthy_1[0:num], 'b')
     ax1.plot(np.arange(num)/10, n_sick_1[0:num], 'r')
     ax1.plot(np.arange(num)/10, n_immune_1[0:num], 'g')
     line.set_data([], [])
     ax1.set_xlim(0,100)
     ax1.set_ylim(0,100)
     ax1.scatter([],[], color='b', label="Susceptible")
     ax1.scatter([],[], color='r', label="Infected")
     ax1.scatter([],[], color='g', label="Removed")
     ax1.legend(loc=1)
     ax1.set_xlabel("Days", color=text_color)
     ax1.set_ylabel("Percentage of population", color=text_color)
     ax1.tick_params(axis='both', which='major', labelcolor=text_color)
     
     ax2.cla()
     ax2.clear()
     ax2.fill_between((0,100),(100,100), color='k')
     if num > 200 and num < 500:
         ax2.set_title("LOCKDOWN \n 50% of population", color=text_color)
     else:
         ax2.set_title("COVID19 \n Quarantine from day 20 to 50", color=text_color)
     ax2.scatter(sim2.x_locations_all[num], sim2.y_locations_all[num], color=sim2.colors_all[num], alpha=0.9, s=3)
     ax2.plot(np.arange(num)/10, n_healthy_2[0:num], 'b')
     ax2.plot(np.arange(num)/10, n_sick_2[0:num], 'r')
     ax2.plot(np.arange(num)/10, n_immune_2[0:num], 'g')
     line.set_data([], [])
     ax2.set_xlim(0,100)
     ax2.set_ylim(0,100)
     ax2.scatter([],[], color='b', label="Susceptible")
     ax2.scatter([],[], color='r', label="Infected")
     ax2.scatter([],[], color='g', label="Removed")
     ax2.legend(loc=1)
     ax2.set_xlabel("Days", color=text_color)
     ax2.tick_params(axis='both', which='major', labelcolor=text_color)
     
     return line, scatter,
     

ani = animation.FuncAnimation(fig, update, 100, repeat_delay=1000,
                               interval=25, blit=True)

writer = animation.writers['ffmpeg'](fps=30, bitrate=5000)
ani.save('test_qa.mp4',writer=writer,dpi=200,savefig_kwargs=dict(facecolor='k'))
#ani.save('SIRish.gif')
plt.show()



