import pyomo.environ as pyo
import time as tm 
from constraints_mcnd import flow_feas,capacity_constraint,obj_expression
from mcnd_data import *

if __name__ == "__main__":

    # Initialize Model
    model = pyo.AbstractModel()

    # Declare Parameter type
    model.users = pyo.Param(within=pyo.NonNegativeIntegers)
    model.nodes = pyo.Param(within=pyo.NonNegativeIntegers)
    model.links = pyo.Param(within=pyo.NonNegativeIntegers)
    model.nodes_idx = pyo.Param(within=pyo.NonNegativeIntegers)
    model.operators = pyo.Param(within=pyo.NonNegativeIntegers)

    # Set initialization 
    model.u = pyo.RangeSet(1,model.users)
    model.n = pyo.RangeSet(1,model.nodes)
    model.l = pyo.RangeSet(1,model.links)
    model.i = pyo.RangeSet(1,model.nodes_idx)
    model.o = pyo.RangeSet(1,model.operators)

    # Parameters
    model.origin = pyo.Param(model.l)
    model.destination = pyo.Param(model.l)
    model.t = pyo.Param(model.l)
    model.c = pyo.Param(model.l)
    model.w = pyo.Param(model.l)
    model.d = pyo.Param(model.u)
    model.O = pyo.Param(model.u)
    model.D = pyo.Param(model.u)
    model.utility = pyo.Param(model.u)
    model.N = pyo.Param(model.n)
    model.heads = pyo.Param(model.i,model.i, default=0)
    model.tails = pyo.Param(model.i,model.i, default=0)

    # Decision Variables
    model.x = pyo.Var(model.i, model.i,model.u,within=pyo.NonNegativeIntegers)
    model.y = pyo.Var(model.i, model.i,within=pyo.Binary)

    # Model 
    model.OBJ = pyo.Objective(rule=obj_expression)
    model.CapacityConstraint = pyo.Constraint(model.l, rule=capacity_constraint)
    model.FlowFeasibility = pyo.Constraint(model.u,model.n,rule=flow_feas)

    # Solve with SCIP
    start = tm.time()
    instance = model.create_instance("Data\\mcnd.dat")
    solver = pyo.SolverFactory('glpk')
    results = solver.solve(instance)

    # Print Results
    print(f'Minimized travel cost is {pyo.value(instance.OBJ)} dollars.')
    for i in instance.x:
        if (instance.x[i]).value != None and (instance.x[i]).value >0 :
            print(f'Link {(i[0],i[1])} is used for route {i[2]} with traffic {int((instance.x[i]).value)}.')

    print(f'Execution time is {round(tm.time()-start,3)} seconds.')
