text = input("Text: ")

def main():
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    L = letters / words * 100
    S = sentences / words * 100
    index = 0.0588 * L - 0.296 * S - 15.8
    round_index = round(index)

    if (index < 1):
        print("Before Grade 1")
    elif (index >= 1 and index <= 16):
        print(f"Grade {round_index}")
    else:
        print("Grade 16+")

def count_letters(text):
    letters = 0
    for i in range (len(text)):
        if text[i].isalpha():
            letters +=1
    return letters

def count_words(text):
    spaces = 0
    for i in range(len(text)):
        if text[i].isspace():
            spaces += 1
    words = spaces + 1
    return words

def count_sentences(text):
    sentences = 0
    for i in range(len(text)):
        if (text[i] == '.' or text[i] == '!' or text[i] == '?'):
            sentences += 1
    return sentences

main()