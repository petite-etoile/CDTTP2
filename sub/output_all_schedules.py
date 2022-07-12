import re
def output_all_schedules(mdl, sol_pool, team_num, f):
    for sol in sol_pool:
        schedule = get_schedule(mdl, sol, team_num)
        write_schedule(schedule, f)

def get_schedule(mdl, sol, team_num):
    nb_vars = mdl.number_of_variables

    schedule = [["__" for _ in range(2*(team_num-1))] for _ in range(team_num)]
    # print(sol.get_values([i for i in range(nb_vars)]))
    for var in mdl.iter_binary_vars():
        if "-" in str(var):
            continue
        if sol.get_value(var) < 0.5:
            continue

        i,r,j,ha = parse(str(var))
        schedule[i-1][r-1] = " {:2>}".format(j) if ha == 0 else "@{:2>}".format(j)
        
    # for key, val in sol.get_value_dict():
    #     print(key,val)
    return schedule

def write_schedule(schedule, f):
    f.write("-"*20 + "\n")
    print("-"*20)
    for row in schedule:
        f.write(" ".join(row))
        f.write("\n")
        print(*row)
    

def parse(line):
    i,r,j,ha,*_ = map(int,re.findall(r"\d+", line))
    return i,r,j,ha
