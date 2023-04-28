# k-domination

In this repository you can see the proposed VNS algorithm for solving the k-domination problem. The 𝑘-dominating set 𝐷 of a graph 𝐺 is such a subset of 𝑉 that every vertex not belonging to 𝐷 is adjacent to at least 𝑘 vertices in 𝐷 [1]. You can see more about the problem, the VNS algorithm for the k-dominance problem and comparisons with other algorithms [here](https://github.com/mikiMilan/k-domination/blob/main/doc/gecco_2023_revised.pdf).

## Organization on the repository:
- algorithms - Source code of the VNS algorithm for the k-dominance problem,
- corcoran2021 - The source codes we got from the author of the paper [2],
- doc - The source code of the paper named *Variable neighborhood search for solving the 𝑘-domination problem*,
- instances - Instances that we received from the authors of the paper [2],
- results - Source results of the Grid Search and VNS algorithm for the k-dominance problem.


[1] James K Lan and Gerard Jennhwa Chang. 2013. Algorithmic aspects of the k-domination
problem in graphs. Discrete Applied Mathematics 161, 10-11 (2013),
1513–1520.

[2] Padraig Corcoran and Andrei Gagarin. 2021. Heuristics for k-domination models
of facility location problems in street networks. Computers & Operations Research
133 (2021), 105368.
