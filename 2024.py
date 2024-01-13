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
def EVALL(a):
    return eval(a, {"f": fac, "s": sq, 'd': dbfac})
    
nums = ['2','0','2','4']
ops = ['','f','d','s']
signs = ['+','-','*','/','**',  '+','-','*']

looking_for = list(range(1, 101))
# missing_nums = [57,69,71,73,75,77,91,93,]
found_nums = []
trycount = 0
try:
    while True:
        trycount += 1

        shuffle(nums)
        if not getrandbits(5):
            #randomly concatinate random pairs of numbers, or triplets
            if not getrandbits(2):
                newnums = [nums[0]+nums[1]+nums[2], nums[3]]
            elif getrandbits(1):
                newnums = [nums[0]+nums[1], nums[2], nums[3]]
            else:
                newnums = [nums[0]+nums[1], nums[2]+nums[3]]
            shuffle(newnums)
        else:
            newnums = nums.copy()
        
        for num in newnums:
            num = ops[getrandbits(2)] + '(' + ('.' if getrandbits(2) else '') + num + ')'
        
        for i in range(len(newnums)):
            newnums[i] = ops[getrandbits(2)] + '(' + newnums[i]
            newnums[i+randint(0,len(newnums)-1-i)] += ')'
        
        for i in range(len(newnums)):
            if i + 1 == len(newnums):
                break
            newnums[i] += signs[getrandbits(3)]
        
        expression = ''.join(newnums)
        val = 0
        
        try:
            val = EVALL(expression)
            if(val - int(val) < 0.001):
                val = int(val)
            else:
                continue

        except:
            #print('this one had an error')
            continue

        if val in looking_for:
            looking_for.remove(val)
            found_nums.append(f"{expression}  =   {str(val)}")
            print('found', val, 'with:', expression, '           after ' + str(trycount) + ' tries and ' + str(round(time() - start_time, 2)) + ' seconds. Amount left: ' + str(len(looking_for)))
            if not looking_for:
                print('found all numbers after ' + str(trycount) + ' tries and ' + str(round(time() - start_time, 2)) + ' seconds!')
                #Export solutions to file, in numerical order. Also export tries and time taken.
                found_nums.sort(key=lambda x: int(x.split(' = ')[1]))
                with open(f'solutions/numsolver_solutions{strftime("%Y-%m-%d %H:%M:%S")}.txt', 'w') as f:
                    f.write('Solutions found after ' + str(trycount) + ' tries and ' + str(round(time() - start_time, 2)) + ' seconds!\n')
                    for solution in found_nums:
                        f.write(solution + '\n')
                break
except KeyboardInterrupt:
    found_nums.sort(key=lambda x: int(x.split(' = ')[1]))
    with open(f'solutions/numsolver_solutions{strftime("%Y-%m-%d %H-%M-%S")}.txt', 'w') as f:
        f.write(str(len(found_nums))+' solutions found after ' + str(trycount) + ' tries and ' + str(round(time() - start_time, 2)) + ' seconds!\n')
        for solution in found_nums:
            f.write(solution + '\n')
print(found_nums)
