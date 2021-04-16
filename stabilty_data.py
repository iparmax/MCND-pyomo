import pandas as pd
from network import * 
import shutil
import pyomo.environ as pyo
import time as tm 

network = network_dict('Data\\network.csv')