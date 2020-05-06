import unittest
from source.objects.env_to_json import env_to_json
from io import StringIO
from json import load


class EnvToJsonTestCase(unittest.TestCase):
    def test_enable_env(self):
        test_env = {
            "ENABLE_ENV": True,
            "test@category": "test_category"
        }
        expected_result = {
            "test": {
                "category": "test_category"
            }
        }
        with StringIO() as file_open:
            result = env_to_json(file_open, test_env)
            self.assertEqual(True, result)
            file_open.seek(0)
            self.assertEqual(expected_result, load(file_open))

    def test_disable_env(self):
        with StringIO() as file_open:
            self.assertEqual(False, env_to_json(file_open, dict()))
            file_open.seek(0)
            self.assertEqual("", file_open.read())

    def test_populate_dict(self):
        test_env = {
            "ENABLE_ENV": True,
            "test@category": "test_category",
            "test@category2": "test_category2",
            "test2@category": "test2_category",
            "test2@category2": [
                1,
                2,
                3
            ]
        }
        expected_result = {
            "test": {
                "category": "test_category",
                "category2": "test_category2"
            },
            "test2": {
                "category": "test2_category",
                "category2": [
                    1,
                    2,
                    3
                ]
            }
        }
        with StringIO() as file_open:
            result = env_to_json(file_open, test_env)
            self.assertEqual(True, result)
            file_open.seek(0)
            self.assertEqual(expected_result, load(file_open))


if __name__ == '__main__':
    unittest.main()
