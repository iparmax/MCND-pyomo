import pyomo.environ as pyo
from constraints_mcnd import flow_feas,capacity_constraint,obj_expression
from mcnd_data import *


class MCND():
    
    def __init__(self):
        
        # Initialize Model
        self.model = pyo.AbstractModel()
        self.model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
        
        # Declare Parameters
        self.model.users = pyo.Param(within=pyo.NonNegativeIntegers)
        self.model.nodes = pyo.Param(within=pyo.NonNegativeIntegers)
        self.model.links = pyo.Param(within=pyo.NonNegativeIntegers)
        self.model.nodes_idx = pyo.Param(within=pyo.NonNegativeIntegers)
        self.model.operators = pyo.Param(within=pyo.NonNegativeIntegers)

        # Set initialization 
        self.model.u = pyo.RangeSet(1,self.model.users)
        self.model.n = pyo.RangeSet(1,self.model.nodes)
        self.model.l = pyo.RangeSet(1,self.model.links)
        self.model.i = pyo.RangeSet(1,self.model.nodes_idx)
        self.model.o = pyo.RangeSet(1,self.model.operators)

        # Parameters
        self.model.origin = pyo.Param(self.model.l)
        self.model.destination = pyo.Param(self.model.l)
        self.model.t = pyo.Param(self.model.l)
        self.model.c = pyo.Param(self.model.l)
        self.model.w = pyo.Param(self.model.l)
        self.model.d = pyo.Param(self.model.u)
        self.model.O = pyo.Param(self.model.u)
        self.model.D = pyo.Param(self.model.u)
        self.model.utility = pyo.Param(self.model.u)
        self.model.N = pyo.Param(self.model.n)
        self.model.heads = pyo.Param(self.model.i,self.model.i, default=0)
        self.model.tails = pyo.Param(self.model.i,self.model.i, default=0)

    # Decision Variables - MIP
    def get_dv_mip(self):
        x = pyo.Var(self.model.i, self.model.i,self.model.u,within=pyo.NonNegativeIntegers)
        y = pyo.Var(self.model.i, self.model.i,within=pyo.Binary)
        return x,y

    # Decision Variables - MIP
    def get_dv_dual(self):
        x = pyo.Var(self.model.i, self.model.i,self.model.u,within=pyo.NonNegativeReals)
        y = pyo.Param(self.model.i,self.model.i, default=0)
        return x,y
    
    def get_obj(self):
        OBJ = pyo.Objective(rule=obj_expression)
        return OBJ

    def get_cap_constraint(self):
        CapacityConstraint = pyo.Constraint(self.model.l, rule=capacity_constraint)
        return CapacityConstraint

    def get_flow_feasibility(self):
        FlowFeasibility = pyo.Constraint(self.model.u,self.model.n,rule=flow_feas)
        return FlowFeasibility 
