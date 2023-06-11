# Reversibility

This is a project that implements an attempt at solving the problem of "avoiding side effects" as well as "safe exploration" in a very environment agnostic manner, i.e. being able to generalize to new environments.
It is based on an agent that has an inductive bias similar to the universal prior of [AIXI](https://arxiv.org/pdf/cs/0004001.pdf).

Since this is a small environment, the agent is a practical implementation of AIXI that does a search of laws of physics in the
observed environment finding a minimal set that explains all observed history. It
then reasons about what actions are reversible, i.e. actions that do:
1. Safe exploration
2. Have side effects are always reversible –– and thus excludes undesireable side effects according to human values


## Post hackathon work

I took this project further after the hackathon and presented it at the AI Safety ([slides](https://www.slideshare.net/antonosika/causal-spacetime-pattern-search-for-safe-planning)).
![image](https://github.com/AntonOsika/AI-Safety-Hackathon/assets/4467025/65e9a360-996f-4d9a-8159-e907efa05203)


## Installation:

```bash
git clone --recursive https://github.com/antonosika/ai-safety-hackathon
cd pycolab
pip install -e .
cd ../reversibility
python learner.py
```

