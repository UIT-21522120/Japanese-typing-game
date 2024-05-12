def is_katakana(word):
    for char in word:
        if not ('\u30A0' <= char <= '\u30FF'):
            return False
    return True

def is_hiragana(word):
    for char in word:
        if not ('\u3040' <= char <= '\u309F'):
            return False
    return True


file = open('kata_word.txt', 'r')
lines = file.readlines()
a = []
for line in lines:
    line = line.strip()
    a.append(line)

# def filter_words_by_length(words, length):
#     filtered_words = [word for word in words if len(word) == length]
#     return filtered_words
#
#
# def write_words_to_file(words, filename):
#     with open(filename, 'w') as file:
#         for word in words:
#             file.write(word + '\n')
#
# filtered_words = filter_words_by_length(a, 7)
#
# output_file = "kara_7.txt"
#
# write_words_to_file(filtered_words, output_file)
