import pandas as pd
from network import * 
import shutil
import pyomo.environ as pyo
import time as tm 
from collections import defaultdict

def write_param(f,in_dict,param):
    f.write(f"param {param} := \n")
    count = 0
    for value in in_dict.items():
        if value[0][1] ==f'{param}':
            f.write(f'{count+1} {value[1]} \n')
            count+=1
    f.write(';\n\n')


# Write file to AMPL Format 
def create_dat():
    # Load Network
    df = pd.read_csv('Data\\network.csv')
    network = {}
    operators = []
    for index, row in df.iterrows():
        network[row[0], row[1]] = row[2], row[3]
        operators.append(row[1])
    no_operators = len(set(operators))

    # Load User Data
    df = pd.read_csv('Data\\routes.csv')
    routes = {}
    no_routes = 0
    for index, row in df.iterrows():
        routes[row[0],'d'] = row[1]
        routes[row[0],'O'] = row[2]
        routes[row[0],'D'] = row[3]
        routes[row[0],'utility'] = row[4]
        no_routes +=1

    # Load Links Data
    df = pd.read_csv('Data\\links.csv')
    links = {}
    no_links = 0
    for index, row in df.iterrows():
        links[row[0],'t'] = row[1]
        links[row[0],'c'] = row[2]
        links[row[0],'w'] = row[3]
        links[row[0],'link_oper'] = row[4]
        no_links +=1

    # Loading Networx 
    G = get_network(network)
    f = open("Data\\mcnd.dat", "w")
    f.write(f'param users := {no_routes} ;\n')
    f.write(f'param nodes := {len(G.nodes)} ;\n')
    f.write(f'param links := {no_links} ;\n')
    f.write(f'param nodes_idx := {max(G.nodes)} ;\n')
    f.write(f'param operators := {no_operators} ;\n')
    f.write(f'\n')

    f.write(f'param origin := \n')
    for count, value in enumerate(network.values()):
        f.write(f'{count+1} {value[0]} \n')
    f.write(';\n\n')

    f.write(f'param destination := \n')
    for count, value in enumerate(network.values()):
        f.write(f'{count+1} {value[1]} \n')
    f.write(';\n\n')

    f.write(f'param N := \n')
    for count, value in enumerate(sorted(G.nodes)):
        f.write(f'{count+1} {value} \n')
    f.write(';\n\n')

    write_param(f,links,'t')
    write_param(f,links,'c')
    write_param(f,links,'w')
    write_param(f,links,'link_oper')
    write_param(f,routes,'d')
    write_param(f,routes,'O')
    write_param(f,routes,'D')
    write_param(f,routes,'utility')

    f.write(f'param : heads := \n')
    for value in heads(G).items():
        f.write(f'{value[0][0]} {value[0][1]} {value[1]} \n')
    f.write(';\n\n')

    f.write(f'param : tails := \n')
    for value in tails(G).items():
        f.write(f'{value[0][0]} {value[0][1]} {value[1]} \n')
    f.write(';\n\n')
    f.close()

def fix_y(model):
    shutil.copyfile("Data\\mcnd.dat", "Data\\mcnd_dual.dat")
    f = open("Data\\mcnd_dual.dat", "a")
    f.write(f'param : y := \n')
    for i in model.y:
        if (model.y[i]).value == None or (model.y[i]).value == 0:
            f.write(f'{i[0]} {i[1]} {0} \n')
        else:
            f.write(f'{i[0]} {i[1]} {1} \n')
    f.write(';\n\n')
    f.close()

def get_results(model,start):
    print(f'Minimized travel cost is {pyo.value(model.OBJ)} dollars.')
    for i in model.x:
        if (model.x[i]).value != None and (model.x[i]).value >0 :
            print(f'Link {(i[0],i[1])} is used for route {i[2]} with traffic {int((model.x[i]).value)}.')

    print(f'Execution time is {round(tm.time()-start,3)} seconds.')

def get_duals(model):
    network = network_dict('Data\\network.csv')
    duals = {} 
    duals = defaultdict(lambda:0,duals)
    y_store = {} 
    y_store = defaultdict(lambda:0,duals)
    for a in (model.CapacityConstraint):
        for count,k in enumerate(network.values()):
            if count+1 == a and model.y[k] ==1 :
                duals[k] = abs(model.dual.get(model.CapacityConstraint[a]))
                y_store[k] = 1
    return duals,y_store