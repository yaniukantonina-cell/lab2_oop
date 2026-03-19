class StringBuilder:
    def __init__(self, text=""):
        self.chars = list(text)

    def to_string(self):
        return "".join(self.chars)

    def find(self, char, start=0, end=None):
        if end is None:
            end = len(self.chars)

        try:
            return self.chars.index(char, start, end)
        except ValueError:
            return -1

    def rfind(self, char, start=0, end=None):
        if end is None:
            end = len(self.chars)

        for i in range(end -1, start-1, -1):
            if self.chars[i] == char:
                return i
        return -1

    def delete(self, start, end):
        del self.chars[start:end]

    def length(self):
        return len(self.chars)

    def char_idx(self, index):
        return self.chars[index]

class TextMod:
    def remove_longest(self, sentence, start, end, start_l, end_l):
        first_idx = sentence.find(start_l, start, end)
        last_idx = sentence.rfind(end_l, start, end)

        if first_idx != -1 and last_idx != -1 and first_idx <= last_idx:
            sentence.delete(first_idx, last_idx + 1)
            return (last_idx + 1) - first_idx

        return 0

    def eval_sentences(self, sentence, start_l, end_l):
        sentence_start = 0
        i = 0

        while i < sentence.length():
            char = sentence.char_idx(i)

            if char in ['.', '!', '?'] or i == sentence.length() - 1:
                sentence_end = i + 1

                del_length = self.remove_longest(sentence, sentence_start, sentence_end, start_l, end_l)

                i -= del_length
                sentence_end -= del_length

                sentence_start = sentence_end

            i += 1

    def text(self):
        try:
            raw_text = "Перше речення - на перевірку! Друге після першого. Третє - останнє?"
            start_char = "е"
            end_char = "н"

            if not raw_text:
                raise ValueError("текст відсутній")

            if not isinstance(start_char, str) or len(start_char) != 1:
                raise ValueError("Початкова літера не один символ")

            if not isinstance(end_char, str) or len(end_char) != 1:
                raise ValueError("Кінцева літера не один символ")

            sentence = StringBuilder(raw_text)
            self.eval_sentences(sentence, start_char, end_char)
            final_text = sentence.to_string()

            print(f"Початковий текст:\n{raw_text}\n")
            print(f'Шуканий підрядок:\nвід "{start_char}" до "{end_char}"\n')
            print(f"Результат:\n{final_text}")

        except ValueError as ve:
            print(f"Помилка вхідних даних {ve}")
        except IndexError as ie:
            print(f"Вихід за межі масиву символів {ie}")
        except Exception as e:
            print(f"Непередбачена помилка {e}")

if __name__ == "__main__":
    test = TextMod()
    test.text()