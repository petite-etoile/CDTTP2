from cplex.exceptions import CplexError, CplexSolverError

def generate(mdl):
    mdl.parameters.mip.pool.absgap = 0.9
    mdl.parameters.mip.pool.intensity=4
    mdl.apply_parameters()
    cpx = mdl.get_cplex()
    try:
        cpx.populate_solution_pool()
    except CplexSolverError:
        print("Exception raised during populate")
        return []
    numsol = cpx.solution.pool.get_num()
    print("The solution pool contains %d solutions." % numsol)
    meanobjval = cpx.solution.pool.get_mean_objective_value()
    print("The average objective value of the solutions is %.10g." %
          meanobjval)

    nb_vars = mdl.number_of_variables
    sol_pool = []
    for i in range(numsol):
        objval_i = cpx.solution.pool.get_objective_value(i)

        x_i = cpx.solution.pool.get_values(i)
        assert len(x_i) == nb_vars
        sol = mdl.new_solution()
        for k in range(nb_vars):
            vk = mdl.get_var_by_index(k)
            if (x_i[k]!=0):
                sol.add_var_value(vk, x_i[k])
        sol_pool.append(sol)
    return sol_pool


# def get_schedule(mdl, values):
#     nb_vars = mdl.number_of_variables
#     schedule = []

#     for 