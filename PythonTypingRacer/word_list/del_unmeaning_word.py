with open('kata_word_translated.txt', 'r') as file:
    wordlist_meaning = file.readlines()
    no_meaning_word_index = []
    wordlist_meaning_filter = []
    for i in range(len(wordlist_meaning)):
        if wordlist_meaning[i] != '\n':
            wordlist_meaning[i] = wordlist_meaning[i].strip()
            wordlist_meaning_filter.append(wordlist_meaning[i])
        else:
            no_meaning_word_index.append(i)

with open('kata_word_translated_after.txt', 'w') as file:
    for i in wordlist_meaning_filter:
        file.write(i + '\n')

with open('kata_word.txt', 'r') as file:
    wordlist = file.read().split()

with open('kata_word_after.txt', 'w') as file:
    wordlist_after = []
    for i in range(len(wordlist)):
        if i not in no_meaning_word_index:
            file.write(wordlist[i] + '\n')
