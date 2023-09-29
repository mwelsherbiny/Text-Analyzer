from language_tool_python import LanguageToolPublicAPI
from textblob import Word
from readability import Readability


class TextAnalyzer:
    def __init__(self, text):
        # store input text
        self.text = text

    # count the number of sentences
    def get_sentences_count(self):
        count = 0
        for c in self.text:
            if c in [".", "?", "!"]:
                count += 1
        return count

    # get a list of words
    def get_words(self):
        words = self.text.strip().split(" ")
        for i in range(len(words)):
            if "." in words[i]:
                words[i] = words[i].replace(".", "")
            elif "?" in words[i]:
                words[i] = words[i].replace("?", "")
            elif "!" in words[i]:
                words[i] = words[i].replace("!", "")
        return words

    # count the number of words
    def get_word_count(self):
        return len(self.text.split(" "))

    # get a list of dictionaries that each contain a mispelled word and its correction
    def get_mispelled(self):
        mispelled = []
        words = self.get_words()
        for word in words:
            checked_word = Word(
                word
            ).spellcheck()  # returns a list of tuples: [(word, confidence)]
            correct = checked_word[0][0]
            if correct != word and checked_word[0][1] > 0.5:
                d = {"mispelled": word, "correct": correct}
                mispelled.append(d)
        return mispelled

    # count the number of mispelled words
    def get_mispelled_count(self):
        count = 0
        words = self.get_words()
        for word in words:
            checked_word = Word(
                word
            ).spellcheck()  # returns a list of tuples: [(word, confidence)]
            if checked_word[0][0] != word:
                count += 1
        return count

    # count number of characters
    def get_char_count(self):
        return len(self.text.replace(" ", ""))

    # correct mispelling and grammer errors in text
    def correct_text(self):
        tool = LanguageToolPublicAPI("en-US")
        mispelled = self.get_mispelled()
        text = self.text
        for i in range(len(mispelled)):
            d = mispelled[i]
            wrong = d.get("mispelled")
            correct = d.get("correct")
            text = text.replace(wrong, correct)
        corrected_text = tool.correct(text)
        return corrected_text

    # get the grade level of text
    def get_grade(self):
        if self.get_word_count() > 100:
            r = Readability(self.text)
            fk = r.flesch_kincaid()
            return fk.grade_level
        else:
            # count the number of letters
            letter_count = 0
            word_count = self.get_word_count()
            sentences_count = self.get_sentences_count()
            if sentences_count == 0:
                sentences_count += 1
            for c in self.text:
                if c.isalpha():
                    letter_count += 1
            # L is the average number of letters per 100 words in the text
            L = letter_count / word_count * 100
            # S is the average number of sentences per 100 words in the text
            S = sentences_count / word_count * 100
            # Grade Level = 0.0588 * L - 0.296 * S - 15.8
            grade = int(0.0588 * L - 0.296 * S - 15.8)
            if grade < 0:
                return "Less than 1"
            if grade > 16:
                return "Higher than 16"
            return round(grade)
