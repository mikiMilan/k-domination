import pygad
from vns import VNS
from read_graph import read_graph
from math import inf
import sys
from random import randrange

if len(sys.argv)!=7:
    print("Incorrect usage, please specify <k> <instance_dir> <instance> <time_limit> <iteration_max> <rseed>")
    sys.exit()

k = int(sys.argv[1])
instance_dir = sys.argv[2]
instance = sys.argv[3]
time_limit = int(sys.argv[4])
iteration_max = int(sys.argv[5])
rseed = int(sys.argv[6])

# GA params
num_generations = 50
num_parents_mating = 5
sol_per_pop = 10
mutation_probability = 0.1

last_fitness = -inf

def fitness_func(solution, solution_idx):

    print("dmin={} dmax={} prob={:.3f} penalty={:.5f}".format(solution[0], solution[1], solution[2], solution[3]))

    #return randrange(0, 100000)

    if solution[0] >= solution[1]:
        return -inf

    graph_open = instance_dir + '/' + instance
    print("Reading graph!")
    g = read_graph(graph_open)
    print("Graph created: ", graph_open)
    vns = VNS(instance, g, k=k, d_min=solution[0], d_max_init=solution[1], time_limit=time_limit, iteration_max=iteration_max, prob=solution[2], penalty=solution[3], rseed=rseed)
    
    value, best_time, feasible = vns.run()

    if not feasible:
        print("-solution is not feasible")
        return -inf

    fitness = len(value) + best_time/100000
    return -fitness


def on_generation(ga_instance):
    global last_fitness
    print("Generation = {generation}".format(generation=ga_instance.generations_completed))
    print("Fitness    = {fitness}".format(fitness=ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]))
    print("Change     = {change}".format(change=ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1] - last_fitness))
    last_fitness = ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]


class GASearch():
    def __init__(self, param_space, param_type, num_generations=num_generations, num_parents_mating=num_parents_mating, sol_per_pop=sol_per_pop, mutation_probability=mutation_probability):
        global last_fitness
        self.num_genes = len(param_space)
        self.gene_space = param_space
        self.gene_type = param_type
        last_fitness = -inf
        self.num_generations = num_generations  # Number of generations.
        self.num_parents_mating = num_parents_mating  # Number of solutions to be selected as parents in the mating pool.
        self.sol_per_pop = sol_per_pop  # Number of solutions in the population.
        self.mutation_probability = mutation_probability

    def run(self):
        self.ga_instance = pygad.GA(num_generations=self.num_generations,
                                    num_parents_mating=self.num_parents_mating,
                                    sol_per_pop=self.sol_per_pop,
                                    num_genes=self.num_genes,
                                    fitness_func=fitness_func,
                                    on_generation=on_generation,
                                    random_seed=11111,
                                    gene_space=self.gene_space,
                                    gene_type=self.gene_type,
                                    mutation_probability=self.mutation_probability,
                                    parallel_processing=['process', 10]
                                    )
        self.ga_instance.run()
        #self.ga_instance.plot_fitness()

        # Returning the details of the best solution.
        solution, solution_fitness, solution_idx = self.ga_instance.best_solution(self.ga_instance.last_generation_fitness)
        print("Parameters of the best solution : {solution}".format(solution=solution))
        print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
        print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))

        if self.ga_instance.best_solution_generation != -1:
            print("Best fitness value reached after {best_solution_generation} generations.".format(best_solution_generation=self.ga_instance.best_solution_generation))

        return solution, solution_fitness


if __name__ == '__main__':

    d_min_space =       {'low': 1, 'high': 10, 'step': 1}
    d_max_init_space =  {'low': 2, 'high': 100, 'step': 1}
    prob_space =        {'low': 0, 'high': 1, 'step': 0.05}
    penalty_space =     {'low': 0.001, 'high': 0.02, 'step': 0.001}

    param_space = [d_min_space, d_max_init_space, prob_space, penalty_space]
    param_type = [int, int, float, float]

    ga = GASearch(param_space=param_space, param_type=param_type)
    sol, sol_fit = ga.run()

    print(sol)
    print(sol_fit)

    fname = 'all_{}_{}_{}_{}.txt'.format(num_generations, num_parents_mating, sol_per_pop, mutation_probability)
    with open('results/GASearch/'+fname, 'a') as f:
        f.write('inst={}\tk={}\tit_max={}\tvns_seed={}\tparams={}\tfit={}\n'.format(instance, k, iteration_max, rseed, sol, sol_fit))
