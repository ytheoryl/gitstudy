import math
angle = 45
value = math.radians(angle)  #convert degree to radians
b = math.sin(value)
c = math.tan(value)
print 'the angle',angle,' = ',value,'in radians'
print 'sin',angle,'=',b
print 'tan',angle,'=',c
print 'pi=',math.pi
print math.degrees(value)  #convert radians to degree
print math.sin(math.pi/2)

print '************************************'




def solve(eq,var='x',var1='y'):
    eq1 = eq.replace("=","-(")+")"
    c = eval(eq1,{var:1j},{var1:1j})
    return -c.real/c.imag

print solve('10+y-x=50', 'x','y')

