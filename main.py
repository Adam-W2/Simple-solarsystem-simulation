"""
Main class
Used to run and debug everything
"""
from Solar_sim import Simulation
class testSimulation(object):
    
    def test(self):
        #imput for the simulation, timestep and number of iterations
        C = Simulation(5000, 25000)
        C.read_file()
        C.initial_cons()
        C.run()

        
def main():
    run = testSimulation()
    run.test()
main()
