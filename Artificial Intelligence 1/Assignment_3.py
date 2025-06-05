from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from itertools import combinations
import random

# The dataset is uploaded
f = open("Assignment 3 medical_dataset.DATA")
dataset_X = []
dataset_y = []
line = " "
while line != "":
    line = f.readline()
    line = line[:-1]
    if line != "":
        line = line.split(",")
        floatList = []
        for i in range(len(line)):
            if i < len(line)-1:
                floatList.append(float(line[i]))
            else:
                value = float(line[i])
                if value == 0:
                    dataset_y.append(0)
                else:
                    dataset_y.append(1)
        dataset_X.append(floatList)
f.close()

# The dataset is splited into training and test.
X_train, X_test, y_train, y_test = train_test_split(dataset_X, dataset_y, test_size = 0.25, random_state = 0)

# The dataset is scaled
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# The model is created
model = KNeighborsClassifier(n_neighbors = 3)

# Function that calculates the fitness of a solution
def calculateFitness(solution):
    fitness = 0

    # The features are selected according to solution
    X_train_Fea_selc = []
    X_test_Fea_selc = []
    for example in X_train:
        X_train_Fea_selc.append([a*b for a,b in zip(example,solution)])
    for example in X_test:
        X_test_Fea_selc.append([a*b for a,b in zip(example,solution)])

    model.fit(X_train_Fea_selc, y_train)

    # We predict the test cases
    y_pred = model.predict(X_test_Fea_selc)

    # We calculate the Accuracy
    cm = confusion_matrix(y_test, y_pred)
    TP = cm[0][0] # True positives
    FP = cm[0][1] # False positives
    TN = cm[1][1] # True negatives
    FN = cm[1][0] # False negatives

    fitness = (TP + TN) / (TP + TN + FP + FN)

    return round(fitness *100,2)

MAX_FITNESS_CALCULATIONS = 5000
FITNESS_CALCULATION_COUNTER = 0

#TODO: Write your algorithm as a funciton. You can add input parameters if you want.
# Generate a random binary vector
def random_solution(length, max_active=None):
    sol = [0] * length  # start with all features off 
    if max_active is None: 
        max_active = random.randint(1, length)  # pick random number of features to turn on 
    for i in random.sample(range(length), max_active):  # randomly pick ones to activate 
        sol[i] = 1
    return sol  # return the new random solution 

# This function performs hill climbing starting from the given solution.
def hill_climb(start):
    global FITNESS_CALCULATIONS_COUNTER
    best = start[:]  # make a copy of the starting solution 
    best_fit = calculateFitness(best)  # get fitness of starting point 
    FITNESS_CALCULATIONS_COUNTER += 1  # update counter 
    print(f"Best solution fitness ( {FITNESS_CALCULATIONS_COUNTER} / {MAX_FITNESS_CALCULATIONS} ): {best_fit}")
    
    improved = True  # used to keep track of improvements 
    while improved and FITNESS_CALCULATIONS_COUNTER < MAX_FITNESS_CALCULATIONS:
        improved = False  # reset for this loop 
        for i in range(13): # 13 features
            neighbor = best[:]  # copy current best solution 
            neighbor[i] = 1 - neighbor[i]  # flip one bit 
            if sum(neighbor) == 0:  # don't allow all-zero (no features) 
                continue
            fit = calculateFitness(neighbor)  # calculate fitness of neighbor  
            FITNESS_CALCULATIONS_COUNTER += 1  # update counter 
            if fit > best_fit:  # check if it's better 
                best = neighbor  # update best solution  
                best_fit = fit
                improved = True
                print(f"Best solution fitness ( {FITNESS_CALCULATIONS_COUNTER} / {MAX_FITNESS_CALCULATIONS} ): {best_fit}")
                break  # break inner loop if improved 
    return best, best_fit  # return the best found solution 


# This runs hill climbing 5 times starting from random solutions.
def random_restart_hill_climbing():
    global FITNESS_CALCULATIONS_COUNTER
    best_overall = None  # to store the best overall solution 
    best_fit_overall = 0  # store the best fitness seen 
    for _ in range(5):  # 5 restarts 
        if FITNESS_CALCULATIONS_COUNTER >= MAX_FITNESS_CALCULATIONS:
            break  # stop if we hit the max fitness calculations 
        start = random_solution(len(X_train[0]))  # create a random starting point 
        candidate, fit = hill_climb(start)  # do hill climbing 
        if fit > best_fit_overall:  # update best overall if needed 
            best_overall = candidate
            best_fit_overall = fit
    return best_overall, best_fit_overall  # return the best from all restarts 
    
# This function performs Variable Neighbourhood Search (VNS).
def variable_neighbourhood_search():
    global FITNESS_CALCULATIONS_COUNTER
    current = random_solution(len(X_train[0]), max_active=4)  # start with 4 features active
    current_fit = calculateFitness(current)  # evaluate starting point 
    FITNESS_CALCULATIONS_COUNTER += 1
    print(f"Best solution fitness ( {FITNESS_CALCULATIONS_COUNTER} / {MAX_FITNESS_CALCULATIONS} ): {current_fit}")
    for k in range(1, 5):  # neighborhood flip 1 to 4 bits 
        if FITNESS_CALCULATIONS_COUNTER >= MAX_FITNESS_CALCULATIONS:
            break
        improved = False 
        for flips in combinations(range(len(current)), k):  
            neighbor = current[:] 
            # tries multiple combinations at once
            for i in flips: # iterates thru flip options
                neighbor[i] = 1 - neighbor[i] 
            if sum(neighbor) > 4 or sum(neighbor) == 0:  # keep max 4 features and at least 1
                continue
            fit = calculateFitness(neighbor) 
            FITNESS_CALCULATIONS_COUNTER += 1
            if fit > current_fit:  # accept better solution 
                current = neighbor
                current_fit = fit
                improved = True
                print(f"Best solution fitness ( {FITNESS_CALCULATIONS_COUNTER} / {MAX_FITNESS_CALCULATIONS} ): {current_fit}")
                break  # break to restart with new current
        if not improved: 
            break  # stop if no better neighbor found
    return current, current_fit  # return best solution found 


# This runs both algorithms 3 times each and shows their performance.
def run_algorithms():
    global FITNESS_CALCULATIONS_COUNTER

    print("Running Random-Restart Hill Climbing:")
    rrhc_scores = []
    for _ in range(3):
        FITNESS_CALCULATIONS_COUNTER = 0  # reset counter
        _, score = random_restart_hill_climbing()  # run hill climbing
        rrhc_scores.append(score)
    print("Scores:", rrhc_scores)
    print("Average:", round(sum(rrhc_scores)/3, 2), "\n")  # show average

    print("Running Variable Neighbourhood Search:")
    vns_scores = []
    for _ in range(3):
        FITNESS_CALCULATIONS_COUNTER = 0  # reset again
        _, score = variable_neighbourhood_search()
        vns_scores.append(score)
    print("Best fitness Scores:", vns_scores)
    print("Average fitness:", round(sum(vns_scores)/3, 2))  # final average
    
if __name__ == "__main__":
    run_algorithms()