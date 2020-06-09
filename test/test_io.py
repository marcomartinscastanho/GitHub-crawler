import unittest
import json
from src.io import read_command_args, decode_input, write_output


class TestReadCommandArgs(unittest.TestCase):
    def test_ok(self):
        input_fn, output_fn = read_command_args(["-i", "input.json", "-o", "output.json"])
        self.assertEqual(input_fn, "input.json")
        self.assertEqual(output_fn, "output.json")

    def test_input_missing(self):
        with self.assertRaises(SystemExit) as cm:
            read_command_args(["-o", "output.json"])

        self.assertEqual(cm.exception.code, 3)

    def test_output_missing(self):
        with self.assertRaises(SystemExit) as cm:
            read_command_args(["-i", "input.json"])

        self.assertEqual(cm.exception.code, 3)

    def test_help(self):
        with self.assertRaises(SystemExit) as cm:
            read_command_args(["-h"])

        self.assertEqual(cm.exception.code, None)


class TestDecodeInput(unittest.TestCase):
    def test_ok(self):
        expected_json_input = {
            "keywords": [
                "openstack",
                "nova",
                "css"
            ],
            "proxies": [
                "194.126.37.94:8080",
                "13.78.125.167:8080"
            ],
            "type": "Repositories"
        }

        real_json_input = decode_input("input_ex1.json")
        self.assertDictEqual(expected_json_input, real_json_input)

    def test_missing_keywords(self):
        with self.assertRaises(SystemExit) as cm:
            decode_input("input_ex1_missing_keywords.json")

        self.assertEqual(cm.exception.code, 2)

    def test_missing_proxies(self):
        with self.assertRaises(SystemExit) as cm:
            decode_input("input_ex1_missing_proxies.json")

        self.assertEqual(cm.exception.code, 3)

    def test_malformatted_input(self):
        with self.assertRaises(SystemExit) as cm:
            decode_input("input_ex1_malformatted.json")

        self.assertEqual(cm.exception.code, 4)


class TestWriteOutput(unittest.TestCase):
    def test_ex1_repositories(self):
        json_output = [
            {"url": "https://github.com/atuldjadhav/DropBox-Cloud-Storage"},
            {"url": "https://github.com/michealbalogun/Horizon-dashboard"}
        ]

        write_output(json_output, "test_output.json")

        with open("test_output.json") as output_file:
            file_content = json.load(output_file)
            self.assertListEqual(json_output, file_content)

    def test_ex2_issues(self):
        json_output = [
            {"url": "https://github.com/RealmTeam/django-rest-framework-social-oauth2/issues/223"},
            {"url": "https://github.com/jpadilla/django-rest-framework-jwt/issues/462"},
            {"url": "https://github.com/Styria-Digital/django-rest-framework-jwt/issues/4"},
            {"url": "https://github.com/SimpleJWT/django-rest-framework-simplejwt/issues/71"},
            {"url": "https://github.com/lock8/django-rest-framework-jwt-refresh-token/pull/50"},
            {"url": "https://github.com/juanifioren/django-oidc-provider/issues/78"},
            {"url": "https://github.com/apluslms/mooc-grader/issues/65"},
            {"url": "https://github.com/jpadilla/django-rest-framework-jwt/issues/440"},
            {"url": "https://github.com/jpadilla/pyjwt/issues/408"},
            {"url": "https://github.com/Styria-Digital/django-rest-framework-jwt/issues/53"}
        ]

        write_output(json_output, "test_output.json")

        with open("test_output.json") as output_file:
            file_content = json.load(output_file)
            self.assertListEqual(json_output, file_content)
