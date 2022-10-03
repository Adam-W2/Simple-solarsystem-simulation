"""
Solar system - simulation class
Makes the whole system tick and calculates accelerations
"""
from Planet import Planet
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Simulation(object):
    
    def __init__(self, timestep, N):
        self.N = N
        #main empty list for planets to go into
        self.planet_list = []
        self.G = 6.67408E-11
        self.totaltime = 0
        #many empty lists to store energy and time values which are then plotted
        self.energy_list = []
        self.kinetic_list = []
        self.potent_list = []
        self.totaltime_list = []
        self.timestep = timestep
        #arbitary values for my closet value to mars 
        self.minValue = 1E12
        self.prevMinValue = 2E12
        #counter to make the value only print once
        self.counter = 1
    #file reading method    
    def read_file(self):
        filein = open("Planets.txt", "r")
        for line in filein.readlines():
            temp = line.split(",")
            #timestep, name, colour, radius, mass, x, y, vx, vy, ax, ay 
            temp2 = Planet(self.timestep, temp[0], str(temp[1]), float(temp[2]), float(temp[3]), np.array((float(temp[4]), float(temp[5]))), np.array((float(temp[6]), float(temp[7]))), np.array((int(temp[8]), 0)))
            self.planet_list.append(temp2)
        filein.close()
    #sets inital conditions    
    def initial_cons(self):
        for i in range(len(self.planet_list)-1):
            if i != 0:    #makes sure mars and the sun dont have general inital velocities so I can manually set them
                d = self.planet_list[i].get_coords()
                if i != 1:
                    a = ((6.67408E-11 * self.planet_list[0].get_mass()) / d[0]) ** (1/2)
                    b = np.array((0,a))
                    self.planet_list[i].set_velocity(b)
        #sets acceleration        
        for i in range(len(self.planet_list)):
            if i != 0:
                a = self.calc_acceleration(self.planet_list[i])
                self.planet_list[i].set_acceleration(a)
                self.planet_list[i].set_prev_acceleration(a)
    #method used to determind closest distance to Mars    
    def sat_distance_mars(self):
        r = self.planet_list[1].get_coords() - self.planet_list[5].get_coords()
        d = np.linalg.norm(r)
    #updates the minvalue so we get the next minimum value
        if d < self.minValue:
            self.minValue = d
    #checks if the minvalue is the same as the previous meaning the satellite has reached its minimum value        
        if self.prevMinValue == self.minValue:
            if self.counter == 1:
                #prints off distance and time taken to reach this value
                print("Closest distance to mars: " + str(self.minValue))
                print("Time taken: " + str(self.totaltime / (60*60*24)))
                #sets the counter to 0 so it only prints once
                self.counter = 0
        self.prevMinValue = self.minValue
    
    def calc_acceleration(self, body):
        acc = np.array((0,0))
        #this loops over each planet to calculate the total acceleration
        for i in range(len(self.planet_list)):
            d = body.get_coords() - self.planet_list[i].get_coords()
            
            if self.planet_list[i] != body:

                a = -(self.G * self.planet_list[i].get_mass() * d) / (np.linalg.norm(d)**3)
                acc = acc + a
        #returns the acceleration for later use
        return acc
    #big method that updates all acceleration, positions and velocities as well as energies 
    def step_forward(self):
        r = []
        #for loop to update coords and append them to the empty list
        for i in range(len(self.planet_list)):
            self.planet_list[i].update_coords()
            r.append(self.planet_list[i].get_coords())
        #for loop to update velocity
        for i in range(len(self.planet_list)):
            a = self.calc_acceleration(self.planet_list[i])
            self.planet_list[i].update_velocity(a)
        #for loop to update acceleration    
        for i in range(len(self.planet_list)):
            a = self.calc_acceleration(self.planet_list[i])
            self.planet_list[i].set_prev_acceleration(self.planet_list[i].get_acceleration())
            self.planet_list[i].set_acceleration(a)
        #checks if the planets have crossed the threshhold of y from negative to positive
        for i in range(len(self.planet_list)): 
            self.planet_list[i].check_orbital_period()
        #constantly checks if the satellite has reached its smallest distance yet    
        self.sat_distance_mars()
        #appends the energy at each timestep to the empty lists    
        self.totaltime_list.append(self.totaltime)
        self.energy_list.append(self.calculate_tot_energy())
        self.potent_list.append(self.calculate_potent())
        #keeps track of the time, updates it
        self.totaltime += self.timestep
        #checks if the simulation has ended then plots graph if it has
        if self.totaltime == self.timestep * self.N:
            self.plot_energy()
            
        return r 
    #calculates the potential energy by looping over each planet
    def calculate_potent(self):
        potent = 0
        for i in range(len(self.planet_list)):
            for j in range(len(self.planet_list)):
                if i != j:
                    d = self.planet_list[i].get_coords() - self.planet_list[j].get_coords()
                    a = -(self.G * self.planet_list[i].get_mass() * self.planet_list[j].get_mass()) / (np.linalg.norm(d))
                    potent = potent + a
        return 1/2 * potent
    #calcualtes the total kinetic energy and adds it to the potential energy of the system
    def calculate_tot_energy(self):
        kinetic = 0
        for i in range(len(self.planet_list)):
            a = self.planet_list[i].kinetic_energy()
            kinetic = kinetic + a
        self.kinetic_list.append(kinetic)
        total = kinetic + self.calculate_potent()
        return total
    #plots the energy versus time graph
    def plot_energy(self):
        #uses a different figure to the animation
        plt.figure(2)
        plt.plot(self.totaltime_list,self.energy_list, color = "Green",label = "Total")
        plt.plot(self.totaltime_list,self.potent_list,color = "Blue",label = "Potential")
        plt.plot(self.totaltime_list,self.kinetic_list,color = "Red",label = "Kinetic")
        plt.xlim([0,self.timestep * self.N])
        plt.legend()
        plt.title("Total, potential and kinetic energy versus time")
        plt.xlabel("Time (s)")
        plt.ylabel("Energy (J)")
        plt.show()
        
        #this is for printing the average energy at the end to see if they change in different simulations
        a = 0
        b = 0 
        c = 0
        for i in range(len(self.energy_list)):
            a += self.energy_list[i]
            b += self.potent_list[i]
            c += self.kinetic_list[i]
            
        print("Average total energy: " + str(a/len(self.energy_list)))
        print("Average potential energy: " + str(b/len(self.potent_list)))
        print("Average kinetic energy: " + str(c/len(self.kinetic_list)))
        
    #animation method, assigns the planets to their own patch at the centre      
    def animate(self, i):
        r = self.step_forward()
        for i in range(len(r)):
            self.patches[i].center = r[i]
        return self.patches
    #runs the whole simulation
    def run(self):
        fig = plt.figure(1)
        ax = plt.axes()
        
        self.patches = []
        #two loops to assign circles and add those circles to the animation    
        for i in range(len(self.planet_list)):
            self.patches.append(plt.Circle(self.planet_list[i].get_coords(), self.planet_list[i].get_radius(), color = self.planet_list[i].get_colour(), animated = True))
        for i in range(0, len(self.patches)):
            ax.add_patch(self.patches[i])
        #axis setup    
        ax.axis('scaled')
        ax.set_xlim(-2.844E11, 2.844E11)
        ax.set_ylim(-2.844E11, 2.844E11)
        ax.set_xlabel("x-axis (m)")
        ax.set_ylabel('y-axis (m)')
        #animates and finally shows the animation
        self.anim = FuncAnimation(fig, self.animate, frames = self.N, repeat = False, interval = 1, blit = True)
        
        plt.show()