import numpy as np
from scipy.spatial import distance
import math

def fitnessFunction(point):
    a, b, c, d = point
    return abs(a + 2 * b + 3 * c + 4 * d - 30)

def sort_two_lists(list1, list2):
    dict = {}
    for i in range(len(list1)):
        dict[list1[i]] = list2[i]

    new_list2 = []
    for key in sorted(dict.keys()):
        new_list2.append(dict[key])
    return new_list2

def random_in_ranges(point1, point2, minRange, maxRange):
    n_dimensions = len(point1)
    random_point = []
    for i in range(n_dimensions):
      
        lMin = min(point1[i], point2[i])
        lMax = max(point1[i], point2[i])

        while True: 
            rndNumber = np.random.uniform(minRange, maxRange)
            if rndNumber < lMin or rndNumber > lMax:
                random_point.append(rndNumber)
                break 

    return random_point
def calculateFitness(foxess):
    fitn = []
    for i in range(len(foxess)):
        fitn.append(fitnessFunction(foxess[i]))
    return fitn

def rfoa(populationSize, dimension, iterations, L, R):
    foxes = []
    f = []

    for _ in range(populationSize):
        fox = []
        for _ in range(dimension):
            fox.append(np.random.uniform(L, R))
        foxes.append(fox)
# برای این روباه ها فیتنس محاسبه میشود
    fitness = calculateFitness(foxes)
# با توجه به فیتنس روباه ها سورت می شوند
    foxes = sort_two_lists(fitness, foxes)
# با توجه به ایتریشن داده شده، وارد الگوریتم می شویم
    for T in range(iterations):
# پنج درصد از روباه های ضعیف ما از بین می روند. این روباه ها از پایین لیست سورت شده ما هستند
        FromIndex = populationSize - int(0.05 * populationSize)
        for index in range(FromIndex, populationSize):
            habitatCenter = []
# وسط بهترین روباه ها انتخاب میشود.
            for j in range(dimension):
                habitatCenter.append((foxes[0][j] + foxes[1][j]) / 2)
# در صورتی که متغیر بالاتر از چهل و پنج صدم باشد یعنی روباه جدید به مکانی دیگر منتقل می شود و  در غیر این 
# صورت در حدود گله فعلی ایجاد می شود
            kappa = np.random.uniform(0, 1)
            if kappa >= 0.45:
                    foxes[index]= random_in_ranges(foxes[0],foxes[1], L,R)
            else:
                for j in range(dimension):
                    foxes[index][j] = kappa * habitatCenter[j]

# در فاز سرچ گلوبال اندازه هر روباه با روباه آلفا محاسبه می شود
        for i in range(len(foxes)):

            alpha = np.random.uniform(0, distance.euclidean(foxes[i], foxes[0]))
            for j in range(dimension):
                value = 1
# ضریب ولیو مشخص میکند که این روباه به سمت آلفا حرکت کند یا از آن دور شود
                if foxes[0][j] - foxes[i][j] < 0:
                    value = -1
                
                if foxes[i][j] + alpha * value < R and foxes[i][j] + alpha * value > L:
                    foxes[i][j] += alpha * value

                elif foxes[i][j] - alpha * value < R and foxes[i][j] - alpha * value > L:
                    foxes[i][j] -= alpha * value

# در فاز جستجوی محلی ضریب
# a فاصله تغییر تصادفی از طعمه
        a = np.random.uniform(0, 0.2)
        for i in range(len(foxes)):
# اگر از ۷۵ صدم بیشتر باشد یعنی به سمت طهمه نزدیک شود
# r شعاع دید روباه
# فی یعنی زاویه ی قابل مشاهد روباه که از ۰ تا دو پی است
            if np.random.uniform(0, 1) > 0.75:
                phi = []
                for _ in range(dimension):
                    phi.append(np.random.uniform(0, 2 * math.pi))
                r = np.random.uniform(0, 1)

                if phi[0] != 0:
# در صورتی که فی بعد اول مخالف صفر باشد شعاع دید به صورت فرمول زیر محاسله می شود
# در این مرحله هر کدام از ابعاد  مربوط به قسمتی از بدن روباه است که در واقع در حال محاسبه چرخش حلزونی روباه
# به دور طعمه است
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

fitnesses,foxeses = rfoa(100, 4, 100, -10, 10)
print("Solution:", foxeses[0])
print("Fitness:", "{0:.8f}".format(fitnesses[0]))
