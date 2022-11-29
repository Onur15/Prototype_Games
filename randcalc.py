import random
op_list = ["+", "-", "x", "/"]
n1, n2, op = 0, 0, 0
c1, c2 ,cp = 0, 0, 0
config = False
run = True
print("'config' for customise numbers.")
n = input("num digits: ")
print()
if n == "config":
    config = True
    print("Type -1 for random:")
    print("Type first number:", end=" ")
    n1 = int(input())
    c1 = n1
    if n1 == 0:
        print("Type first num digits:", end=" ")
        n = int(input())
    print("Type second number:", end=" ")
    n2 = int(input())
    c2 = n2
    if n2 == 0:    
        print("Type second num digits:", end=" ")
        m = int(input())
    print("operation [+ : 0, - : 1, x : 2, / : 3]:", end=" ")
    op = int(input())
    cp = op
    if op != -1 and config:
        op = op_list[op]
if not config:
    n = int(n)
    m = n
while run:
    if c1 == -1:
        n1 = random.randint(10**(n-1), 10**n)
    if c2 == -1:
        n2 = random.randint(10**(m-1), 10**m)    
    
    div = True
    while div:
        if cp == -1:
            op = random.choices(op_list, weights=[3,2,2,2])[0]
        if op == "/":
            for i in range(10):
                if n1/n2 == round(n1/n2, 2):
                    div = False
                    break
                if c1 == -1:
                    n1 = random.randint(10**(n-1), 10**n)
                if c2 == -1:
                    n2 = random.randint(10**(m-1), 10**m)
        else:
            div = False               
    print(str(n1)+op+str(n2)+" =", end=" ")
    eq = {
        0 : n1+n2,
        1 : n1-n2,
        2 : n1*n2,
        3 : n1/n2
    }
    ans = input()
    if ans != "":
        ans = float(ans)
    if ans != eq.get(op_list.index(op)):
        print("Answer was:", eq.get(op_list.index(op)))
        print("Try again.")
        run = False
        
