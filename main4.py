a = list(map(str, input().split()))
dictionary = {}
for x in a:
    dictionary[x] = dictionary.get(x, 0) + 1
for x in dictionary:
    print(x, dictionary[x])