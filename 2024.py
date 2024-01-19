from math import factorial, prod, sqrt
from time import time
from random import getrandbits, shuffle
from functools import cache

start_time = time()

@cache
def fac(a):
    if a > 30 or type(a) is not int: return
    return factorial(a)

@cache
def dbfac(a):
    if a > 50 or a < 0 or type(a) is not int: return
    return prod(range(2 if a % 2 == 0 else 1, a+1, 2))

@cache
def sq(a):
    if a < 0: return
    return sqrt(a)

@cache
def pow(a,b):
    if a > 1000 or b > 1000: return
    return a**b

@cache
def convertpowers(expression):
    while '**' in expression:
        # Find index of last ** in expression
        index = expression.rfind('**')
        endLeftSide = index-1
        startRightSide = index+2
        if expression[endLeftSide] == ')':
            # Find the index of the matching opening parenthesis
            perenthesisCount = 1
            startLeftSide = endLeftSide-1
            while perenthesisCount > 0:
                if expression[startLeftSide] == ')':
                    perenthesisCount += 1
                elif expression[startLeftSide] == '(':
                    perenthesisCount -= 1
                startLeftSide -= 1
            if expression[startLeftSide] in ['f','d','s','p']:
                startLeftSide -= 1
            thingOnLeft = expression[startLeftSide+1:endLeftSide+1]
            stuffFarLeft = expression[:startLeftSide+1]
        else:
            startLeftSide = endLeftSide-1
            while startLeftSide>=0 and (expression[startLeftSide].isdigit() or expression[startLeftSide]=='.'):
                startLeftSide -= 1
            thingOnLeft = expression[startLeftSide+1:endLeftSide+1]
            stuffFarLeft = expression[:startLeftSide+1]
        if expression[startRightSide] == '(' or expression[startRightSide] in ['f','d','s','p']:
            # Find the index of the matching closing parenthesis
            perenthesisCount = 1
            endRightSide = startRightSide+1
            startedWithFunction = False
            if expression[startRightSide] in ['f','d','s','p']:
                startedWithFunction = True
            while endRightSide < len(expression) and  perenthesisCount > 0:
                if expression[endRightSide] == '(':
                    perenthesisCount += 1
                    if startedWithFunction:
                        perenthesisCount -= 1
                        startedWithFunction = False
                elif expression[endRightSide] == ')':
                    perenthesisCount -= 1
                endRightSide += 1
            thingOnRight = expression[startRightSide:endRightSide]
            stuffFarRight = expression[endRightSide:]
        else:
            endRightSide = startRightSide+1
            while endRightSide<len(expression) and (expression[endRightSide].isdigit() or expression[endRightSide]=='.'):
                endRightSide += 1
            thingOnRight = expression[startRightSide:endRightSide]
            stuffFarRight = expression[endRightSide:]
        expression = stuffFarLeft + 'p(' + thingOnLeft + ',' + thingOnRight + ')' + stuffFarRight
    return expression

@cache
def e(a):
    if '**' in a:
        a = convertpowers(a)
    return eval(a, {"f": fac, "s": sq, 'd': dbfac, 'p': pow})

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
try:
    while True:
        trycount += 1

        if trycount % 5000000 == 0:
           print("Just checking in, currently on try", trycount, "and time spent so far:", round(time() - start_time, 2), "seconds.")

        shuffle(nums)
        if getrandbits(1):
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
            if getrandbits(1): #Chance to not use parenthesis/functions
                num = ops[getrandbits(2)] + '(' + ('.' if getrandbits(3) else '') + num + ')'
                
        for i in range(len(newnums)):
            if getrandbits(1): #Small chance to not use parenthesis/functions
                newnums[i] = ops[getrandbits(2)] + '(' + newnums[i]
                newnums[(getrandbits(2))%(len(newnums)-i)+i] += ')'
        
        for i in range(len(newnums) - 1):
            newnums[i] += signs[getrandbits(3)]
        
        expression = ''.join(newnums)
        
        try:
            val = e(expression)
            if(val - int(val) < 0.0001):
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
    pass

with open(f'numsolver_solutions.txt', 'w') as f:
    f.write(("ALL!! (🙂🙂🙂)" if len(found_expressions.keys()) == len(looking_for) else str(len(found_expressions))) + ' solutions found after ' + str(trycount) + ' tries and ' + str(round(time() - start_time, 2)) + ' seconds!')
    #Sort found_expressions by their keys
    found_expressions = {key: value for key, value in sorted(found_expressions.items())}
    for val, expression in sorted(found_expressions.items()):
        f.write(expression + " = " + str(val)+'\n')
print("Successfully saved solutions to numsolver_solutions.txt")
