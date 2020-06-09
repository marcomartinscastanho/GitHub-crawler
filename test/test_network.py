import unittest
from src.network import encode_request, get_random_proxy, send, decode_query_response, decode_language_stats, add_extra_information


class TestEncodeRequest(unittest.TestCase):
    def test_ex1_ok(self):
        json_input = {
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

        expected_url = "https://github.com/search?q=openstack+nova+css&type=Repositories"
        real_url = encode_request(json_input)

        self.assertEqual(expected_url, real_url)

    def test_ex2_ok(self):
        json_input = {
            "keywords": [
                "python",
                "django-rest-framework",
                "jwt"
            ],
            "proxies": [
                "194.126.37.94:8080",
                "13.78.125.167:8080"
            ],
            "type": "Issues"
        }

        expected_url = "https://github.com/search?q=python+django-rest-framework+jwt&type=Issues"
        real_url = encode_request(json_input)

        self.assertEqual(expected_url, real_url)

    def test_ex1_no_type(self):
        json_input = {
            "keywords": [
                "openstack",
                "nova",
                "css"
            ],
            "proxies": [
                "194.126.37.94:8080",
                "13.78.125.167:8080"
            ],
        }

        expected_url = "https://github.com/search?q=openstack+nova+css"
        real_url = encode_request(json_input)

        self.assertEqual(expected_url, real_url)


class TestGetRandomProxy(unittest.TestCase):
    def test_ex1(self):
        json_input = {
            "keywords": [
                "openstack",
                "nova",
                "css"
            ],
            "proxies": [
                "194.126.37.94:8080",
                "13.78.125.167:8080"
            ],
        }

        random_proxy = get_random_proxy(json_input)

        self.assertIn(random_proxy, json_input["proxies"])

    def test_ex1_only_1_proxy(self):
        json_input = {
            "keywords": [
                "openstack",
                "nova",
                "css"
            ],
            "proxies": [
                "194.126.37.94:8080"
            ],
        }

        random_proxy = get_random_proxy(json_input)

        self.assertEqual(random_proxy, "194.126.37.94:8080")


class TestSend(unittest.TestCase):
    def setUp(self) -> None:
        # FIXME: check if there's a better one
        self.proxy = "103.78.75.165:8080"

    def test_ex1_repositories(self):
        request_url = "https://github.com/search?q=openstack+nova+css&type=Repositories"

        response = send(request_url, self.proxy)

        self.assertEqual(response["code"], 200)
        self.assertEqual(response["encoding"], "utf-8")

    def test_ex1_no_type(self):
        request_url = "https://github.com/search?q=openstack+nova+css"

        response = send(request_url, self.proxy)

        self.assertEqual(response["code"], 200)
        self.assertEqual(response["encoding"], "utf-8")

    def test_ex2_issues(self):
        request_url = "https://github.com/search?q=python+django-rest-framework+jwt&type=Issues"

        response = send(request_url, self.proxy)

        self.assertEqual(response["code"], 200)
        self.assertEqual(response["encoding"], "utf-8")

    def test_ex3_wikis(self):
        request_url = "https://github.com/search?q=python+django-rest-framework+jwt&type=Wikis"

        response = send(request_url, self.proxy)

        self.assertEqual(response["code"], 200)
        self.assertEqual(response["encoding"], "utf-8")


class TestDecodeResponse(unittest.TestCase):
    def test_ex1_repositories(self):
        expected_output = [
            {"url": "https://github.com/atuldjadhav/DropBox-Cloud-Storage"},
            {"url": "https://github.com/michealbalogun/Horizon-dashboard"}
        ]

        with open("ex1_raw_response.html") as response_html:
            actual_response = decode_query_response(response_html)
            self.assertListEqual(expected_output, actual_response)

            for result in actual_response:
                self.assertEqual(len(result.keys()), 1)
                self.assertIn("url", result.keys())
                # TODO: check if it has an url format

    def test_ex2_issues(self):
        expected_output = [
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

        with open("ex2_raw_response.html") as response_html:
            actual_response = decode_query_response(response_html)
            self.assertListEqual(expected_output, actual_response)

            for result in actual_response:
                self.assertEqual(len(result.keys()), 1)
                self.assertIn("url", result.keys())
                # TODO: check if it has an url format

    def test_ex3_wikis(self):
        expected_output = [
            {"url": "https://github.com/JeongtaekLim/TIL/wiki/JWT,-Superuser"},
            {"url": "https://github.com/ninemilli-song/all-season-investor/wiki/%E5%AD%A6%E4%B9%A0%E8%B7%AF%E5%BE%84"},
            {"url": "https://github.com/Altiimax/DevWebProject/wiki/12_References"},
            {"url": "https://github.com/Larissa-Developers/prizy_backend/wiki/Knowledge-Base"},
            {"url": "https://github.com/Altiimax/DevWebProject/wiki/12.References"},
            {"url": "https://github.com/Altiimax/DevWebProject/wiki/Links&references"},
            {"url": "https://github.com/tsrnd/dp-yashoes/wiki/Authenticate-package-in-django"},
            {"url": "https://github.com/balakrishnanm/mybook/wiki/Django-Authentication"},
            {"url": "https://github.com/arkwith7/arkwith-app-template/wiki/%EC%95%84%ED%81%AC%EC%9C%84%EB%93%9C-%EC%8A%A4%ED%83%80%ED%84%B0-%ED%85%9C%ED%94%8C%EB%A6%AC%ED%8A%B8%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%9C-%EC%83%88%EB%A1%9C%EC%9A%B4-%EA%B8%B0%EB%8A%A5-%EA%B0%9C%EB%B0%9C-%EB%B0%A9%EB%B2%95"},
            {"url": "https://github.com/PartyGwam/api/wiki/%EA%B8%B0%EC%88%A0-%EC%8A%A4%ED%83%9D"}
        ]

        with open("ex3_raw_response.html", encoding='utf8') as response_html:
            actual_response = decode_query_response(response_html)
            self.assertListEqual(expected_output, actual_response)

            for result in actual_response:
                self.assertEqual(len(result.keys()), 1)
                self.assertIn("url", result.keys())


class TestDecodeLanguageStats(unittest.TestCase):
    def test_ok(self):
        expected_output = {
                     "CSS": 52,
                     "JavaScript": 47.2,
                     "HTML": 0.8
                 }

        with open("ex1_details_response.html", encoding='utf8') as response_html:
            actual_output = decode_language_stats(response_html)
            self.assertDictEqual(expected_output, actual_output)


class TestAddExtraInformation(unittest.TestCase):
    def setUp(self) -> None:
        # FIXME: check if there's a better one
        self.proxy = "45.64.99.26:8080"

    def test_ok(self):
        expected = [
            {
                "url": "https://github.com/atuldjadhav/DropBox-Cloud-Storage",
                "extra": {
                    "owner": "atuldjadhav",
                    "language_stats": {
                        "CSS": 52,
                        "JavaScript": 47.2,
                        "HTML": 0.8
                    }
                }
            },
            {
                "url": "https://github.com/michealbalogun/Horizon-dashboard",
                "extra": {
                    "owner": "michealbalogun",
                    "language_stats": {
                        "Python": 100.0
                    }
                }
            }
        ]
        actual = [
            {"url": "https://github.com/atuldjadhav/DropBox-Cloud-Storage"},
            {"url": "https://github.com/michealbalogun/Horizon-dashboard"}
        ]

        add_extra_information(actual, self.proxy)
        self.assertListEqual(expected, actual)
