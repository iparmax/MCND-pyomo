
from ampl_data import *
from MCND import *
from cores import * 


if __name__ == "__main__":

    # Construct Original MCND
    mcnd = MCND()
    model = mcnd.model
    model.x = mcnd.get_dv_mip()[0]
    model.y = mcnd.get_dv_mip()[1]
    model.OBJ =  mcnd.get_obj()
    model.CapacityConstraint = mcnd.get_cap_constraint()
    model.FlowFeasibility = mcnd.get_flow_feasibility()
    
    # Solve Original MCND
    start = tm.time()
    try:
        instance = model.create_instance("Data\\mcnd.dat")
    except:
        create_dat()
        instance = model.create_instance("Data\\mcnd.dat")
    solver = pyo.SolverFactory('glpk')
    results = solver.solve(instance)

    # Print Results
    get_results(instance,start)

    # Construct Dual
    mcnd = MCND()
    model = mcnd.model
    model.x = mcnd.get_dv_dual()[0]
    model.y = mcnd.get_dv_dual()[1] # Fixing y to get duals
    model.OBJ =  mcnd.get_obj()
    model.CapacityConstraint = mcnd.get_cap_constraint()
    model.FlowFeasibility = mcnd.get_flow_feasibility()
    
    # Find Duals for Capacity Constraint
    try:
        instance = model.create_instance("Data\\mcnd_dual.dat")
    except:
        fix_y(instance)
        instance = model.create_instance("Data\\mcnd_dual.dat")
    solver = pyo.SolverFactory('glpk')
    results = solver.solve(instance)
    
    
    duals = (get_duals(instance)[0])
    y_star = (get_duals(instance)[1])
    cores = (get_cores(duals,y_star))

