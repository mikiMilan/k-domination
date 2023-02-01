import numpy as np
from vns_estimator import VNS
from sklearn.model_selection import GridSearchCV
from read_graph import read_graph
from sklearn.metrics import accuracy_score, r2_score
from sklearn.model_selection import train_test_split
from model_estimator import TemplateEstimator


def GS(X, y, k, d_min, d_max, time_limit, iteration_max, prob, penalty):
    param_grid = dict(k=np.array(k),
                      d_min=np.array(d_min),
                      d_max=np.array(d_max),
                      time_limit=np.array(time_limit),
                      iteration_max=np.array(iteration_max),
                      prob=np.array(prob),
                      penalty=np.array(penalty)
                      )

    # create and fit a ridge regression model
    model = VNS()
    grid = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        scoring=r2_score
    )
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
    grid.fit(X_train, y_train)

    print(grid.best_score_)
    print(grid.best_params_)

    # grid.score(X_test, y_test)


if __name__ == '__main__':
    instance_dir = 'cities_small_instances'
    # instances = ['bath.txt', 'belfast.txt', 'brighton.txt', 'bristol.txt',
    #              'cardiff.txt', 'coventry.txt', 'exeter.txt', 'glasgow.txt']
    instance = 'bath.txt'
    graph_open = instance_dir + '/' + instance
    print("Reading graph!")
    g = read_graph(graph_open)

    X = [] # uzorak
    n_samples = 10
    for i in range(n_samples):
        X.append([g, i, instance])

    y = [71] * n_samples  # opt k=2

    GS(X, y, k=[2], d_min=[1], d_max=[20, 15], time_limit=[1],
       iteration_max=[3900], prob=[0.5], penalty=[0.01])