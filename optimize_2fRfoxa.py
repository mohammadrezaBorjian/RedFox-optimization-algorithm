import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
import math
from PIL import Image
import sys

images = []


def fitness_function(point):
    a , b = point
    return abs(2 * a + 3 * b + 10)

def sort_two_lists(list1, list2):
    dict = {}
    for i in range(len(list1)):
        dict[list1[i]] = list2[i]
    new_list2 = []
    for key in sorted(dict.keys()):
        new_list2.append(dict[key])
    return new_list2

def calculateFitness(foxess):
    fitn = []
    for i in range(len(foxess)):
        fitn.append(fitness_function(foxess[i]))
    return fitn

def random_in_ranges(iteration ,point1, point2, minRange, maxRange):
    print(f"iteration {iteration}")
    n_dimensions = len(point1)
    point1 = np.array(point1)
    point2 = np.array(point2)
    sum = np.add(point1 , point2)
    center = np.divide(sum, 2)
    
    print(f'point 1 {point1} point 2 {point2} sum{sum} center {center}')
    radius = np.sqrt(np.sum(np.square(center - point1)))
    
    while True:
        rndNumber = np.random.uniform(minRange, maxRange, size=n_dimensions)
        random_point_distance = np.sqrt(np.sum(np.square(center - rndNumber)))
        if random_point_distance > radius:
            return rndNumber


def rfoa(populationSize, dimension, iterations, L, R):
    foxes = []
    f = []
    FromIndex = populationSize - int(0.05 * populationSize)

    for _ in range(populationSize):
        fox = []
        for _ in range(dimension):
            fox.append(np.random.uniform(L, R))
        foxes.append(fox)
    fitness = calculateFitness(foxes)
    foxes = sort_two_lists(fitness, foxes)
    for T in range(iterations):
        createChart(foxes , T,FromIndex)
        for index in range(FromIndex, populationSize):
            habitatCenter = []
            for j in range(dimension):
                habitatCenter.append((foxes[0][j] + foxes[1][j]) / 2)

            kappa = np.random.uniform(0, 1)
            if kappa >= 0.45:
                    foxes[index]= random_in_ranges(T ,foxes[0],foxes[1], L,R)
            else:
                for j in range(dimension):
                    foxes[index][j] = kappa * habitatCenter[j]

        for i in range(len(foxes)):

            alpha = np.random.uniform(0, distance.euclidean(foxes[i], foxes[0]))
            for j in range(dimension):
                value = 1
                if foxes[0][j] - foxes[i][j] < 0:
                    value = -1
                
                if foxes[i][j] + alpha * value < R and foxes[i][j] + alpha * value > L:
                    foxes[i][j] += alpha * value

                elif foxes[i][j] - alpha * value < R and foxes[i][j] - alpha * value > L:
                    foxes[i][j] -= alpha * value


        a = np.random.uniform(0, 0.2)
        for i in range(len(foxes)):

            if np.random.uniform(0, 1) > 0.75:
                phi = []
                for _ in range(dimension):
                    phi.append(np.random.uniform(0, 2 * math.pi))
                r = np.random.uniform(0, 1)

                if phi[0] != 0:

                    r = a * math.sin(phi[0]) / phi[0]
            
                for j in range(dimension):
                    if j == 0:
                        foxes[i][j] = foxes[i][j] + a * r * math.cos(phi[0])
                    else:
                        for k in range(j):
                            if k != j:
                                foxes[i][j] = foxes[i][j] + a * r * math.sin(phi[j])
                            else:
                                foxes[i][j] = foxes[i][j] + a * r * math.cos(phi[j])
                                
        fitnessArray = calculateFitness(foxes)                       
        foxes = sort_two_lists(fitnessArray,foxes)

        f = fitnessArray

    return f,foxes


def createChart(foxes,s,FromIndex):
    for i,v in enumerate(foxes):
        if i == 0 or i == 1:
            plt.scatter(foxes[i][0], foxes[i][1], color= "blue", s=30)
        elif i >= FromIndex:
            plt.scatter(foxes[i][0], foxes[i][1], color= "yellow", s=30)
        else:
            plt.scatter(foxes[i][0], foxes[i][1], color= "red", s=30)

        
    plt.axhline(y = 0, color = 'b', linestyle = '-') 
    plt.axvline(x=0,color = "b" , linestyle = '-')
    plt.xlim(-10, 10) 
    plt.ylim(-10, 10) 
    plt.legend(fontsize=10) 
    plt.savefig(f"images/{s}.png")
    images.append(f"images/{s}.png")
    plt.close()
def create_gif(image_path_list,output_path):
    image_list = [Image.open(file) for file in image_path_list]

    image_list[0].save(
            output_path,
            save_all=True,
            append_images=image_list, 
            duration=5000, 
            loop=0)


fitnesses,foxes = rfoa(100, 2, 200, -10, 10)
print("Solution:", foxes[0])
print("Fitness:", "{0:.8f}".format(fitnesses[0]))
create_gif(images,"fox.gif")

