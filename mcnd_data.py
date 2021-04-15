import pandas as pd
from network import * 

def write_param(f,in_dict,param):
    f.write(f"param {param} := \n")
    count = 0
    for value in in_dict.items():
        if value[0][1] ==f'{param}':
            f.write(f'{count+1} {value[1]} \n')
            count+=1
    f.write(';\n\n')

# Write file to AMPL Format 

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
