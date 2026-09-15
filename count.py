words = ["apple", "banana", "apple", "mango", "banana", "apple"]

for word in set(words):
    print(word, words.count(word))