import numpy
import pygad
from vns import VNS
from read_graph import read_graph

function_inputs = None # vns
last_fitness = 0


def fitness_func(solution, solution_idx):
    global function_inputs
    print("dmin={} dmax={} prob={:.3f} penalty={:.5f}".format(solution[0], solution[1], solution[2], solution[3]))

    if solution[0] >= solution[1]:
        return 0

    function_inputs.d_min = solution[0]
    function_inputs.d_max_init = solution[1]
    function_inputs.d_max = solution[1]
    function_inputs.prob = solution[2]
    function_inputs.penalty = solution[3]

    output, best_time = function_inputs.run()
    print("-solution={}".format(len(output)))
    fitness = len(function_inputs.graph) - len(output) + 1.0/best_time
    return fitness


def on_generation(ga_instance):
    global last_fitness
    print("Generation = {generation}".format(generation=ga_instance.generations_completed))
    print("Fitness    = {fitness}".format(fitness=ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]))
    print("Change     = {change}".format(change=ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1] - last_fitness))
    last_fitness = ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]


class GASearch():
    def __init__(self, vns, param_space, param_type, num_generations=20, num_parents_mating=5, sol_per_pop=10, mutation_probability=0.1, rseed=12345):
        global function_inputs, last_fitness
        function_inputs = vns
        last_fitness = 0
        self.num_genes = len(param_space)
        self.gene_space = param_space
        self.gene_type = param_type

        self.num_generations = num_generations  # Number of generations.
        self.num_parents_mating = num_parents_mating  # Number of solutions to be selected as parents in the mating pool.
        self.sol_per_pop = sol_per_pop  # Number of solutions in the population.
        self.mutation_probability = mutation_probability
        self.rseed = rseed

    def run(self):
        global function_inputs, desired_output
        self.ga_instance = pygad.GA(num_generations=self.num_generations,
                                    num_parents_mating=self.num_parents_mating,
                                    sol_per_pop=self.sol_per_pop,
                                    num_genes=self.num_genes,
                                    fitness_func=fitness_func,
                                    on_generation=on_generation,
                                    random_seed=self.rseed,
                                    gene_space=self.gene_space,
                                    gene_type=self.gene_type,
                                    mutation_probability=self.mutation_probability
                                    # parallel_processing=['process', 1]
                                    )
        self.ga_instance.run()
        # self.ga_instance.plot_fitness()

        # Returning the details of the best solution.
        solution, solution_fitness, solution_idx = self.ga_instance.best_solution(self.ga_instance.last_generation_fitness)
        print("Parameters of the best solution : {solution}".format(solution=solution))
        print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
        print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))

        if self.ga_instance.best_solution_generation != -1:
            print("Best fitness value reached after {best_solution_generation} generations.".format(best_solution_generation=self.ga_instance.best_solution_generation))

        # Saving the GA instance.
        filename = "results/GASearch/"+vns.instance_name # The filename to which the instance is saved. The name is without extension.
        self.ga_instance.save(filename=filename)
        with open(filename, 'a') as f:
            f.write('{}\n'.format(str(solution)))
        #
        # # Loading the saved GA instance.
        # loaded_ga_instance = pygad.load(filename=filename)
        # loaded_ga_instance.plot_fitness()

        return solution


if __name__ == '__main__':
    instance_dir = 'cities_small_instances'
    instance = 'bath.txt'
    time_limit = 3000
    iteration_max = 1000

    graph_open = instance_dir + '/' + instance
    print("Reading graph!")
    g = read_graph(graph_open)
    print("Creating process: ", graph_open)

    vns = VNS(instance, g, k=4, d_min=1, d_max_init=100, time_limit=time_limit, iteration_max=iteration_max, prob=0.5, penalty=0.01, rseed=12345)

    d_min_space =       {'low': 1, 'high': 10, 'step': 1}
    d_max_init_space =  {'low': 2, 'high': 100, 'step': 1}
    prob_space =        {'low': 0, 'high': 1, 'step': 0.05}
    penalty_space =     {'low': 0.001, 'high': 0.02, 'step': 0.001}

    param_space = [d_min_space, d_max_init_space, prob_space, penalty_space]
    param_type = [int, int, float, float]

    ga = GASearch(vns=vns, param_space=param_space, param_type=param_type)
    res = ga.run()

    print(res)
