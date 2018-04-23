from tests.test_base import BaseTestCase
import json
import unittest
from inkit_project.resources import validate_json


class TestContactCollectionRoute(BaseTestCase):

    def test_get_empty(self):
        response = self.simulate_request('/contacts', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response)

        self.assertEqual(response[0], b'[]')

    def test_get_after_post(self):
        post = {
            "first_name": "Adam",
            "last_name": "Smith",
            "email": "asmith@macalester.edu",
            "address": {
                "street_address": "1600 Grand Avenue",
                "unit_number": "Macalester College",
                "city": "St. Paul",
                "state": "MN",
                "post_code": "55105"
            }
        }

        self.simulate_request('/contacts', method='POST', body=json.dumps(post), headers={'Content-Type': 'application/json'})

        response = self.simulate_request('/contacts', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response)
        try:
            validate_json(json.loads(response[0].decode('utf-8')))
        except AssertionError:
            self.fail()

    def test_get_multiple(self):
        post = [
            {
                "first_name": "Juan David",
                "last_name": "Garrido",
                "email": "jgarrido@macalester.edu",
                "address": {
                    "street_address": "1600 Grand Avenue",
                    "unit_number": "Macalester College",
                    "city": "St. Paul",
                    "state": "MN",
                    "post_code": "55105"
                }
            },
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@macalester.edu",
                "address": {
                    "street_address": "1600 Pennsilvania Avenue",
                    "unit_number": "White Oval",
                    "city": "Washington",
                    "state": "MD",
                    "country": "Colombia",
                    "post_code": "11111"
                }
            }]

        self.simulate_request('/contacts', method='POST', body=json.dumps(post), headers={'Content-Type': 'application/json'})

        response = self.simulate_request('/contacts', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response)
        self.assertEqual(len(json.loads(response[0].decode('utf-8'))), 2)

        try:
            validate_json(json.loads(response[0].decode('utf-8')))
        except AssertionError:
            self.fail()

    def test_get_invalid_endpoint(self):
        response = self.simulate_request('/invalid', method='GET', headers={'Accept': 'application/json'})
        self.assertNotFound(response)

    def test_delete(self):
        response = self.simulate_request('/contacts', method='DELETE')
        self.assertMethodNotAllowed(response)

    def test_put(self):
        response = self.simulate_request('/contacts', method='PUT')
        self.assertMethodNotAllowed(response)

    def test_patch(self):
        response = self.simulate_request('/contacts', method='PATCH')
        self.assertMethodNotAllowed(response)

    def test_custom_method(self):
        response = self.simulate_request('/contacts', method='CUSTOM')
        self.assertBadRequest(response, 'Bad request', 'Invalid HTTP method')


class TestContactsPost(BaseTestCase):

    def test_post_only_required(self):
        post = {
                "first_name": "Adam",
                "last_name": "Smith",
                "email": "asmith@macalester.edu",
                "address": {
                    "street_address": "1600 Grand Avenue",
                    "unit_number": "Macalester College",
                    "city": "St. Paul",
                    "state": "MN",
                    "post_code": "55105"
                }
            }

        response = self.simulate_request('/contacts', method='POST', body=json.dumps(post), headers={'Content-Type': 'application/json'})
        self.assertCreated(response)

    def test_post_all_properties(self):
        post = {
            "first_name": "Juan David",
            "last_name": "Garrido",
            "email": "jgarrido@macalester.edu",
            "phone_number": "7632830994",
            "company": "Inkit",
            "address": {
                "street_address": "1600 Grand Avenue",
                "unit_number": "Macalester College",
                "city": "St. Paul",
                "state": "MN",
                "country": "Colombia",
                "post_code": "55105"
            },
            "notes": "This is a difficult project"
        }

        response = self.simulate_request('/contacts', method='POST', body=json.dumps(post), headers={'Content-Type': 'application/json'})
        self.assertCreated(response)

    def test_post_multiple(self):
        post = [
            {
                "first_name": "Juan David",
                "last_name": "Garrido",
                "email": "jgarrido@macalester.edu",
                "address": {
                    "street_address": "1600 Grand Avenue",
                    "unit_number": "Macalester College",
                    "city": "St. Paul",
                    "state": "MN",
                    "post_code": "55105"
                }
            },
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@macalester.edu",
                "address": {
                    "street_address": "1600 Pennsilvania Avenue",
                    "unit_number": "White Oval",
                    "city": "Washington",
                    "state": "MD",
                    "country": "Colombia",
                    "post_code": "11111"
                }
            }]

        response = self.simulate_request('/contacts', method='POST', body=json.dumps(post), headers={'Content-Type': 'application/json'})
        self.assertCreated(response)

    def test_post_all_required_one_null(self):
        post = {
            "first_name": None,
            "last_name": "Smith",
            "email": "asmith@macalester.edu",
            "address": {
                "street_address": "1600 Grand Avenue",
                "unit_number": "Macalester College",
                "city": "St. Paul",
                "state": "MN",
                "post_code": "55105"
            }
        }

        response = self.simulate_request('/contacts', method='POST', body=json.dumps(post), headers={'Content-Type': 'application/json'})
        self.assertFailValidation(response, "None is not of type 'string'")

    def test_post_missing_required(self):
        post = {
            "last_name": "No first name",
            "email": "asmith@macalester.edu",
            "address": {
                "street_address": "1600 Grand Avenue",
                "unit_number": "Macalester College",
                "city": "St. Paul",
                "state": "MN",
                "post_code": "55105"
            }
        }

        response = self.simulate_request('/contacts', method='POST', body=json.dumps(post), headers={'Content-Type': 'application/json'})
        self.assertFailValidation(response, "'first_name' is a required property")

    def test_post_wrong_type(self):
        post = {
            "first_name": "Adam",
            "last_name": "No first name",
            "email": "asmith@macalester.edu",
            "phone_number": 1234567890,
            "address": {
                "street_address": "1600 Grand Avenue",
                "unit_number": "Macalester College",
                "city": "St. Paul",
                "state": "MN",
                "post_code": "55105"
            }
        }

        response = self.simulate_request('/contacts', method='POST', body=json.dumps(post), headers={'Content-Type': 'application/json'})
        self.assertFailValidation(response, "1234567890 is not of type 'string', 'null'")

    def test_post_extra_property(self):
        post = {
            "first_name": "Juan David",
            "last_name": "Garrido",
            "email": "jgarrido@macalester.edu",
            "phone_number": "7632830994",
            "company": "Inkit",
            "address": {
                "street_address": "1600 Grand Avenue",
                "unit_number": "Macalester College",
                "city": "St. Paul",
                "state": "MN",
                "country": "Colombia",
                "post_code": "55105"
            },
            "notes": "This is a difficult project",
            "unknown": "What am I doing here"
        }

        response = self.simulate_request('/contacts', method='POST', body=json.dumps(post), headers={'Content-Type': 'application/json'})
        self.assertFailValidation(response, "Additional properties are not allowed ('unknown' was unexpected)")

    def test_post_invalid_content_type(self):
        response = self.simulate_request('/contacts', method='POST', body=json.dumps({}), headers={'Content-Type': 'application/xml'})
        self.assertUnsupportedMediaType(response)

    def test_post_invalid_json_file(self):
        invalid_file = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        response = self.simulate_request('/contacts', method='POST', body=invalid_file, headers={'Content-Type': 'application/json'})
        self.assertFailValidation(response, 'b\'' + invalid_file + '\'' + " is not of type 'object', 'array'")


class TestSingleContactRoute(BaseTestCase):

    def test_get(self):
        response = self.simulate_request('/contacts/1', method='GET', headers={'Accept': 'application/json'})
        self.assertNotFound(response)

        post = {
            "first_name": "Adam",
            "last_name": "Smith",
            "email": "asmith@macalester.edu",
            "address": {
                "street_address": "1600 Grand Avenue",
                "unit_number": "Macalester College",
                "city": "St. Paul",
                "state": "MN",
                "post_code": "55105"
            }
        }

        self.simulate_request('/contacts', method='POST', body=json.dumps(post), headers={'Content-Type': 'application/json'})

        response = self.simulate_request('/contacts/1', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response)
        try:
            validate_json(json.loads(response[0].decode('utf-8')))
        except AssertionError:
            self.fail()

        post = [
            {
                "first_name": "Juan David",
                "last_name": "Garrido",
                "email": "jgarrido@macalester.edu",
                "address": {
                    "street_address": "1600 Grand Avenue",
                    "unit_number": "Macalester College",
                    "city": "St. Paul",
                    "state": "MN",
                    "post_code": "55105"
                }
            },
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@macalester.edu",
                "address": {
                    "street_address": "1600 Pennsilvania Avenue",
                    "unit_number": "White Oval",
                    "city": "Washington",
                    "state": "MD",
                    "country": "Colombia",
                    "post_code": "11111"
                }
            }]

        self.simulate_request('/contacts', method='POST', body=json.dumps(post), headers={'Content-Type': 'application/json'})

        response = self.simulate_request('/contacts/2', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response)
        try:
            validate_json(json.loads(response[0].decode('utf-8')))
        except AssertionError:
            self.fail()

        response = self.simulate_request('/contacts/3', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response)
        try:
            validate_json(json.loads(response[0].decode('utf-8')))
        except AssertionError:
            self.fail()

    def test_delete(self):
        self.test_get()

        response = self.simulate_request('/contacts/1', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response)

        response = self.simulate_request('/contacts/1', method='DELETE')
        self.assertOK(response)

        response = self.simulate_request('/contacts/1', method='GET', headers={'Accept': 'application/json'})
        self.assertNotFound(response)

    def test_put(self):
        self.test_get()

        response_before_put = self.simulate_request('/contacts/1', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response_before_put)

        response_before_put2 = self.simulate_request('/contacts/1', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response_before_put)

        put = {
            "first_name": "Another David",
            "last_name": "Garrido",
            "email": "jgarrido@macalester.edu",
            "phone_number": "7632830994",
            "company": "Inkit",
            "address": {
                "street_address": "1600 Grand Avenue",
                "unit_number": "Macalester College",
                "city": "St. Paul",
                "state": "MN",
                "country": "Colombia",
                "post_code": "55105"
            },
            "notes": "This is a difficult project"
        }

        response_put = self.simulate_request('/contacts/1', method='PUT', body=json.dumps(put), headers={'Content-Type': 'application/json'})
        self.assertOK(response_put)

        response_after_put = self.simulate_request('/contacts/1', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response_after_put)

        self.assertEqual(response_before_put, response_before_put2)
        self.assertNotEqual(response_before_put, response_after_put)

    def test_invalid_put(self):
        self.test_get()

        put = {
            "last_name": "Garrido",
            "email": "jgarrido@macalester.edu",
            "phone_number": "7632830994",
            "company": "Inkit",
            "address": {
                "street_address": "1600 Grand Avenue",
                "unit_number": "Macalester College",
                "city": "St. Paul",
                "state": "MN",
                "country": "Colombia",
                "post_code": "55105"
            },
            "notes": "This is a difficult project"
        }

        response_put = self.simulate_request('/contacts/1', method='PUT', body=json.dumps(put), headers={'Content-Type': 'application/json'})
        self.assertFailValidation(response_put, "'first_name' is a required property")

    def test_patch(self):
        self.test_get()

        response_before_patch = self.simulate_request('/contacts/1', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response_before_patch)

        response_before_patch2 = self.simulate_request('/contacts/1', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response_before_patch2)

        patch = {
            "first_name": "Another David",
        }

        response_patch = self.simulate_request('/contacts/1', method='PATCH', body=json.dumps(patch), headers={'Content-Type': 'application/json'})
        self.assertOK(response_patch)

        response_after_patch = self.simulate_request('/contacts/1', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response_after_patch)

        self.assertEqual(response_before_patch, response_before_patch2)
        self.assertNotEqual(response_before_patch, response_after_patch)

    def test_invalid_patch(self):
        self.test_get()

        patch = {
            "first_name": None,
        }

        response_patch = self.simulate_request('/contacts/1', method='PATCH', body=json.dumps(patch), headers={'Content-Type': 'application/json'})
        self.assertConflict(response_patch)

    def test_unknown_attribute_patch(self):
        self.test_get()

        response_before_patch = self.simulate_request('/contacts/1', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response_before_patch)

        patch = {
            "unknown": None,
        }

        response_patch = self.simulate_request('/contacts/1', method='PATCH', body=json.dumps(patch), headers={'Content-Type': 'application/json'})
        self.assertOK(response_patch)

        response_after_patch = self.simulate_request('/contacts/1', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response_after_patch)

        self.assertEqual(response_before_patch, response_after_patch)

    def test_post(self):
        response = self.simulate_request('/contacts/1', method='POST')
        self.assertMethodNotAllowed(response)

    def test_custom_method(self):
        response = self.simulate_request('/contacts/1', method='CUSTOM')
        self.assertBadRequest(response, 'Bad request', 'Invalid HTTP method')


class TestSingleAddressRoute(BaseTestCase):

    def test_get(self):
        response = self.simulate_request('/contacts/1/address', method='GET', headers={'Accept': 'application/json'})
        self.assertNotFound(response)

        post = {
            "first_name": "Adam",
            "last_name": "Smith",
            "email": "asmith@macalester.edu",
            "address": {
                "street_address": "1600 Grand Avenue",
                "unit_number": "Macalester College",
                "city": "St. Paul",
                "state": "MN",
                "post_code": "55105"
            }
        }

        self.simulate_request('/contacts', method='POST', body=json.dumps(post), headers={'Content-Type': 'application/json'})

        response = self.simulate_request('/contacts/1/address', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response)

        post = [
            {
                "first_name": "Juan David",
                "last_name": "Garrido",
                "email": "jgarrido@macalester.edu",
                "address": {
                    "street_address": "1600 Grand Avenue",
                    "unit_number": "Macalester College",
                    "city": "St. Paul",
                    "state": "MN",
                    "post_code": "55105"
                }
            },
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@macalester.edu",
                "address": {
                    "street_address": "1600 Pennsilvania Avenue",
                    "unit_number": "White Oval",
                    "city": "Washington",
                    "state": "MD",
                    "country": "Colombia",
                    "post_code": "11111"
                }
            }]

        self.simulate_request('/contacts', method='POST', body=json.dumps(post), headers={'Content-Type': 'application/json'})

        response = self.simulate_request('/contacts/2/address', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response)

        response = self.simulate_request('/contacts/3/address', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response)

    def test_post(self):
        response = self.simulate_request('/contacts/1/address', method='POST')
        self.assertMethodNotAllowed(response)

    def test_delete(self):
        response = self.simulate_request('/contacts/1/address', method='DELETE')
        self.assertMethodNotAllowed(response)

    def test_cascade_delete(self):
        self.test_get()

        response = self.simulate_request('/contacts/1/address', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response)

        response = self.simulate_request('/contacts/1', method='DELETE')
        self.assertOK(response)

        response = self.simulate_request('/addresses/1', method='GET', headers={'Accept': 'application/json'})
        print(response)
        self.assertNotFound(response)

    def test_put(self):
        response = self.simulate_request('/contacts/1/address', method='PUT')
        self.assertMethodNotAllowed(response)

    def test_patch(self):
        response = self.simulate_request('/contacts/1/address', method='PATCH')
        self.assertMethodNotAllowed(response)

    def test_custom_method(self):
        response = self.simulate_request('/contacts', method='CUSTOM')
        self.assertBadRequest(response, 'Bad request', 'Invalid HTTP method')


class TestAddressCollectionRoute(BaseTestCase):

    def test_get(self):
        response = self.simulate_request('/addresses', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response)
        self.assertEqual(response[0], b'[]')

        post = {
            "first_name": "Adam",
            "last_name": "Smith",
            "email": "asmith@macalester.edu",
            "address": {
                "street_address": "1600 Grand Avenue",
                "unit_number": "Macalester College",
                "city": "St. Paul",
                "state": "MN",
                "post_code": "55105"
            }
        }

        self.simulate_request('/contacts', method='POST', body=json.dumps(post), headers={'Content-Type': 'application/json'})

        response = self.simulate_request('/addresses', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response)
        self.assertEqual(len(json.loads(response[0].decode('utf-8'))), 1)

        post = [
            {
                "first_name": "Juan David",
                "last_name": "Garrido",
                "email": "jgarrido@macalester.edu",
                "address": {
                    "street_address": "1600 Grand Avenue",
                    "unit_number": "Macalester College",
                    "city": "St. Paul",
                    "state": "MN",
                    "post_code": "55105"
                }
            },
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@macalester.edu",
                "address": {
                    "street_address": "1600 Pennsilvania Avenue",
                    "unit_number": "White Oval",
                    "city": "Washington",
                    "state": "MD",
                    "country": "Colombia",
                    "post_code": "11111"
                }
            }]

        self.simulate_request('/contacts', method='POST', body=json.dumps(post), headers={'Content-Type': 'application/json'})

        response = self.simulate_request('/addresses', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response)

    def test_post(self):
        response = self.simulate_request('/contacts/1', method='POST')
        self.assertMethodNotAllowed(response)

    def test_delete(self):
        response = self.simulate_request('/contacts', method='DELETE')
        self.assertMethodNotAllowed(response)

    def test_put(self):
        response = self.simulate_request('/contacts', method='PUT')
        self.assertMethodNotAllowed(response)

    def test_patch(self):
        response = self.simulate_request('/contacts', method='PATCH')
        self.assertMethodNotAllowed(response)

    def test_custom_method(self):
        response = self.simulate_request('/contacts', method='CUSTOM')
        self.assertBadRequest(response, 'Bad request', 'Invalid HTTP method')

    def test_cascade_delete(self):
        response = self.simulate_request('/addresses', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response)
        self.assertEqual(response[0], b'[]')

        post = {
            "first_name": "Adam",
            "last_name": "Smith",
            "email": "asmith@macalester.edu",
            "address": {
                "street_address": "1600 Grand Avenue",
                "unit_number": "Macalester College",
                "city": "St. Paul",
                "state": "MN",
                "post_code": "55105"
            }
        }

        self.simulate_request('/contacts', method='POST', body=json.dumps(post), headers={'Content-Type': 'application/json'})

        response = self.simulate_request('/addresses', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response)
        self.assertEqual(len(json.loads(response[0].decode('utf-8'))), 1)

        response = self.simulate_request('/contacts/1', method='DELETE')
        self.assertOK(response)

        response = self.simulate_request('/addresses', method='GET', headers={'Accept': 'application/json'})
        self.assertOK(response)
        print(response)
        self.assertEqual(response[0], b'[]')


if __name__ == '__main__':
    test_classes_to_run = [TestSingleContactRoute, TestContactCollectionRoute, TestContactsPost]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    unittest.TextTestRunner().run(big_suite)
