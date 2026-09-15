numbers = [10, 15, 22, 3, 7, 1, 55, 98, 8]

minimum = numbers[0]
maximum = numbers[0]

for num in numbers:
    if num < minimum:
        minimum = num

    if num > maximum:
        maximum = num

print("Minimum:", minimum)
print("Maximum:", maximum)