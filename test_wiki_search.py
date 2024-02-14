import unittest
import controllers.wiki_search_controller as wiki_search_controller
from flask import request, jsonify
from controllers.wiki_search_controller import search_history

class WikiSearchTest(unittest.TestCase):

    def setUp(self):
        self.app = wiki_search_controller.app.test_client()

    def test_word_frequency_analysis_endpoint(self):
        # Test with a valid topic
        response = self.app.get('/wiki_search?topic=Pytorch&n=5')
        data = response.get_json()

        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
            self.assertIn('topic', data)
            self.assertIn('top_words', data)
        elif response.status_code == 400 and 'error' in data and data['error'] == 'DisambiguationError':
            # Handle DisambiguationError case
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data)
            self.assertIn('options', data)
        else:
            self.fail(f"Unexpected response: {response.status_code}, {data}")

        # Test with missing topic parameter
        response = self.app.get('/wiki_search?n=5')
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'You have not entered any topic, please provide a topic.')

        # Test with invalid topic (no Wikipedia article found)
        response = self.app.get('/wiki_search?topic=InvalidTopic&n=5')
        data = response.get_json()

        if response.status_code == 404:
            self.assertEqual(response.status_code, 404)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'No Wikipedia article found for the given topic')
        elif response.status_code == 400 and 'error' in data and data['error'] == 'DisambiguationError':
            # Handle DisambiguationError case
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data)
            self.assertIn('options', data)
        else:
            self.fail(f"Unexpected response: {response.status_code}, {data}")

    def test_search_history_endpoint(self):
        # Add a search result to the history
        search_result = {'topic': 'Pytorch', 'top_words': [{'word': 'code', 'frequency': 10}]}
        search_history.append(search_result)

        # Test the search history endpoint
        response = self.app.get('/search_history')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertDictEqual(data[0], search_result)

if __name__ == '__main__':
    unittest.main()
