def prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

num = int(input("Enter number: "))

if num > 1 and prime(num):
    print("Prime")
else:
    print("Not Prime")
