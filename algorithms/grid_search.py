import numpy as np
from sklearn import datasets
from vns_estimator import VNS
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
from read_graph import read_graph


def GS(instance_name, graph, k, d_min, d_max, time_limit, iteration_max, prob, penalty, y, rseed):
    param_grid = dict(k=np.array(k),
                      d_min=np.array(d_min),
                      d_max=np.array(d_max),
                      time_limit=np.array(time_limit),
                      iteration_max=np.array(iteration_max),
                      prob=np.array(prob),
                      penalty=np.array(penalty),
                      rseed=np.array(rseed)
                      )

    # create and fit a ridge regression model
    model = VNS()
    grid = GridSearchCV(estimator=model, param_grid=param_grid)
    grid.fit(X, y)

    print(grid.best_score_)


if __name__ == '__main__':
    instance_dir = 'cities_small_instances'
    # instances = ['bath.txt', 'belfast.txt', 'brighton.txt', 'bristol.txt',
    #              'cardiff.txt', 'coventry.txt', 'exeter.txt', 'glasgow.txt']
    instances = ['bath.txt', 'belfast.txt', 'brighton.txt','bristol.txt',
                 'cardiff.txt', 'coventry.txt']
    X = [] # uzorak
    for instance in instances:
        graph_open = instance_dir + '/' + instance
        print("Reading graph!")
        g = read_graph(graph_open)
        X.append(g)
    # y = [71, 76, 40, 72, 78, 72, 76, 93] # opt
    y = [71, 76, 40, 72, 78, 72]  # opt

    GS(instance, X, k=[2], d_min=[1], d_max=[20, 15], time_limit=[10],
       iteration_max=[3900], prob=[0.5], penalty=[0.01],
       rseed=[12345], y=y)