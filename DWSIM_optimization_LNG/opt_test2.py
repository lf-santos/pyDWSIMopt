# from pyDWSIMconnect import PyDWSIMconnect
from simulation import Simulation
import numpy as np
import time
from fobj import *
from scipy import optimize


sim_smr = Simulation(path2sim="C:\\Users\\lfsfr\\Desktop\\pyDWSIMopt\\sim\\SMR_1exp.dwxmz")
sim_smr.Add_refs()
sim_smr.Connect()

x0=[0.00118444444444444, 2.3e5, 48e5]
args=(sim_smr)
xtol=0.01
ftol=0.01
maxiter=50 # +- 5 seconds per iteration
print("starting optimization")
iteration = 0
regularizer = np.array([1e3, 1e-5, 1e-6])
bounds_raw = np.array( [[0.0010, 2e5, 30e5],[0.002, 5e5, 60e5]] )
bounds_reg = regularizer*bounds_raw
bounds = optimize.Bounds(bounds_reg[0], bounds_reg[1])
g = lambda x: fobj3n(sim_smr,np.asarray(x)/regularizer)[1]
nonlinear_constraint = optimize.NonlinearConstraint(g, 3, np.inf, jac='2-point', hess=optimize.BFGS())
f = lambda x: fobj3n(sim_smr,np.asarray(x)/regularizer)[0]

def test_TR():
    # Local optimization with trust-region -> working to some extent
    result = optimize.minimize(f,np.asarray(x0)*regularizer, method='trust-constr', jac='2-point', hess=optimize.BFGS(),
                constraints=[nonlinear_constraint], options={'verbose': 3, 'xtol': xtol, 'maxiter': maxiter, 'finite_diff_rel_step': None}, 
                bounds=bounds, callback=None)
    return result

def test_SHGO():
    # Global optimization with Simplical Homology -> too slow
    result = optimize.shgo(f, [(bounds_reg[0][0], bounds_reg[1][0]), (bounds_reg[0][1], bounds_reg[1][1]), (bounds_reg[0][2], bounds_reg[1][2])], 
            constraints={"type":'ineq', "fun": lambda x: g(x)-3}, n=20,
            options={"disp": 3, "maxiter": 20, "maxtime": 180})
    return result

def test_DE():
    # Global optimization with Differential Evolution
    result = optimize.differential_evolution(f, bounds, constraints=[nonlinear_constraint], maxiter=20, seed=1234, disp=True, polish=False)
    return result

def test_eggholder_GO():
    # Test SHGO:
    def eggholder(x):
        return (-(x[1] + 47) * np.sin(np.sqrt(abs(x[0]/2 + (x[1] + 47))))-x[0] * np.sin(np.sqrt(abs(x[0] - (x[1] + 47)))))

    bounds = [(-512, 512), (-512, 512)]
    results = dict()
    results['shgo'] = optimize.shgo(eggholder, bounds, n=64, sampling_method='sobol')
    results['da'] = optimize.dual_annealing(eggholder, bounds)
    results['de'] = optimize.differential_evolution(eggholder, bounds)
    results['bh'] = optimize.basinhopping(eggholder, bounds)
    return results

# result = optimize.minimize(f,np.asarray(x0)*regularizer, method='COBYLA', jac='2-point', hess=optimize.BFGS(),
#                constraints=[nonlinear_constraint], options={'disp': 1}, bounds=bounds, callback=cb)
# result = optimize.fmin_cobyla(f, x0, lambda x: g(x)-3, disp=3)
# result = optimize.fmin_slsqp(f, np.array([1.3, 1, 1])*x0, f_ieqcons = lambda x: g(x)-3, disp=3)

if __name__ == "__main__":
    test_TR()