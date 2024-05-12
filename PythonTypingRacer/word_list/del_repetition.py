filename = 'kara_7.txt'

with open(filename, 'r') as file:
    unique_words = set(file.read().split())

with open(filename, 'w') as file:
    for word in unique_words:
        file.write(word + '\n')
