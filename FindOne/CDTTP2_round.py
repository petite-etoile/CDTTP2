from docplex.mp import model, conflict_refiner
import os
import re
import sys

# import tkinter as tk
# from tkinter import ttk
from time import time

from datetime import datetime

sys.path.append(os.path.pardir)
from Model import CDTTP2_round_Model 

from cplex.exceptions import CplexError, CplexSolverError

def main():
    
    n = int(sys.argv[1])

    year, month, date, hour, minute, second, *_ = re.split("[ .:-]", str(datetime.now()))
    output_file = "result_round/n{:0>2}_{:0>4}年{:0>2}月{:0>2}日{:0>2}時{:0>2}分{:0>2}秒.text".format(n, year, month, date, hour, minute, second)
    f = open(output_file, "a")

    try:
        Model = CDTTP2_round_Model.Model(n, f)
        
        # CR = conflict_refiner.ConflictRefiner()
        # conflict_result = CR.refine_conflict(Model.Model)
        # conflict_result.display()


        start = time()
        Model.solve()
        end = time()
        Model.print_solution_values()
        Model.print_objective_value()
        print(end - start,"秒")
        f.write("{}秒\n".format(end - start))

        Model.output_schdule(end-start)
    except CplexSolverError:
        f.write("だめでした\n")


    f.close()




if __name__ == "__main__":
    main()



