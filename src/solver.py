import argparse
import random
import itertools
import math

def readInput(fn):
    cities = []
    xs = []
    ys = []

    with open(fn) as f:
        lines = f.readlines()

    #format:
    #each line is "<cityId>\w<x>\w<y>"
    #where "\w" is some amount of whitespace
    for i, line in enumerate(lines):
        p = line.split()
        cities.append(p[0])
        xs.append(int(p[1]))
        ys.append(int(p[2]))

    return cities, xs, ys

def writeOutput(rfn, tour, cities, coors):
    #format:
    #first line : length (cost) of tour
    #then, the tour is printed, each line having one cityId
    fn = rfn + ".tour"
    with open(fn, 'w') as f:
        f.write(str(calc_cost(tour, cities, coors)))
        f.write('\n')
        f.write('\n'.join(tour))
        f.write('\n')

def calc_cost(tour,cities,coors):
    #calculate the cost of the current tour

    cost = 0
    #our list of all the positions of the cities,
    #in the order found in the tour
    poses = []
    for i, val in enumerate(tour):
        poses.append((coors[0][cities.index(val)], 
            coors[1][cities.index(val)]))

    #handling wrapping (turns a HAM-PATH into a HAM-CYCLE)
    poses.append(poses[0])

    for i in range(0, len(poses) - 1):
        # d(c1,c2) = sqrt( (c1.x - c2.x)^2 + (c1.y - c2.y)^2) )
        cost += math.sqrt(
                (poses[i][0]-poses[i+1][0])**2 
                + (poses[i][1]-poses[i+1][1])**2
                )

    return cost

def change2(tour,cities,coors,showall): 
    n = len(tour) 
    curr_cost = calc_cost(tour,cities, coors) 
    
    #use combinations instead of two loops
    #for nicer code and hopefully better performance
    combs = itertools.combinations(range(n),2)
    for idx,(i,j) in enumerate(combs): 
        i = int(i)
        j = int(j)
        n1 = tour[i] 
        n2 = -1 

        n2 = tour[j]
        #clone the tour to check the score if we swapped the cities
        new_tour = list(tour) 
        new_tour[i] = n2 
        new_tour[j] = n1 
        new_cost = calc_cost(new_tour,cities, coors) 

        #just for knowing whats going on
        if new_cost < curr_cost or showall:
            print(("CHECKING " if showall else "")+"Switching " 
                    + str(n1) 
                    + " with " 
                    + str(n2)
                    + " for an score of "
                    + str(new_cost)
                    + " or a loss of "
                    + str(curr_cost - new_cost))

        if new_cost < curr_cost:
            return new_tour

    print("Nothing better found")
    return False

def LocalMinima(tour,cities, coors):
    print("Finding local minima of tour "
            + str(tour) + "\nusing 2-change...")
    new_tour = tour
    while True:
        t = change2(new_tour,cities, coors, False)

        if t == False:
            #minima found
            print("Found LocalMinima!")
            return new_tour

        # not found, continue
        new_tour = t

def solve(fn):
    #parse input file
    cities, xs, ys = readInput(fn)
    coors = [xs, ys]

    #randomize for a starting tour - dont need to loop here
    start_tour = [i for i in cities]
    random.shuffle(start_tour)
    #starting cost
    print(calc_cost(start_tour, cities, coors))

    #solve for our local minima
    optim = LocalMinima(start_tour,cities ,coors)

    #sorta-debug - show all the possible 2-changes
    #and why we are at optimum
    print(change2(optim,cities,coors,True))

    #print it all out
    print("optim: " + str(optim))
    print("final score: " + str(calc_cost(optim, cities, coors)))

    #save
    writeOutput(fn, optim, cities, coors)

def main():
    parser = argparse.ArgumentParser(description="solve Travelling Salesman Problems.")
    parser.add_argument('inputFn',type=str)

    args = parser.parse_args()
    print(args)
    solve(args.inputFn)
    
main()
