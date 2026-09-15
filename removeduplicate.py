s = input("Enter a word: ")

result = ""

for i in s:
    if i not in result:
        result += i

print(result)