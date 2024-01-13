from math import factorial, prod, sqrt
from time import time
from random import getrandbits, shuffle
from functools import cache

start_time = time()

@cache
def fac(a):
    if a > 100 or type(a) is not int: return
    return factorial(a)

@cache
def dbfac(a):
    if a > 100 or a < 0 or type(a) is not int: return
    start = 2 if a % 2 == 0 else 1
    return prod(range(start, a+1, 2))

@cache
def sq(a):
    if a < 0: return #Theres a chance a non-intiger could be used, so we might have to remove this.
    return sqrt(a)

@cache
def e(a):
    return eval(a, {"f": fac, "s": sq, 'd': dbfac})
    
nums = ['2','0','2','4']
ops = ['','f','d','s']
signs = ['+','-','*','/','**',  '+','-','*']

#Import already found solutions from numsolver_solutions.txt
found_expressions = {}
with open(f'numsolver_solutions.txt', 'r') as f:
    expressions = f.readlines()
    expressions.pop(0) #Remove header line
    for expression in expressions:
        solution, val = expression.split(' = ')
        found_expressions[int(val)] = solution
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
            if getrandbits(1): #Small chance to not use parenthesis/functions
                num = ops[getrandbits(2)] + '(' + ('.' if getrandbits(2) else '') + num + ')'
            
        
        for i in range(len(newnums)):
            if getrandbits(1): #Small chance to not use parenthesis/functions
                newnums[i] = ops[getrandbits(2)] + '(' + newnums[i]
                newnums[(getrandbits(2))%(len(newnums)-i)+i] += ')'
        
        for i in range(len(newnums)):
            if i + 1 == len(newnums):
                break
            newnums[i] += signs[getrandbits(3)]
        
        expression = ''.join(newnums)
        _ = 0
        
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
                print('new solution found', val, '=', expression, '           after ' + str(trycount) + ' tries and ' + str(round(time() - start_time, 2)) + ' seconds.')
            elif len(expression) < len(found_expressions[val]): #Solution has already been found, see if smaller.
                found_expressions[val] = expression
                print('shorter solution found', val, '=', expression, '           after ' + str(trycount) + ' tries and ' + str(round(time() - start_time, 2)) + ' seconds. Amount left: ' + str(len(looking_for)))
except KeyboardInterrupt:
    done = True

with open(f'numsolver_solutions.txt', 'w') as f:
    f.write(("ALL!! (🙂🙂🙂)" if len(found_expressions.keys()) == len(looking_for) else str(len(found_expressions))) + ' solutions found after ' + str(trycount) + ' tries and ' + str(round(time() - start_time, 2)) + ' seconds!\n')
    #Sort found_expressions by their keys
    found_expressions = {key: value for key, value in sorted(found_expressions.items())}
    for val, expression in sorted(found_expressions.items()):
        f.write(expression + " = " + str(val)+'\n')
print("Successfullly saved solutions to numsolver_solutions.txt")