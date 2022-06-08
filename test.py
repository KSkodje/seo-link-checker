import unittest

from report import remove_none_values, sort_pages
from crawl import normalize_url, get_urls_from_string


class Tests(unittest.TestCase):
    def test_remove_none_values(self):
        self.assertEqual({}, remove_none_values({"1": None}))
        self.assertEqual({"1": "1"}, remove_none_values({"1": "1", "2": None}))
        self.assertEqual({}, remove_none_values({}))
        self.assertEqual({"1": "1"}, remove_none_values({"1": "1"}))

    def test_sort_pages(self):
        self.assertEqual([("first", 45), ("second", 25), ("third", 15)],
                         sort_pages({"first": 45, "third": 15, "second": 25}))

    def test_get_urls_from_string(self):
        self.assertEqual(
            ["https://blog.boot.dev"],
            get_urls_from_string(
                '<html><body><a href="https://blog.boot.dev"><span>Boot.dev></span></a></body></html>',
                "https://blog.boot.dev",
            ),
        )
        self.assertEqual(
            ["https://blog.boot.dev", "https://wagslane.dev"],
            get_urls_from_string(
                '<html><body><a href="https://blog.boot.dev"><span>Boot.dev></span></a>\
                <a href="https://wagslane.dev"><span>Boot.dev></span></a></body></html>',
                "https://blog.boot.dev",
            ),
        )

    def test_normalize_url(self):
        self.assertEqual('boot.dev', normalize_url("https://Boot.dev"))
        self.assertEqual('boot.dev', normalize_url("http:/boot.dev"))
        self.assertEqual('boot.dev', normalize_url("http://boot.dev/"))
        self.assertEqual('boot.dev', normalize_url("https://boot.dev#header"))
        self.assertEqual('boot.dev', normalize_url("https://boot.dev?via=lane"))


if __name__ == "__main__":
    unittest.main()
