from docplex.mp import model 
import os
import re
import sys

from time import time

from datetime import datetime

sys.path.append(os.pardir)
from sub import generate_solution_pool, output_all_schedules
from Model import CDTTP2_round_pair_Model 


def main():
    
    n = int(sys.argv[1])

    year, month, date, hour, minute, second, *_ = re.split("[ .:-]", str(datetime.now()))
    output_file = "round_pair_result_all/n{:0>2}.text".format(n)
    f = open(output_file, "w")

    mdl = CDTTP2_round_pair_Model.Model(n, f)
    start = time()
    
    sol_pool = generate_solution_pool.generate(mdl.Model)

    end = time()
    f.write("{}秒\n".format(end - start))
    print(end - start,"秒")

    output_all_schedules.output_all_schedules(mdl.Model, sol_pool, n, f)


    f.close()



if __name__ == "__main__":
    main()



