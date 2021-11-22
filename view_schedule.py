import tkinter as tk
from tkinter import ttk
import re

class TreeView(ttk.Frame): 
    def __init__(self, master):
        super().__init__(master, height = 900)
        self.pack(anchor = tk.CENTER)

    def create_widgets(self, columns, datas):
        self.tree = ttk.Treeview(self, columns = columns, height = 900)
        self.tree.pack(anchor = tk.CENTER)
        
        # self.tree.heading("#0")

        self.tree.column("#0", anchor = tk.CENTER, width = 50)

        self.set_columns(columns)
        self.set_datas(datas)

    def set_columns(self, columns):
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor = tk.CENTER, width = 40)

    def set_row(self, index = "", row_data = []):
        self.tree.insert("", index = "end", text = index, values = row_data)

    def set_datas(self, datas):
        for i,data in enumerate(datas, start = 1):
            self.set_row(i, data)




def parse(line):
    i,r,j,ha,*_ = map(int,re.findall(r"\d+", line))
    return i,r,j,ha

def get_team_num(lines):
    round_num = max([max(map(int, re.findall(r"\d+", line))) for line in lines   if line and line[0]=="x"])
    return (round_num + 2) // 2

def input_schedule():
    *lines, = open(0).read().split("\n")
    team_num = get_team_num(lines)
    round_num = (team_num-1)*2

    schedule = [["*"]*(round_num) for _ in range(team_num)]

    for line in lines:
        if(line == "" or line[0] != "x"):
            continue
        team_i,round_,team_j,homeaway = parse(line)
        schedule[team_i-1][round_-1] = "{}{}".format("@" if homeaway else " ", team_j)
    return schedule

def get_break_num(schedule):
    res = 0
    for i,row in enumerate(schedule):
        for r,_ in enumerate(row[:-1]):
            if(not ((row[r][0] == "@") ^ (row[r+1][0] == "@"))):
                res += 1
    return res

def view_schedule(schedule):
    n = len(schedule)
    break_num = get_break_num(schedule)

    root = tk.Tk()
    root.title("CDTTP(2) n={} break数:{}".format(n, break_num))

    root.geometry("2400x900+100+100")
    table = TreeView( root )

    columns = [i for i in range(1, (2 * (n - 1)) + 1)]

    table.create_widgets(columns, schedule)
    root.mainloop()




def main():
    
    schedule = input_schedule()
    view_schedule(schedule)


if __name__ == "__main__":
    main()



