from collections import Counter
import re


class WordCounter:
    stop_words_path = "stop_words.txt"

    def count_words(text):
        words = re.findall(r"\b\w+\b", text)
        word_count = Counter(words)
        word_count = WordCounter.filter_short_words(word_count)
        # load stop words
        with open(WordCounter.stop_words_path, "r", encoding="utf8") as f:
            lines = f.readlines()
            stop_words_text = " ".join(lines)
            stop_words = re.findall(r"\b\w+\b", stop_words_text)
        word_count = WordCounter.filter_stop_words(word_count, stop_words)
        sorted_word_count = dict(
            sorted(word_count.items(), key=lambda item: item[1], reverse=True)
        )
        return sorted_word_count

    def filter_short_words(word_count):
        return {word: count for word, count in word_count.items() if len(word) >= 3}

    def filter_stop_words(word_count, stop_words):
        return {
            word: count for word, count in word_count.items() if word not in stop_words
        }
