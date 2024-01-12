from math import factorial, prod
from time import time, strftime
from random import getrandbits, shuffle, randint
from functools import cache

start_time = time()

@cache
def fac(a):
    return factorial(a)

@cache
def dbfac(n):
    start = 2 if n % 2 == 0 else 1
    return prod(range(start, n+1, 2))

@cache
def sq(a):
    return a ** 0.5

@cache
def e(a):
    return eval(a, {"f": fac, "s": sq, 'd': dbfac})
    
nums = ['2','0','2','4']
ops = ['','f','d','s']
signs = ['+','-','*','/','**',  '+','-','*']

#Import already found solutions from numsolver_solutions.txt
found_expressions = {}
with open(f'solutions/numsolver_solutions.txt', 'r') as f:
    expressions = f.readlines()
    for expression in expressions:
        solution, val = expression.split(' = ')
        found_expressions[val] = solution
#Done importing solutions
looking_for = list(range(101))
trycount = 0
done = False
try:
    while not done:
        trycount += 1

        shuffle(nums)
        if not getrandbits(5):
            #randomly concatinate random pairs or triplets or all 4
            if not getrandbits(2):
                newnums = [nums[0]+nums[1]+nums[2], nums[3]]
            elif getrandbits(1):
                newnums = [nums[0]+nums[1], nums[2], nums[3]]
            elif getrandbits(2):
                newnums = [nums[0]+nums[1], nums[2]+nums[3]]
            else:
                newnums = [nums[0]+nums[1]+nums[2]+nums[3]]
            shuffle(newnums)
        else:
            newnums = nums.copy()
        
        for num in newnums:
            num = ops[getrandbits(2)] + '(' + ('.' if getrandbits(2) else '') + num + ')'
        
        for i in range(len(newnums)):
            newnums[i] = ops[getrandbits(2)] + '(' + newnums[i]
            newnums[(getrandbits(2))%(len(newnums)-i)+i] += ')'
        
        for i in range(len(newnums)):
            if i + 1 == len(newnums):
                break
            newnums[i] += signs[getrandbits(3)]
        
        expression = ''.join(newnums)
        #val = 0
        
        try:
            val = e(expression)
            if(val - int(val) < 0.001):
                val = int(val)
            else:
                continue

        except:
            #print('this one had an error')
            continue

        if val in looking_for:
            if val not in found_expressions.keys():
                found_expressions[val] = expression
            else: #Solution has already been found, see if smaller.
                if len(expression) < len(found_expressions[val]):
                    found_expressions[val] = expression
            
            print('found', val, '=', expression, '           after ' + str(trycount) + ' tries and ' + str(round(time() - start_time, 2)) + ' seconds. Amount left: ' + str(len(looking_for)))
            if not looking_for:
                done = True
except KeyboardInterrupt:
    done = True

with open(f'solutions/numsolver_solutions.txt', 'w') as f:
    f.write(("ALL!! (🙂🙂🙂)" if len(found_expressions[val].keys()) == len(looking_for) else str(len(found_expressions))) + ' solutions found after ' + str(trycount) + ' tries and ' + str(round(time() - start_time, 2)) + ' seconds!\n')
    for i, expression in list(enumerate(found_expressions)):
        if expression != None: 
            f.write(expression + " = " + str(i) + '\n')
