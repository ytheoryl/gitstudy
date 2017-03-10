print ("""*****************
***hello***
*****************""")               #""" for multiple lines output
print
a = 100; b = "word"; c = 3.14; d = True
line = '-------------------------------------'
print a, '--', type(a)
print b, '--', type(b)
print c, '--', type(c)
print d, '--', type(d)

print line
########################################################################################################################
s1 = (2, 1.3, 'love', 5.6, 9, 12, False)     #tuple
s2 = [True, 5, 'smile']                          #list, can be modified
s3 = (1,[3,4,5])
s4=[]

print s1[2], s2[0]
print s1[2][3]                                    #print 4th letter of the word
print s3[1]
print s3[1][0]                                      #print 1st digit of 2nd number in s3
print
s2[0]=False
print s2[0]

print s1[0:3]                 #print from 0 till 3, not include 3
print s1[0:6:2]              #print from 0 till 6, not include 6, print every 2
	
print line
########################################################################################################################
txt='abcd efgh'
print txt.upper()
print txt.lower()
print txt.title()
print txt.capitalize()

print txt.isupper()
print txt.islower()
print txt.istitle()

text=txt.upper()
print text
print text.isupper()

print line
########################################################################################################################
print 1+9
print 1.3-4
print 3*5
print 4.5/1.5
print 3**2    # = 3*3
print 10%3

print line
########################################################################################################################
print 5==6
print 8.0!=8.0  
print 3<3, 3<=3
print 4>5, 4>=0 
print 5 in [1,3,5]

print line
########################################################################################################################
print True and True, True and False
print True or False
print not True
print 5==6 or 5 in [1,3,5]
print 5==6 and 5 in [1,3,5]

print line
########################################################################################################################
i = -3
x=2
if i>0:
	x=1
#x=5
print x
if not i>0:
	x=1
print x

print line
########################################################################################################################
# for and while
idx=range(5)  #create a table starting from 0
print idx
print
for f in s1:
	print f
print
for h in range(9):
	print h
	if h > 6:
		break
print

for g in range(20):
    while g < 5:
    print g
    g = g + 1

print line
########################################################################################################################
# def ()
def square_sum(m,n):
	l = m**2 + n**2
	return l
m=2; n=3
print "square_sum of",m,'and',n,'=',square_sum(m,n)
print 
print

j=[3,4,5]
def change_list(j):
	j[0]=j[0]+1
	return j
print 'def j=',change_list(j)
print 'j=',j                        #list value wil be changed by def

print
k = 1
def change_integer(k):
    k = k + 1
    return k
print 'def k=',change_integer(k)
print 'k=',k                          #variable will NOT be changed by def

print line
########################################################################################################################
#class and object
class bird(object):
	have_feather = True
	reproduction = 'egg'
	def move(self, dx, dy):
		position = [2,10]
		position[0] = position[0] + dx
		position[1] = position[1] + dy
		return position
		
summer = bird()
print summer.have_feather,'and',summer.reproduction
print 'after move:',summer.move(5,8)
autumn=summer.move(10,10)
print 'autumn=',autumn

class chicken(bird):         #inherit from bird(), add more properties
	wap_of_move = 'walk'
	in_kfc = True
spring = chicken()
print 'spring=',spring.reproduction,' and ',spring.in_kfc

class eagle(bird):           #inherit from bird(), add more properties
	way_of_move = 'fly'
	in_kfc = False
winter = eagle()
print 'winter=',winter.way_of_move,'and',winter.in_kfc


print line
########################################################################################################################

class Human(object):
    laugh = 'hahahaha'
    def show_laugh(self):
        print self.laugh
    def laugh_100th(self):
        for i in range(5):
            self.show_laugh()
li_lei = Human()          
li_lei.show_laugh()
print 
li_lei.laugh_100th()

print line
########################################################################################################################

class happyBird(Bird):
    def __init__(self,more_words):
        print 'We are happy birds.',more_words
summer = happyBird('Happy,Happy!')