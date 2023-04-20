import numpy
import pygad
from vns import VNS

function_inputs = [4, -2, 3.5, 5, -11, -4.7]
desired_output = 44
last_fitness = 0


def fitness_func(solution, solution_idx):
    global function_inputs, desired_output
    print("--", solution)
    solution[0] = int(solution[0])
    output = numpy.sum(solution * function_inputs)
    fitness = 1.0 / (numpy.abs(output - desired_output) + 0.000001)
    return fitness


def on_generation(ga_instance):
    global last_fitness
    print("Generation = {generation}".format(generation=ga_instance.generations_completed))
    print("Fitness    = {fitness}".format(fitness=ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]))
    print("Change     = {change}".format(change=ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1] - last_fitness))
    last_fitness = ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]


class GASearch():
    def __init__(self, inputs, output, num_generations=100, num_parents_mating=10, sol_per_pop=20, rseed=2):
        global function_inputs, desired_output
        function_inputs = inputs
        desired_output = output
        self.num_generations = num_generations  # Number of generations.
        self.num_parents_mating = num_parents_mating  # Number of solutions to be selected as parents in the mating pool.
        self.sol_per_pop = sol_per_pop  # Number of solutions in the population.
        self.num_genes = len(function_inputs)
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
                                    gene_space=[
                                        {'low':-1, 'high': 4, 'step':1},
                                        {'low':1, 'high': 2, 'step':0.2},
                                        {'low': 1, 'high': 2, 'step': 0.2},
                                        {'low': 1, 'high': 2, 'step': 0.2},
                                        {'low': 1, 'high': 2, 'step': 0.2},
                                        {'low': 1, 'high': 2, 'step': 0.2},
                                    ],
                                    gene_type=[int, float, float, float, float, float],
                                    mutation_probability = 0.1
                                    )
        self.ga_instance.run()
        self.ga_instance.plot_fitness()

        # Returning the details of the best solution.
        solution, solution_fitness, solution_idx = self.ga_instance.best_solution(self.ga_instance.last_generation_fitness)
        print("Parameters of the best solution : {solution}".format(solution=solution))
        print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
        print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))

        prediction = numpy.sum(numpy.array(function_inputs)*solution)
        print("Predicted output based on the best solution : {prediction}".format(prediction=prediction))

        if self.ga_instance.best_solution_generation != -1:
            print("Best fitness value reached after {best_solution_generation} generations.".format(best_solution_generation=self.ga_instance.best_solution_generation))

        # # Saving the GA instance.
        # filename = 'genetic' # The filename to which the instance is saved. The name is without extension.
        # ga_instance.save(filename=filename)
        #
        # # Loading the saved GA instance.
        # loaded_ga_instance = pygad.load(filename=filename)
        # loaded_ga_instance.plot_fitness()


if __name__ == '__main__':
    ga = GASearch(inputs=[4, -2, 3.5, 5, -11, -4.7], output=44)
    ga.run()
