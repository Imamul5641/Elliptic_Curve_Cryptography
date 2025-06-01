#
# tonelli_shanks() :- implementation of Tonelli-Shanks algorithm
#
# @n : the quadratic residue for which the solution
# is to be found
#
# @p : the prime number with respect to which the
# solution has to be found
#
# finds x : (x*x) ≡ n mod p
# where p = 4k + 3
#
def tonelli_shanks(n, p):
  print(f"**** Tonelli Shanks *****")
  x = p-1
  s = 0
  while x%2!=1:
    x=x//2
    s+=1
  q = (p-1)//(2**s)
  z = 2
  while(isResidue(z,p)):
    z+=1
  M = s
  c = pow(z,q,p)
  t = pow(n,q,p)
  R = pow(n,(q+1)/2,p)
  while(True):
    if(t==0):
      return 0
    if(t==1):
      return R
    i = 0
    while(pow(t,2**i,p)!=1):
      i+=1
    b = pow(c,2**(M-i-1),p)
    M = i
    c = pow(b,2,p)
    t = (t*c)%p
    R = (R*b)%p

#
# pow() :- helper function to execute
# fast exponentiation with modular operation
#
# @a, @b : base and index values respectively for
# exponentiation operation
#
# @m : the value to be used for modular part of
# the operation
#
# returns a^b mod m
# time complexity : O(logn)
#
def pow(a, b, m):
    # print(f"**** pow *****")
    if(b == 0):
      return 1%m
    ans = pow(a, b//2, m)
    if(b%2 == 0):
      return (ans*ans)%m
    else:
      return ((ans*ans)%m*a)%m

#
# isResidue() :- helper function to check whether a
# given number is a quadratic residue with respect to
# a given prime number
#
# @x : the number to check for quadratic residue
#
# @p : the prime number with respect to which the
# condition has to be checked
#
# Euler's criterion for QR:
#
# if x^((p-1)/2) ≡ 1 mod p, then x is QR
# if x^((p-1)/2) ≡ -1 mod p, then x is QNR
#
def isResidue(x, p):
  # print(f"**** isResidue *****")
  return pow(x,(p-1)/2,p) == 1

#
# generatePoints() :- generates points according to the
# given curve parameters and stores them in file
#
# @a, @d : parameters of the Short Weiestrass Curve
#
# @p : the prime number with respect to which the
# points have to be found
#
# @fname : takes the name of the file to be created
# to store the points (default : points.txt)
#
# The general equation for Short Weiestrass Curve is :
#
# y^2 = x^3+ax+d
#
#
#
# opens a new file with given name
#
# for every x from 0 to p, checks if the corresponding
# value of y^2 is a quadratic residue
#
# if it is, uses appropriate function to find y
# depending on nature of p
#
# writes the points into the opened file
#
def generatePoints(a, d, p, start=0):
  print(f"**** generatePoints *****")
  #Creating the output file
  x_array = []
  y_array = []

  # $$$
  if start > p:
    start = 0

  # take at max 1000 points
  for x in range(start,  min(start+1000, p)):
      fx = ((x*x*x)+(a*x)+d)%p   #finding values of y^2 mod p for every integer value of x in range
      if(isResidue(fx, p) or fx == 0):
        # 4k+3 form
        if((p-3)%4 == 0):
          y = pow(fx, (p+1)/4, p)   #euler's method
        # 4k+1 form
        else:
          y = tonelli_shanks(fx,p)   #Tonneli-Shank's method

        x_array.append(x)
        y_array.append(y)
        if fx != 0:
          x_array.append(x)
          y_array.append(p-y)
  return (x_array,y_array)
