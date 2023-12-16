import os

from cleaner import Cleaner
from merger import Merger
from counter import WordCounter


def main():
    # merge pdf, output the merged text
    Merger("pdf").merge()
    with open(Merger.origin_path, "r", encoding="utf8") as f:
        lines = f.readlines()
        pdf_text = " ".join(lines)
    print("=== merge text completed.")

    # remove invalid characteristics
    cleaned_text = Cleaner(pdf_text).clean()
    with open("out/final.txt", "w", encoding="utf8") as f:
        f.write(cleaned_text)
    print("=== remove invalid characteristics completed.")

    # count words
    sorted_word_count = WordCounter.count_words(cleaned_text)

    # output the word statistics
    if os.path.exists("out/result.txt"):
        os.remove("out/result.txt")
    with open("out/result.txt", "a+", encoding="utf8") as f:
        for word, count in sorted_word_count.items():
            f.write(f"{word}: {count}\n")
    print("=== all completed.")


if __name__ == "__main__":
    main()
