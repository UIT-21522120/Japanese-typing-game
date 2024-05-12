with open('hira_word_translated_after.txt', 'r') as file:
    wordlist = file.readlines()
    a = []
    for i in wordlist:
        i = i.strip()
        a.append(i)
    print(a)
