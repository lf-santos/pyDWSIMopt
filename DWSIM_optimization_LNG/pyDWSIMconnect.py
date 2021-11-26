from pyDWSIMrefs import pyDWSIMrefs
pyDWSIMrefs()
# importing DWSIM classes from clr references
from DWSIM.Interfaces.Enums.GraphicObjects import ObjectType
from DWSIM.Thermodynamics import Streams, PropertyPackages
from DWSIM.UnitOperations import UnitOperations
from DWSIM.Automation import Automation2
from DWSIM.GlobalSettings import Settings

from os import getcwd

def pyDWSIMconnect(sim):  
    if hasattr(sim, 'flowsheet') != True:
        # create automation manager
        interf = Automation2()

        # load simulation
        flowsheet = interf.LoadFlowsheet(sim.path)

        # add DWSIM objects to Simulation object
        sim.interface = interf
        sim.flowsheet = flowsheet
        
        if flowsheet is not None:
            print("Simulation was loaded successfully")
    
    

    

if __name__ == "__main__":
    pyDWSIMconnect()