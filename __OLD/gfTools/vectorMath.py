import math
help(math) #sqrt(x)
math.pow(2, 2)
# Dot Product
# Multiply all indexes and add all results to find a length number
loc1 = cmds.xform('locator1', q=True, ws=True, t=True)
loc2 = cmds.xform('locator2', q=True, ws=True, t=True)
dotResult = (loc1[0] * loc2[0]) + (loc1[1] * loc2[1]) + (loc1[2] * loc2[2])

# Vector length
# ||vec a||* = square root of every index squared (* = magnitude)
# Vector length is equal to a square rooted of dot product of a same vector 
loc3 = cmds.xform('locator3', q=True, ws=True, t=True)
lengthLoc1 = math.sqrt(math.pow(loc1[0], 2) + math.pow(loc1[1], 2) +
    math.pow(loc1[2], 2))

# Cross Product
# Multiply all indexes and find result vector
loc4 = cmds.xform('locator4', q=True, ws=True, t=True)
loc5 = cmds.xform('locator5', q=True, ws=True, t=True)
crossResult = []
crossResult.append((loc4[1] * loc5[2]) - (loc4[2] * loc5[1]))
crossResult.append((loc4[2] * loc5[0]) - (loc4[0] * loc5[2]))
crossResult.append((loc4[0] * loc5[1]) - (loc4[1] * loc5[0]))