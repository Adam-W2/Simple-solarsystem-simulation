## Simple Solar System Simulation

This repo contains a object orientated simulation of the solar system with a small satellite sent to land on Mars
Simulation will run for given nunmber of iterations set in the main.py file and each time a planet completes its orbit the orbital period will be printed in the terminal. Planet information including mass, radius, position, starting velocity are contained in the Planets.txt file

Simulation is currently set up to set Mars position manually and so will need to be edited if
the user wants to set the mars position and velocity automatically. Getting rid of the if statement on
line 47 in the simulation class will change this

# How to run
The simulation is currently set up with inital parameters so just running
```
python main.py
```