import sys
def fibonacci(n):
    if n < 1:
        print('err')
        return -1
    if n==1 or n==2:
        return 1
    return fibonacci(n-1)+fibonacci(n-2)
for _ in range(int(sys.argv[1])):
    fibonacci(30)
