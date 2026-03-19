import unittest
from unittest.mock import patch
from io import StringIO
from lab2_oop import StringBuilder, TextMod


class TestStringBuilderInit(unittest.TestCase):

    def test_init_with_text(self):
        sb = StringBuilder("hello")
        self.assertEqual(sb.to_string(), "hello")

    def test_init_empty(self):
        sb = StringBuilder()
        self.assertEqual(sb.to_string(), "")

    def test_init_empty_string(self):
        sb = StringBuilder("")
        self.assertEqual(sb.to_string(), "")

    def test_init_stores_as_list(self):
        sb = StringBuilder("abc")
        self.assertIsInstance(sb.chars, list)
        self.assertEqual(sb.chars, ['a', 'b', 'c'])


class TestStringBuilderLength(unittest.TestCase):

    def test_length_nonempty(self):
        sb = StringBuilder("hello")
        self.assertEqual(sb.length(), 5)

    def test_length_empty(self):
        sb = StringBuilder()
        self.assertEqual(sb.length(), 0)

    def test_length_single_char(self):
        sb = StringBuilder("x")
        self.assertEqual(sb.length(), 1)

    def test_length_after_delete(self):
        sb = StringBuilder("hello")
        sb.delete(0, 2)
        self.assertEqual(sb.length(), 3)


class TestStringBuilderToString(unittest.TestCase):

    def test_to_string_basic(self):
        sb = StringBuilder("world")
        self.assertEqual(sb.to_string(), "world")

    def test_to_string_empty(self):
        sb = StringBuilder()
        self.assertEqual(sb.to_string(), "")

    def test_to_string_returns_str(self):
        sb = StringBuilder("abc")
        self.assertIsInstance(sb.to_string(), str)


class TestStringBuilderCharIdx(unittest.TestCase):

    def test_char_idx_first(self):
        sb = StringBuilder("hello")
        self.assertEqual(sb.char_idx(0), 'h')

    def test_char_idx_last(self):
        sb = StringBuilder("hello")
        self.assertEqual(sb.char_idx(4), 'o')

    def test_char_idx_middle(self):
        sb = StringBuilder("abcde")
        self.assertEqual(sb.char_idx(2), 'c')


class TestStringBuilderFind(unittest.TestCase):

    def test_find_first_occurrence(self):
        sb = StringBuilder("abcabc")
        self.assertEqual(sb.find('a'), 0)

    def test_find_not_found(self):
        sb = StringBuilder("hello")
        self.assertEqual(sb.find('z'), -1)

    def test_find_with_start(self):
        sb = StringBuilder("abcabc")
        self.assertEqual(sb.find('a', 1), 3)

    def test_find_with_start_excludes_match(self):
        sb = StringBuilder("abcde")
        self.assertEqual(sb.find('b', 2), -1)

    def test_find_with_start_and_end(self):
        sb = StringBuilder("abcabc")
        self.assertEqual(sb.find('c', 0, 3), 2)

    def test_find_with_end_excludes_match(self):
        sb = StringBuilder("abcabc")
        self.assertEqual(sb.find('c', 0, 2), -1)

    def test_find_single_char_string(self):
        sb = StringBuilder("a")
        self.assertEqual(sb.find('a'), 0)

    def test_find_empty_string(self):
        sb = StringBuilder()
        self.assertEqual(sb.find('a'), -1)

    def test_find_cyrillic(self):
        sb = StringBuilder("Привіт")
        self.assertEqual(sb.find('і'), 4)


class TestStringBuilderRfind(unittest.TestCase):

    def test_rfind_last_occurrence(self):
        sb = StringBuilder("abcabc")
        self.assertEqual(sb.rfind('a'), 3)

    def test_rfind_not_found(self):
        sb = StringBuilder("hello")
        self.assertEqual(sb.rfind('z'), -1)

    def test_rfind_single_occurrence(self):
        sb = StringBuilder("abcde")
        self.assertEqual(sb.rfind('c'), 2)

    def test_rfind_with_end(self):
        sb = StringBuilder("abcabc")
        self.assertEqual(sb.rfind('a', 0, 3), 0)

    def test_rfind_with_end_excludes(self):
        sb = StringBuilder("abcabc")
        self.assertEqual(sb.rfind('b', 0, 1), -1)

    def test_rfind_empty_string(self):
        sb = StringBuilder()
        self.assertEqual(sb.rfind('a'), -1)

    def test_rfind_cyrillic(self):
        sb = StringBuilder("Привіт, світе!")
        self.assertEqual(sb.rfind('і'), 10)


class TestStringBuilderDelete(unittest.TestCase):

    def test_delete_from_start(self):
        sb = StringBuilder("hello world")
        sb.delete(0, 6)
        self.assertEqual(sb.to_string(), "world")

    def test_delete_from_middle(self):
        sb = StringBuilder("abcdef")
        sb.delete(2, 4)
        self.assertEqual(sb.to_string(), "abef")

    def test_delete_to_end(self):
        sb = StringBuilder("hello world")
        sb.delete(5, 11)
        self.assertEqual(sb.to_string(), "hello")

    def test_delete_all(self):
        sb = StringBuilder("hello")
        sb.delete(0, 5)
        self.assertEqual(sb.to_string(), "")

    def test_delete_single_char(self):
        sb = StringBuilder("abcde")
        sb.delete(2, 3)
        self.assertEqual(sb.to_string(), "abde")

    def test_delete_updates_length(self):
        sb = StringBuilder("hello")
        sb.delete(0, 3)
        self.assertEqual(sb.length(), 2)


class TestTextModRemoveLongest(unittest.TestCase):

    def setUp(self):
        self.mod = TextMod()

    def test_remove_longest_basic(self):
        sb = StringBuilder("abcde.")
        removed = self.mod.remove_longest(sb, 0, 6, 'b', 'd')
        self.assertEqual(sb.to_string(), "ae.")
        self.assertEqual(removed, 3)

    def test_remove_longest_no_start(self):
        sb = StringBuilder("abcde.")
        removed = self.mod.remove_longest(sb, 0, 6, 'z', 'd')
        self.assertEqual(sb.to_string(), "abcde.")
        self.assertEqual(removed, 0)

    def test_remove_longest_no_end(self):
        sb = StringBuilder("abcde.")
        removed = self.mod.remove_longest(sb, 0, 6, 'b', 'z')
        self.assertEqual(sb.to_string(), "abcde.")
        self.assertEqual(removed, 0)

    def test_remove_longest_start_after_end(self):
        sb = StringBuilder("abcde.")
        removed = self.mod.remove_longest(sb, 0, 6, 'd', 'b')
        self.assertEqual(sb.to_string(), "abcde.")
        self.assertEqual(removed, 0)

    def test_remove_longest_same_char(self):
        sb = StringBuilder("aXXXa.")
        removed = self.mod.remove_longest(sb, 0, 6, 'a', 'a')
        self.assertEqual(sb.to_string(), ".")
        self.assertEqual(removed, 5)

    def test_remove_longest_returns_int(self):
        sb = StringBuilder("abc.")
        result = self.mod.remove_longest(sb, 0, 4, 'a', 'c')
        self.assertIsInstance(result, int)


class TestTextModEvalSentences(unittest.TestCase):

    def setUp(self):
        self.mod = TextMod()

    def test_eval_basic(self):
        sb = StringBuilder("abcdef. ghijkl!")
        self.mod.eval_sentences(sb, 'b', 'e')
        self.assertEqual(sb.to_string(), "af. ghijkl!")

    def test_eval_no_matches(self):
        sb = StringBuilder("Тут немає потрібних літер.")
        self.mod.eval_sentences(sb, 'щ', 'ю')
        self.assertEqual(sb.to_string(), "Тут немає потрібних літер.")

    def test_eval_empty_string(self):
        sb = StringBuilder("")
        self.mod.eval_sentences(sb, 'a', 'b')
        self.assertEqual(sb.to_string(), "")

    def test_eval_no_sentence_delimiters(self):
        sb = StringBuilder("no delim here")
        self.mod.eval_sentences(sb, 'e', 'r')
        self.assertEqual(sb.to_string(), "no de")

    def test_eval_match_in_both_sentences(self):
        sb = StringBuilder("find. find!")
        self.mod.eval_sentences(sb, 'f', 'd')
        self.assertEqual(sb.to_string(), ". !")

    def test_eval_exclamation_delimiter(self):
        sb = StringBuilder("hello!")
        self.mod.eval_sentences(sb, 'e', 'o')
        self.assertEqual(sb.to_string(), "h!")

    def test_eval_question_delimiter(self):
        sb = StringBuilder("hello?")
        self.mod.eval_sentences(sb, 'e', 'o')
        self.assertEqual(sb.to_string(), "h?")

    def test_eval_dot_delimiter(self):
        sb = StringBuilder("abc.")
        self.mod.eval_sentences(sb, 'a', 'c')
        self.assertEqual(sb.to_string(), ".")

    def test_eval_cyrillic(self):
        sb = StringBuilder("Перше речення.")
        self.mod.eval_sentences(sb, 'е', 'н')
        self.assertEqual(sb.to_string(), "Пя.")


class TestTextModText(unittest.TestCase):

    def setUp(self):
        self.mod = TextMod()

    def test_text_runs_without_error(self):
        try:
            with patch('sys.stdout', new=StringIO()):
                self.mod.text()
        except Exception as e:
            self.fail(f"text() викинув виняток: {e}")

    def test_text_prints_original(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.mod.text()
            output = fake_out.getvalue()
        self.assertIn("Початковий текст", output)

    def test_text_prints_result(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.mod.text()
            output = fake_out.getvalue()
        self.assertIn("Результат", output)

    def test_text_prints_search_chars(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.mod.text()
            output = fake_out.getvalue()
        self.assertIn("Шуканий підрядок", output)


if __name__ == '__main__':
    unittest.main()