marks = [85, 72, 45, 90, 35, 60]

# Average
average = sum(marks) / len(marks)

# Highest mark
highest = max(marks)

# Lowest mark
lowest = min(marks)

# Number of students passed
passed = 0

for mark in marks:
    if mark >= 40:
        passed += 1

# Grade for each student
for mark in marks:
    if mark >= 90:
        grade = "A+"
    elif mark >= 80:
        grade = "A"
    elif mark >= 70:
        grade = "B"
    elif mark >= 60:
        grade = "C"
    elif mark >= 40:
        grade = "D"
    else:
        grade = "F"

    print(mark, "->", grade)


print("Average:", average)
print("Highest:", highest)
print("Lowest:", lowest)
print("Passed students:", passed)
