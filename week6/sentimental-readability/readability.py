def main():
    text = get_text()
    get_grade(text)

def get_grade(text):
    letter_count = sum(1 for char in text if char.isalpha())
    word_count = len(text.split())
    sentence_count = text.count(".") + text.count("!") + text.count("?")
    index = coleman_liau_index(letter_count, word_count, sentence_count)

    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {round(index)}")

def coleman_liau_index(letter_count, word_count, sentence_count):
    L = letter_count / word_count * 100
    S = sentence_count / word_count * 100
    index = 0.0588 * L - 0.296 * S - 15.8
    return index

def get_text():
    text = input("Text: ").lower()
    return text

if __name__ == "__main__":
    main()