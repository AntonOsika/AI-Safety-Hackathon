# Reversibility

This is a project that implements an attempt at solving the problem of "avoiding side effects" as well as "safe exploration" in a very environment agnostic manner, i.e. being able to generalize to new environments.
It is based on an agent that has an inductive bias similar to the universal prior of [AIXI](https://arxiv.org/pdf/cs/0004001.pdf).

The agent is a practical implementation of AIXI that does an efficient search of laws of physics in the
observed environment finding a minimal set that explains all observed history. It
then reasons about what actions are reversible, i.e. actions that do:
1. Safe exploration
2. Whose side effects are always reversible –– which in essence excludes all
undesireable side effects according to human values

## Installation:

```bash
git clone --recursive https://github.com/antonosika/ai-safety-hackathon
cd pycolab
pip install -e .
cd ../reversibility
python learner.py
```

