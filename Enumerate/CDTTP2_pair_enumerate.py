from docplex.mp import model 
import os
import re
import sys

from time import time

from datetime import datetime

sys.path.append(os.pardir)
from sub import generate_solution_pool
from Model import CDTTP2_pair_Model 


def main():
    
    n = int(sys.argv[1])

    year, month, date, hour, minute, second, *_ = re.split("[ .:-]", str(datetime.now()))
    output_file = "default_result_all/n{:0>2}_{:0>4}年{:0>2}月{:0>2}日{:0>2}時{:0>2}分{:0>2}秒.text".format(n, year, month, date, hour, minute, second)
    f = open(output_file, "w")

    mdl = CDTTP2_pair_Model.Model(n, f)
    start = time()
    generate_solution_pool.generate(mdl.Model)
    end = time()
    print(end - start,"秒")
    # f.write("{}秒\n".format(end - start))

    # mdl.output_schdule(end-start)

    f.close()



if __name__ == "__main__":
    main()



