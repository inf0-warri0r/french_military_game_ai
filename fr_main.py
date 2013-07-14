"""
Author : tharindra galahena (inf0_warri0r)
Project: french military game using tempreal difference learning
Blog   : http://www.inf0warri0r.blogspot.com
Date   : 14/07/2013
License:

     Copyright 2013 Tharindra Galahena

This is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. This is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

* You should have received a copy of the GNU General Public License along with
this. If not, see http://www.gnu.org/licenses/.

"""

from Tkinter import *
import copy
import random


graph = [
        [3, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [2, 3, 1, 0, 1, 1, 0, 0, 0, 0, 0],
        [2, 1, 3, 1, 0, 1, 0, 0, 0, 0, 0],
        [2, 0, 1, 3, 0, 1, 1, 0, 0, 0, 0],
        [0, 2, 0, 0, 3, 1, 0, 1, 0, 0, 0],
        [0, 2, 2, 2, 1, 3, 1, 1, 1, 1, 0],
        [0, 0, 0, 2, 0, 1, 3, 0, 0, 1, 0],
        [0, 0, 0, 0, 2, 2, 0, 3, 1, 0, 1],
        [0, 0, 0, 0, 0, 2, 0, 1, 3, 1, 1],
        [0, 0, 0, 0, 0, 2, 2, 0, 1, 3, 1],
        [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 3]
    ]


class state:
    def __init__(self):
        self.ai = 0
        self.p1 = 0
        self.p2 = 0
        self.p3 = 0


class game:

    def __init__(self, st):
        self.current_state = st
        self.a = random.uniform(-10.0, 10.0)
        self.b = random.uniform(0.0, 10.0)
        self.c = random.uniform(-10.0, 10.0)
        self.d = random.uniform(-10.0, 10.0)
        self.r = 0.9
        self.learnng_rate = 0.5

    def get_ai_moves(self, st):
        moves = list()
        for i in range(0, 11):
            if graph[st.ai][i] == 1 or graph[st.ai][i] == 2:
                if i != st.p1:
                    if i != st.p2:
                        if i != st.p3:
                            moves.append(i)
        return moves

    def get_human_moves(self, st):
        moves1 = list()
        moves2 = list()
        moves3 = list()
        for i in range(0, 11):
            if graph[st.p1][i] == 1:
                if i != st.ai:
                    if i != st.p2:
                        if i != st.p3:
                            moves1.append(i)

        for i in range(0, 11):
            if graph[st.p2][i] == 1:
                if i != st.ai:
                    if i != st.p1:
                        if i != st.p3:
                            moves2.append(i)

        for i in range(0, 11):
            if graph[st.p3][i] == 1:
                if i != st.ai:
                    if i != st.p1:
                        if i != st.p2:
                            moves3.append(i)

        return moves1, moves2, moves3

    def get_nearest_dot(self, st):
        f = True
        for i in range(0, 11):
            if graph[st.ai][i] == 1 or graph[st.ai][i] == 2:
                if i == st.p1 or i == st.p2 or i == st.p3:
                    return 1

        if f:
            moves = self.get_ai_moves(st)
            for move in moves:
                for i in range(0, 11):
                    if graph[move][i] == 1 or graph[move][i] == 2:
                        if i == st.p1 or i == st.p2 or i == st.p3:
                            return 2
            return 3

    def find_v(self, tmp):
        ms = self.get_ai_moves(tmp)
        v = 0.0
        ia = (float(len(ms)) + 1.0) / 7.0
        ib = 0.0
        ic = 0.0
        ie = 1.0
        if tmp.ai in [8]:
            ie = 0.5

        if tmp.ai == 0:
            ib = 16.0 / 16.0
        elif tmp.ai > 0 and tmp.ai < 4:
            ib = 8.0 / 16.0
        elif tmp.ai > 3 and tmp.ai < 7:
            ib = 4.0 / 16.0
        elif tmp.ai > 6 and tmp.ai < 10:
            ib = 2.0 / 16.0
        elif tmp.ai == 10:
            ib = 1.0 / 16.0

        ic = float(self.get_nearest_dot(tmp)) / 3.0

        v = self.a * ia + self.b * ib + self.c * ic + self.d * ie

        return v, ia, ib, ic, ie

    def find_move(self, st):
        moves = self.get_ai_moves(st)
        mx = -10000
        mv = st.ai
        if len(moves) == 0:
            mx, ma, mb, mc, me = self.find_v(st)
        else:
            ma = 0
            mb = 0
            mc = 0
            me = 0
            for move in moves:
                tmp = copy.deepcopy(st)
                tmp.ai = move
                v, ia, ib, ic, ie = self.find_v(tmp)
                v = self.r * v
                if tmp.ai == 0:
                    v = v + 1000
                elif ia == 1.0 / 7.0:
                    v = v - 1000

                if mx < v:
                    mx = v
                    mv = tmp.ai
                    ma = ia
                    mb = ib
                    mc = ic
                    me = ie
        return mv, mx, ma, mb, mc, me

    def learn(self, st, v, ia, ib, ic, ie):
        v2, a, b, c, d = self.find_v(st)
        v2 = v2 * self.r
        if st.ai == 0.0:
            v2 = v2 + 1000
        elif a == 1.0 / 7.0:
            v2 = v2 - 1000
        self.a = self.a - self.learnng_rate * (v2 - v) * ia
        self.b = self.b - self.learnng_rate * (v2 - v) * ib
        self.c = self.c - self.learnng_rate * (v2 - v) * ic
        self.d = self.d - self.learnng_rate * (v2 - v) * ie

st = state()

st.ai = 5
st.p1 = 0
st.p2 = 1
st.p3 = 3

g = game(st)

root = Tk()
root.title("french military game - inf0_warri0r")

cw = 300
ch = 400

chart_1 = Canvas(root, width=cw, height=ch, background="black")
chart_1.grid(row=0, column=0)

pos = [
    (150, 325),
    (75, 265),
    (150, 265),
    (225, 265),
    (75, 190),
    (150, 190),
    (225, 190),
    (75, 115),
    (150, 115),
    (225, 115),
    (150, 55)
    ]

selected_player = -1
current = -1

mx = 0
ia = 0
ib = 0
ic = 0
ie = 0
s = 0


def callback(event):
    global current
    global selected_player
    global g, mx, ia, ib, ic, ie, s

    chart_1.focus_set()
    for i in range(0, 11):
        if pos[i][0] - 5 <= event.x:
            if pos[i][0] + 5 >= event.x:
                if pos[i][1] - 5 <= event.y:
                    if pos[i][1] + 5 >= event.y:

                        if g.current_state.p1 == i:
                            selected_player = 1
                        elif  g.current_state.p2 == i:
                            selected_player = 2
                        elif  g.current_state.p3 == i:
                            selected_player = 3
                        else:
                            current = i
                        return 0
    if event.x < 20 and event.x > 5:
        if event.y < 20 and event.y > 5:
            selected_player = -1
            current = -1
            mx = 0
            ia = 0
            ib = 0
            ic = 0
            ie = 0
            g.current_state.ai = 5
            g.current_state.p1 = 0
            g.current_state.p2 = 1
            g.current_state.p3 = 3
            s = 0

chart_1.bind("<Button-1>", callback)

sa = 0
sh = 0

while 1:

    chart_1.create_rectangle(5, 5, 20, 20, fill='red')
    chart_1.create_text(12, 12, text="R", fill='white')
    chart_1.create_line(pos[0][0], pos[0][1], pos[10][0], pos[10][1],
                        fill='red')
    chart_1.create_line(pos[1][0], pos[1][1], pos[7][0], pos[7][1],
                        fill='red')
    chart_1.create_line(pos[3][0], pos[3][1], pos[9][0], pos[9][1],
                        fill='red')

    chart_1.create_line(pos[1][0], pos[1][1], pos[3][0], pos[3][1],
                        fill='red')
    chart_1.create_line(pos[4][0], pos[4][1], pos[6][0], pos[6][1],
                        fill='red')
    chart_1.create_line(pos[7][0], pos[7][1], pos[9][0], pos[9][1],
                        fill='red')

    chart_1.create_line(pos[0][0], pos[0][1], pos[1][0], pos[1][1],
                        fill='red')
    chart_1.create_line(pos[0][0], pos[0][1], pos[3][0], pos[3][1],
                        fill='red')

    chart_1.create_line(pos[1][0], pos[1][1], pos[9][0], pos[9][1],
                        fill='red')
    chart_1.create_line(pos[3][0], pos[3][1], pos[7][0], pos[7][1],
                        fill='red')

    chart_1.create_line(pos[10][0], pos[10][1], pos[7][0], pos[7][1],
                        fill='red')
    chart_1.create_line(pos[10][0], pos[10][1], pos[9][0], pos[9][1],
                        fill='red')

    for p in pos:
        chart_1.create_oval(p[0] - 5, p[1] - 5,
                            p[0] + 5, p[1] + 5,
                            fill='yellow')

    chart_1.create_oval(pos[g.current_state.ai][0] - 10,
                        pos[g.current_state.ai][1] - 10,
                        pos[g.current_state.ai][0] + 10,
                        pos[g.current_state.ai][1] + 10,
                        fill='red')

    chart_1.create_oval(pos[g.current_state.p1][0] - 10,
                        pos[g.current_state.p1][1] - 10,
                        pos[g.current_state.p1][0] + 10,
                        pos[g.current_state.p1][1] + 10,
                        fill='green')

    chart_1.create_oval(pos[g.current_state.p2][0] - 10,
                        pos[g.current_state.p2][1] - 10,
                        pos[g.current_state.p2][0] + 10,
                        pos[g.current_state.p2][1] + 10,
                        fill='green')

    chart_1.create_oval(pos[g.current_state.p3][0] - 10,
                        pos[g.current_state.p3][1] - 10,
                        pos[g.current_state.p3][0] + 10,
                        pos[g.current_state.p3][1] + 10,
                        fill='green')

    st = "Score AI = " + str(sa) + " Human = " + str(sh)
    chart_1.create_text(150, 350, text=st, fill='white')

    if selected_player != -1:
        if selected_player == 1:
            i = g.current_state.p1
        elif selected_player == 2:
            i = g.current_state.p2
        else:
            i = g.current_state.p3

        chart_1.create_oval(pos[i][0] - 10, pos[i][1] - 10,
                            pos[i][0] + 10, pos[i][1] + 10,
                            fill='blue')
    if current != -1:
        i = current

        if selected_player == 1:
            j = g.current_state.p1
        elif selected_player == 2:
            j = g.current_state.p2
        else:
            j = g.current_state.p3

        if graph[j][i] == 1 and g.current_state.ai != i:
            if selected_player == 1:
                g.current_state.p1 = i
            elif selected_player == 2:
                g.current_state.p2 = i
            else:
                g.current_state.p3 = i
            selected_player = -1
            current = -1
            if s > 0:
                g.learn(g.current_state, mx, ia, ib, ic, ie)
            else:
                s = 1
            mv, mx, ia, ib, ic, ie = g.find_move(g.current_state)
            if mv != g.current_state.ai:
                g.current_state.ai = mv
            else:
                g.current_state.ai = 5
                g.current_state.p1 = 0
                g.current_state.p2 = 1
                g.current_state.p3 = 3
                g.learn(g.current_state, mx, ia, ib, ic, ie)
                s = 0
                sh = sh + 1
            if mv == 0:
                g.current_state.ai = 5
                g.current_state.p1 = 0
                g.current_state.p2 = 1
                g.current_state.p3 = 3
                g.learn(g.current_state, mx, ia, ib, ic, ie)
                s = 0
                sa = sa + 1
        else:
            current = -1

    chart_1.update()
    chart_1.after(20)

    chart_1.delete(ALL)
root.mainloop()
