"""GA_supervisor controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Supervisor, Keyboard, Emitter, Receiver
import numpy as np
from new_GA import *

# create the supervisor instance.
my_supervisor = Supervisor()
TIMESTEP = 32
# TIMESTEP = int(my_supervisor.getBasicTimeStep())
my_supervisor.step(TIMESTEP)
## Robot node that I created
my_robot_node = my_supervisor.getFromDef("ROBOT_1")

## The emitter to send genotype to my_robot
emitter = my_supervisor.getDevice("emitter")
emitter.setChannel(1)

receiver = my_supervisor.getDevice("receiver")
receiver.enable(TIMESTEP)
receiver.setChannel(2)

## Establish Sync between emitter and receiver

POPULATION_SIZE = 10
GENOTYPE_SIZE = 10
NUM_GENERATIONS = 100
## Weighs, bias bounds
weights_bias_range = np.arange(-5, 5, 0.5)

def run_seconds(t, reset_position = False):
    """
        Simulation time.
    """
    # n = 1000*t/TIMESTEP
    start_time = my_supervisor.getTime()
    while my_supervisor.step(TIMESTEP) != 1:
        if my_supervisor.getTime() - start_time >= t:
            # print("time", t)
            break
        if reset_position:
            restore_robot_position()
            my_robot_node.resetPhysics()

def getPerformanceData():
    """
        Get the number of squares explored by the robot in that simulation.
    """
    emitter.send("return_fitness".encode('utf-8'))
    while my_supervisor.step(TIMESTEP) != -1:

        ## Keep waiting for a message to continue the process
        if receiver.getQueueLength() == 0:
            continue

        if receiver.getQueueLength()>0:
            # message = receiver.getData().decode('utf-8')
            message = receiver.getString()
            receiver.nextPacket()
            ## Number of squares explored
            explored_fitness = int(message)

        return explored_fitness

def send_genotype(genotype):
    """
        Send the genotype to the robot controller and
        evaluate fitness.
        :param genotype: List with the genotype information
    """
    genotype_string = [str(gene) for gene in genotype]
    genotype_string = ','.join(genotype_string)

    # print("Genotype string: ", genotype_string)
    # test_message = "Hello"
    # test_encode = test_message.encode('utf-8')
    # print("Encode Test: ", test_encode)

    emitter.send(genotype_string.encode('utf-8'))
    # emitter.send(genotype_string.encode('utf-8'))

def restore_robot_position():
    global init_translation,init_rotation
    my_robot_translation.setSFVec3f(init_translation)
    my_robot_rotation.setSFRotation(init_rotation)

def evaluate_genotype(genotype):
    ## Send genotype to my_robot
    send_genotype(genotype)

    ## Run for 1 minute
    run_seconds(30)

    ## Store fitness
    fitness = getPerformanceData()
    #print("Supervisor:Fitness of ",genotype," - %f "%(fitness))

    ## Store genotype

    my_robot_node.resetPhysics()
    restore_robot_position()

    run_seconds(5, True)

    my_robot_node.resetPhysics()
    restore_robot_position()

    return fitness

def run_optimization(population):

    print("---\n")
    print("Starting Optimization")
    print("Population Size %i , Genome Size %i"%(POPULATION_SIZE,GENOTYPE_SIZE))

    ## List to store average fitness
    average_fitness_over_time = []

    for gen in range(NUM_GENERATIONS):
        population_fitness = []
        for ind in range(POPULATION_SIZE):
            print("-----------------------------------------------")
            print("Generation %i , Genotype %i "%(gen,ind))

            ## Get genotype from population
            genotype = population[ind]

            print("Run optimization, genotype sent: ", genotype)

            ## Evaluate genotype
            fitness = evaluate_genotype(genotype)

            ## Add fitness to population fitness
            population_fitness.append(fitness)

        best_fitness, best_fitness_val = population_get_fittest(population, population_fitness)
        average_fitness = population_get_average_fitness(population_fitness)
        print("Best Fitness Params: ",best_fitness)
        print("Best Fitness Value: ", best_fitness_val)
        print("Average Fitness: ", average_fitness)

        ## Store average fitness over generations
        average_fitness_over_time.append(average_fitness)

        # print("Best Fitness Value - %f"%int(best_fitness_val))
        # print("Average Fitness - %f"%average_fitness)

        if(gen < NUM_GENERATIONS-1):

            population = population_reproduce(population,population_fitness, GENOTYPE_SIZE)
            print("New population: ", population)

    return best_fitness, best_fitness_val, average_fitness_over_time

def main():
    ## Initialize keyboard
    global init_translation ,init_rotation, my_robot_translation, my_robot_rotation, population

    keyb = Keyboard()
    keyb.enable(TIMESTEP)

    my_robot_translation = my_robot_node.getField("translation")
    my_robot_rotation = my_robot_node.getField("rotation")
    init_translation = (my_robot_translation.getSFVec3f())
    init_rotation = (my_robot_rotation.getSFRotation())

    population = create_random_parameters_set(POPULATION_SIZE, GENOTYPE_SIZE, weights_bias_range)

    fittest_params, fittest_fitness, average_fitness_over_time = run_optimization(population)

    print("------------------------------------------------------")
    print("Best Fitness Params All Time: ",fittest_params)
    print("Best Fitness Value All Time: ", fittest_fitness)
    print("Average Fitness Per generation All Time: ", average_fitness_over_time)
    print("Average Fitness All Time: ", sum(average_fitness_over_time)/len(average_fitness_over_time))
    print("------------------------------------------------------")

    send_genotype(fittest_params)

    ## Restore robot's position
    print("Restore robot position last time")
    restore_robot_position()

    while my_supervisor.step(TIMESTEP) != -1:
        key = keyb.getKey()

        if key == ord('Q'):
            quit()

main()
