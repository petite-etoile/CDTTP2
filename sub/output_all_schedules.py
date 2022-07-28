import re
def output_all_schedules(mdl, sol_pool, team_num, f):
    for idx, sol in enumerate(sol_pool, start=1):
        schedule = get_schedule(mdl, sol, team_num)
        f.write("{:0>2}".format(idx) + "-"*20 + "\n")
        write_schedule(schedule, f)

def get_schedule(mdl, sol, team_num):
    nb_vars = mdl.number_of_variables

    schedule = [["__" for _ in range(2*(team_num-1))] for _ in range(team_num)]
    # print(sol.get_values([i for i in range(nb_vars)]))
    for var in mdl.iter_binary_vars():
        if sol.get_value(var) < 0.5:
            continue
        # print(str(var), sol.get_value(var))
        if "-" in str(var) or "vs" in str(var):
            continue

        i,r,j,ha = parse(str(var))
        schedule[i-1][r-1] = "{:>3}".format(j) if ha == 0 else "{:>3}".format("@" + str(j))
        
    # for key, val in sol.get_value_dict(cat ):
    #     print(key,val)
    return schedule

def write_schedule(schedule, f):
    print("-"*20)
    for row in schedule:
        f.write(" ".join(row))
        f.write("\n")
        print(*row, sep=" ")
    

def parse(line):
    i,r,j,ha,*_ = map(int,re.findall(r"\d+", line))
    return i,r,j,ha
