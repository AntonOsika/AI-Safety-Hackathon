from learner import distribute
from learner import gen_conditions


def test_distribute():
    s = list(x for x in distribute(0, 5, 5))
    assert len(s) == 1
    assert s[0] == [0, 0, 0, 0, 0]

    s = list(x for x in distribute(1, 5, 5))
    assert len(s) == 5
    assert s[0] == [1, 0, 0, 0, 0]
    assert s[-1] == [0, 0, 0, 0, 1]

    s = list(x for x in distribute(2, 5, 5))
    assert len(s) == 15
    assert s[0] == [2, 0, 0, 0, 0]
    assert s[-1] == [0, 0, 0, 0, 2]

    s = list(x for x in distribute(1, 5, 0))
    assert len(s) == 0

    s = list(x for x in distribute(1, 0, 1))
    assert len(s) == 0



def test_gen_conditions():
    conds = list(gen_conditions())
    print(len(set(tuple(x) for x in conds)))
    assert len(conds) == 5*5*11
