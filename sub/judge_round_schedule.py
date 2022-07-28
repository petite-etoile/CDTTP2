#
# 　　  ⋀_⋀　 
#　　  (･ω･)  
# .／ Ｕ ∽ Ｕ＼
#  │＊　合　＊│
#  │＊　格　＊│ 
#  │＊　祈　＊│ 
#  │＊　願　＊│ 
#  │＊　　　＊│ 
#      ￣
#
import sys
sys.setrecursionlimit(10**6)
input=sys.stdin.readline
from math import floor,sqrt,factorial,hypot,log #log2ないｙｐ
from heapq import heappop, heappush, heappushpop
from collections import Counter,defaultdict,deque
from itertools import accumulate,permutations,combinations,product,combinations_with_replacement
from bisect import bisect_left,bisect_right
from copy import deepcopy
from fractions import gcd
from random import randint
import re


def parse(line):
    i,r,j,ha,*_ = map(int,re.findall(r"\d+", line))
    return i,r,j,ha

def get_team_num(lines):
    
    return max(map(int,lines[2].replace("@","").split()))

def input_all_schedules():
    *lines, = open(0).read().split("\n")
    team_num = get_team_num(lines)
    round_num = (team_num-1)*2

    print(team_num)

    schedule_num = len(lines)//(team_num+1)
    schedules = [[["*"]*round_num for _ in range(team_num)] for _ in range(schedule_num)]


    for i in range(schedule_num):
        for idx in range(2 + i * (team_num+1), 2 + i * team_num + round_num):
            print(lines[idx])
            schedules[i][(idx-2)%team_num] = lines[idx].split()
        print(schedules[i])



    return schedules


def main():
    schedules = input_all_schedules()
    


if __name__ == '__main__':
    main()
