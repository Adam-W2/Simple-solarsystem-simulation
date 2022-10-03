"""
Solar system - Planet class
Planet class to create the planets and sun
"""
import numpy as np

class Planet(object):
    def __init__(self, timestep, name, colour, radius, mass, coords, velocity, acceleration):
        self.name = name
        self.mass = mass
        self.coords = coords
        self.velocity = velocity
        self.acceleration = acceleration
        self.prev_acceleration = 0
        self.timestep = timestep
        self.colour = colour
        self.radius = radius
        self.prev_coords = 0
        #need a counter for the timestep to print out days of period
        self.counter = 0
    #most of these are just encapsulation to access them else where
    def get_name(self):
        return self.name
    
    def get_colour(self):
        return self.colour
    
    def get_radius(self):
        return self.radius

    def get_mass(self):
        return self.mass

    def get_coords(self):
        return self.coords

    def get_velocity(self):
        return self.velocity
    
    def get_acceleration(self):
        return self.acceleration
    
    def get_prev_acceleration(self):
        return self.prev_acceleration
    #updates coords
    def update_coords(self):
        self.prev_coords = self.coords
        self.coords = self.coords + self.velocity * self.timestep + 1/6 * (4 * self.acceleration - self.prev_acceleration) * (self.timestep)**2
    #updates velocity
    def update_velocity(self, new_acceleration):
        self.velocity = self.velocity + 1/6 * (2 * new_acceleration + 5 * self.acceleration - self.prev_acceleration) * self.timestep
    
    def set_coords(self, coords):
        self.coords = coords
        
    def set_velocity(self, velocity):
        self.velocity = velocity
    
    def set_acceleration(self, acceleration):
        self.acceleration = acceleration
    
    def set_prev_acceleration(self, prev_acceleration):
        self.prev_acceleration = prev_acceleration
    #orbital period - calculated from when the y coord goes from negative to positive
    def check_orbital_period(self):
        self.counter = self.counter + self.timestep 
        if self.prev_coords[1] < 0 and self.coords[1] > 0:
            #prints the orbital period in days then resets counter to calculate next orbit
            print(self.get_name() + " " + "orbital period: " + str(self.counter/(60*60*24)))
            self.counter = 0
            
    def kinetic_energy(self):
        a = 1/2 * self.get_mass() * (np.linalg.norm(self.get_velocity()))**2
        return a 