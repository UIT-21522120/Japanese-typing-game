with open('hira_word_translated.txt', 'r') as file:
    wordlist = file.readlines()
    finish = []
    for i in wordlist:
        i = i.strip()
        i = i.split(', ')
        line = []
        for j in i:
            if len(j) < 20:
                line.append(j)
        line = ', '.join(line)
        finish.append(line)
with open('hira_word_translated_after.txt', 'w') as file:
    for i in finish:
        file.write(i + '\n')