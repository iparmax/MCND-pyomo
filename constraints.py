import pyomo.environ as pyo
import time as tm 

def obj_expression(model):

    terms_x = []
    for i in model.l:
        for u in model.u:
            terms_x.append(model.t[i]*model.x[model.origin[i],model.destination[i],u])

    terms_y = []
    for i in model.l:
        terms_y.append(model.c[i]*model.y[model.origin[i],model.destination[i]])
        
    return sum(terms_x) + sum(terms_y)

def capacity_constraint(model,l):

    terms = []
    for u in model.u:
        terms.append(model.x[model.origin[l],model.destination[l],u]) 
    return (sum(terms)<= model.w[l]*model.y[model.origin[l],model.destination[l]])

def check_flow(model,u,n):
    
    terms_heads = []
    terms_tails = []
    N_n = model.N[n]
    for i in model.i:
        if model.heads[N_n,i] >= 1 :
            terms_heads.append(model.x[N_n,model.heads[N_n,i],u])

        if model.tails[model.N[n],i] >= 1 :
            terms_tails.append(model.x[model.tails[N_n,i],N_n,u])

    return (sum(terms_heads) - sum(terms_tails)) 

def flow_feas(model,u,n):
    
    if model.N[n] == model.O[u]:
        return check_flow(model,u,n) == model.d[u]

    elif model.N[n] == model.D[u]:
        return check_flow(model,u,n) == -model.d[u]

    else:
        return check_flow(model,u,n) == 0

