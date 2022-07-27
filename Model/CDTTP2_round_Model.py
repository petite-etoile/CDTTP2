from docplex.mp import model 
import os

# ペア制約のみ追加したCDTTP2モデル
class Model:
    def __init__(self, n:int, f):
        self.n = n
        self.build(n)
        self.schedule = [ ["#"]*(2*(self.n-1)) for _ in range(self.n) ]
        self.f = f

    def build(self, n:int):
        self.Model = model.Model()
        self.Model.context.cplex_parameters.threads = os.cpu_count()

        self.teams = range(1, n+1)
        self.rounds = range(1, 2*(n-1)+1)
        self.HomeAway = range(2)

        #変数宣言
        self.Model.keys = self.get_keys(n)
        self.Model.vars = self.Model.binary_var_dict( keys = self.Model.keys, name = "x", key_format = "(%s)" )

        #制約
        self.add_constraints1()
        self.add_constraints2()
        self.add_constraints3()
        self.add_constraints4()
        self.add_constraints5()
        self.add_constraints6()
        self.add_constraints7()
        self.add_constraints8()
        # self.add_constraints9()
        self.add_constraints10()
        # self.Model.add_constraint(self.Model.vars[1,1,2,1] == 1) 


        #目的関数値
        obj_expr = self.get_obj_expr()
        self.Model.maximize(obj_expr)

    def get_obj_expr(self):
        expr = self.Model.linear_expr()

        for i in self.teams:
            for r in self.rounds[:-1]:
                for ha in range(2):
                    expr.add( self.Model.vars[-i,-r,-ha] )
                    
        return expr
        
    def solve(self):
        self.Model.solve()

        self.represent_schdule()

    def get_keys(self, n):
        keys = []

        # x_{i,r,j,ha}
        for i in self.teams:
            for r in self.rounds:
                for j in self.teams:
                    for ha in range(2): # home/away. iff ha is 0, i's home game.
                        keys.append((i,r,j,ha))
            
        # z_{i,r,ha}
        for i in self.teams:
            for r in self.rounds[:-1]:
                for ha in range(2): # home/away. iff ha is 0, i's home game.
                    keys.append((-i,-r,-ha))

        # z_{i,j,i',j'}
        for i in self.teams:
            for j in self.teams:
                for i_ in self.teams:
                    for j_ in self.teams:
                        if(len(set((i,j,i_,j_))) != 4):
                            continue
                        keys.append((-i,-j,-i_,-j_))

        return keys

    #i (\in X) が 1スロットに何戦やるかを表す式
    def get_expr_game_count_on_round_of_team(self, i:int, r:int): 
        expr = self.Model.linear_expr()
        for j in self.teams:
            for ha in self.HomeAway:
                expr.add( self.Model.vars[i,r,j,ha] )
        return expr

    #各チーム1スロットにちょうど1試合
    def add_constraints1(self):
        for i in self.teams:
            for r in self.rounds:
                self.Model.game_count_on_round_of_team = self.get_expr_game_count_on_round_of_team(i, r)
                self.Model.add_constraint(self.Model.game_count_on_round_of_team == 1) 

    #2連続スロットのi vs jの試合数を表す式
    def get_expr_count_continuous_on_2rounds(self, i, j, r):
        expr = self.Model.linear_expr()
        for ha in self.HomeAway:
            expr.add( self.Model.vars[i, r, j, ha] + self.Model.vars[i, r + 1, j, ha] )
        return expr

    #No Repeater
    def add_constraints2(self):
        for i in self.teams:
            for j in self.teams:
                for r in self.rounds[:-1]:
                    self.Model.count_continuous_on_2rounds = self.get_expr_count_continuous_on_2rounds(i, j, r)
                    self.Model.add_constraint(self.Model.count_continuous_on_2rounds <= 1)

    #3スロットの中での Home Standあるいは Road Tripの長さ
    def get_expr_count_continuous_HomeAway_on_3rounds_of_team(self, i, r, ha):
        expr = self.Model.linear_expr()
        for j in self.teams:
            expr.add( self.Model.vars[i, r, j, ha] + self.Model.vars[i, r + 1, j, ha] + self.Model.vars[i, r + 2, j, ha] )
        return expr

    #AtMost2制約
    def add_constraints3(self):
        for i in self.teams:
            for r in self.rounds[:-2]:
                for ha in self.HomeAway:
                    self.Model.count_continuous_HomeAway_on_3rounds_of_team = self.get_expr_count_continuous_HomeAway_on_3rounds_of_team(i, r, ha)
                    self.Model.add_constraint(self.Model.count_continuous_HomeAway_on_3rounds_of_team <= 2)

    # i vs j が ha(Home/Away)で戦う回数を表す式
    def get_expr_count_i_vs_j_ha(self, i, j, ha):
        expr = self.Model.linear_expr()
        for r in self.rounds:
            expr.add( self.Model.vars[i, r, j, ha])
        return expr

    #i vs j はiのホームで1戦, jのホームで1戦
    def add_constraints4(self):
        for i in self.teams:
            for j in self.teams:
                if(i==j):
                    continue
                for ha in self.HomeAway:
                    self.Model.count_i_vs_j_ha = self.get_expr_count_i_vs_j_ha(i, j, ha)
                    self.Model.add_constraint(self.Model.count_i_vs_j_ha == 1)

    # i vs jの整合性 を確認する式
    def get_expr_ivsj_diff(self, i, r, j):
        expr = self.Model.linear_expr()
        expr.add( self.Model.vars[i,r,j,1] - self.Model.vars[j,r,i,0])
        return expr

    # iがjとホーム(アウェイ)で戦うとき, jがiとアウェイ(ホーム)で戦う
    def add_constraints5(self):
        for i in self.teams:
            for j in self.teams:
                for r in self.rounds:
                    self.Model.ivsj_diff = self.get_expr_ivsj_diff(i, r, j)
                    self.Model.add_constraint(self.Model.ivsj_diff == 0)

    # チームiがラウンドrにホーム(アウェイ)で対戦するか
    def get_expr_i_play_on_r_at_ha(self, i, r, ha):
        expr = self.Model.linear_expr()
        for j in self.teams:
            expr.add( self.Model.vars[i, r, j, ha])
        return expr
        
    def get_expr_upper_of_z(self, i, r, ha):
        expr = self.Model.linear_expr()
        for j in self.teams:
            expr.add( self.Model.vars[i, r, j, ha] + self.Model.vars[i, r+1, j, ha])
        expr.add( -1 )
        return expr
        
    # z_{i,r,ha}=\sigma(x_{i,r,j,ha}) * \sigma(x_{i,r+1,j,ha})
    def add_constraints6(self):
        for i in self.teams:
            for r in self.rounds[:-1]:
                for ha in range(2):
                    self.Model.play_on_r = self.get_expr_i_play_on_r_at_ha(i, r, ha)
                    self.Model.play_on_r_plus_1 = self.get_expr_i_play_on_r_at_ha(i, r+1, ha)

                    self.Model.add_constraint( self.Model.vars[-i,-r,-ha] <= self.Model.play_on_r )
                    self.Model.add_constraint( self.Model.vars[-i,-r,-ha] <= self.Model.play_on_r_plus_1 )
                    
                    self.Model.upper_of_z = self.get_expr_upper_of_z(i, r, ha)
                    self.Model.add_constraint( self.Model.vars[-i,-r,-ha] >= self.Model.upper_of_z )

    #break数はn^2 - 2n
    def add_constraints7(self):
        self.Model.break_num = self.get_obj_expr()
        self.Model.add_constraint(self.Model.break_num >= self.n ** 2 - self.n*2 - 1)

    # 前半のチームの最初のラウンド, Away Game
    def add_constraints8(self):
        for i in self.teams:
            if(i&1):
                j=i+1
                self.Model.add_constraint(self.Model.vars[i,1,j,1] == 1) 
                
    # 制約B
    def add_constraints9(self):
        for r in self.rounds:
            for t1 in self.teams[::2]:
                for t2 in self.teams:
                    if(t1+1==t2 or t1==t2):
                        continue
                    t1_2 = t1+1
                    t2_2 = t2+1 if t2&1 else t2-1
                    self.Model.add_constraint(self.Model.vars[t1,r,t2,0] ==  self.Model.vars[t1_2,r,t2_2,1])
                    self.Model.add_constraint(self.Model.vars[t1,r,t2,1] ==  self.Model.vars[t1_2,r,t2_2,0])

    # ラウンド補ラウンド制約
    def add_constraints10(self):
        for r in self.rounds:
            for t1 in self.teams:
                for t2 in self.teams:
                    for t1_ in self.teams:
                        for t2_ in self.teams:
                            if(len(set((t1,t2,t1_,t2_))) != 4):
                                continue
                            print((t1,t2), (t1_,t2_))
                            self.Model.add_constraint(
                                self.Model.vars[t1, r, t2, 0] + self.Model.vars[t1, r, t2, 1]
                                + self.Model.vars[t1_, r, t2_, 0] + self.Model.vars[t1_, r, t2_, 1]
                                - 1 <= self.Model.vars[-t1, -t2, -t1_, -t2_]
                            )

                            self.Model.add_constraint(
                                self.Model.vars[t1, r, t2, 0] + self.Model.vars[t1, r, t2, 1]
                                >= self.Model.vars[-t1, -t2, -t1_, -t2_]
                            )

                            self.Model.add_constraint(
                                self.Model.vars[t1_, r, t2_, 0] + self.Model.vars[t1_, r, t2_, 1]
                                >= self.Model.vars[-t1, -t2, -t1_, -t2_]
                            )
                    


    def print_solution_value(self, i, r, j, ha):
        print("x({:0>2},{:0>2},{:0>2},{:0>2}) : {}".format(i,r,j,ha,self.Model.vars[i,r,j,ha].solution_value))

    def fprint_solution_value(self, i, r, j, ha):
        self.f.write("x({:0>2},{:0>2},{:0>2},{:0>2}) : {}\n".format(i,r,j,ha,self.Model.vars[i,r,j,ha].solution_value))

    def print_solution_z_value(self, i, r, ha):
        print("z({:0>2},{:0>2},{:0>2}) : {}".format(i,r,ha,self.Model.vars[-i,-r,-ha].solution_value))

    def fprint_solution_z_value(self, i, r, ha):
        self.f.write("z({:0>2},{:0>2},{:0>2}) : {}\n".format(i,r,ha,self.Model.vars[-i,-r,-ha].solution_value))


    def print_solution_values(self):
        for i in self.teams:
            for r in self.rounds:
                for j in self.teams:
                    for ha in self.HomeAway:
                        value = self.Model.vars[i,r,j,ha].solution_value
                        if(value):
                            self.print_solution_value(i, r, j, ha)
                            self.fprint_solution_value(i, r, j, ha)
        for i in self.teams:
            for r in self.rounds[:-1]:
                for ha in self.HomeAway:
                    value = self.Model.vars[-i,-r,-ha].solution_value
                    if(value):
                        self.print_solution_z_value(i, r, ha)
                        self.fprint_solution_z_value(i, r, ha)

    def print_objective_value(self):
        obj_value = 0
        for i in self.teams:
            for r in self.rounds[:-1]:
                for ha in self.HomeAway:
                    obj_value += self.Model.vars[-i,-r,-ha].solution_value
        print("最適値:{}".format(obj_value))
        self.f.write("最適値:{}\n".format(obj_value))
    
        

    def represent_schdule(self):
        for i in self.teams:
            for r in self.rounds:
                for j in self.teams:
                    for ha in self.HomeAway:
                        value = self.Model.vars[i,r,j,ha].solution_value
                        if(value):
                            self.schedule[i-1][r-1] = "{}{}".format("@" if ha else " ", j)

    def output_schdule(self,sec):
        for row in self.schedule:
            for a in row:
                self.f.write("{:>4}".format(a))
            self.f.write("\n")
