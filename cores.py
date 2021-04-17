from ampl_data import *

def get_cores(duals,y_star):
    network = network_dict('Data\\network.csv')
    links = pd.read_csv('Data\\links.csv')
    t = []
    c = []
    for index, row in links.iterrows():
        t.append(row[1])
        c.append(row[2])

    routes = pd.read_csv('Data\\routes.csv')
    O = []
    D = []
    utility = []
    for index, row in routes.iterrows():
        O.append(row[2])
        D.append(row[3])
        utility.append(row[4])
    
    paths = (feas_paths(network,O,D))
    non_optimal_paths = {}
    for i in paths.items():
        idx = 0
        for j in y_star:
            if (any(list(j) == i[1][k:k+2] for k in range(len(i[1]) - 1))):
                idx = 1
                break
        if idx == 0:
            non_optimal_paths[i[0]] = i[1]

    u_cost = []
    for idx,(o,d) in enumerate(zip(O,D)):
        for i in paths.items():
            cost = 0
            for count,j in enumerate(network.values()):
                if (any(list(j) == i[1][k:k+2] for k in range(len(i[1]) - 1))) and (o in i[1]) and (d in i[1]) :
                    for k in non_optimal_paths.keys():
                        if i[0] == k:
                            cost += t[count] + duals[j] + c[count]*(1-y_star[j])
            u_cost.append((idx,cost))
    u = [x for x in u_cost if x[1]!=0]
    return u