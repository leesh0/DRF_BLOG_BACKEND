from typing import Union


class Link:
    def __init__(self, tg, to=None):
        tgs = tg.split(":")
        self.input = tgs[0]
        self.replace = tgs[1]
        self.move = tgs[2]
        self.to = to

    def __call__(self, t):
        if self.input == t:
            return self
        else:
            return False


class Q:
    links = []

    def __init__(self, name):
        self.name = name

    def add_links(self, *links):
        self.links = links

    def __call__(self, t) -> Union[Link, bool]:
        for link in self.links:
            if link(t):
                return link(t)
        return False


q0 = Q("q0")
q1 = Q("q1")
q2 = Q("q2")
q3 = Q("q3")
q4 = Q("q4")
q5 = Q("q5")
q6 = Q("q6")
q7 = Q("q7")
q8 = Q("q8")
q9 = Q("q9")
q10 = Q("q10")
qf = Q("qf")

q0.add_links(
    Link("1:1':L", to=q1), Link("c:c:L", to=q9), Link("0:0':L", to=q5),
)

q1.add_links(
    Link("1:1:L"), Link("0:0:L"), Link("c:c:L", to=q2)
)

q2.add_links(
    Link("1':1':L"), Link("1:0':L", to=q3), Link("0:1':R", to=q7)
)

q3.add_links(
    Link("1:0:L"), Link("￠:1:L", to=q4), Link("0:1:R", to=q7)
)

q4.add_links(
    Link("B:￠:R", to=q7)
)

q5.add_links(
    Link("1:1:L"), Link("0:0:L"), Link("c:c:L", to=q6)
)

q6.add_links(
    Link("0':0':L"), Link("1':1':L"), Link("0:0':R", to=q7), Link("1:1':R", to=q7)
)

q7.add_links(
    Link("0:0:R"), Link("1:1:R"), Link("0':0':R"), Link("1':1':R"),
    Link("c:c:R", to=q8)
)

q8.add_links(
    Link("0:0:R"), Link("1:1:R"),
    Link("0':0':L", to=q0), Link("1':1':L", to=q0)
)

q9.add_links(
    Link("0:0:R"), Link("1:1:R"), Link("￠:￠:R"), Link("0':0:L"), Link("1':1:L"),
    Link("c:c:R", to=q10)
)

q10.add_links(
    Link("0':0:R"), Link("1':1:R"),
    Link("$:$:L", to=qf)
)


print([f'{l.input}, {l.replace}' for l in q1.links])


def read_tape(tape, st_q, end_q):
    tape_split = tape.split("$")
    tape_l = list(tape_split[0])
    tape_r = list("$")
    ci = tape_l.pop(-1)
    cq = st_q
    eq = end_q
    while True:
        lk = cq(ci)
        if lk and lk.to != eq:
            out = f"{''.join(tape_l)}[{ci}:{cq.name}]{''.join(tape_r[::-1])}"
            print(out)
            if lk.move == "L":
                tape_r.append(lk.replace)
                ci = tape_l.pop(-1)
            else:
                tape_l.append(lk.replace)
                ci = tape_r.pop(-1)
            if lk.to is not None:
                cq = lk.to
        elif lk and lk.to == eq:
            out = f"{''.join(tape_l)}[{ci}:{cq.name}]{''.join(tape_r[::-1])}"
            print(out)
            out = f"{''.join(tape_l)}{lk.replace}{''.join(tape_r[::-1])}"
            arrow = f"{' ' * len(''.join(tape_l))}^"
            end_q_to = f"{' ' * len(''.join(tape_l))}{lk.to.name}"
            print(out)
            print(arrow)
            print(end_q_to)
            print("End TM")
            break
        else:
            out = f"{''.join(tape_l)}[{ci}:{cq.name}]{''.join(tape_r[::-1])}"
            print("ERROR")
            break


read_tape("BB￠010c011$", st_q=q0, end_q=qf)
