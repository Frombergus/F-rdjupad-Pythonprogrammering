import unittest
from unittest.mock import patch, Mock
from webscraper import WebScraper

ws =WebScraper()

@patch('web_scraper.requests.Session.get')
def test_connect_and_fetching_data_success(self, mock_get):
    # Mocking a successful response for the initial request
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b'{"numberOfItems": 100, "itemListElement": []}'  # Mock response content
    mock_get.return_value = mock_response

    scraper = WebScraper()
    scraper.add_input()  # Set up the input
    input_data = scraper.add_start_data()

    self.assertEqual(scraper.input[2], 100)  # Number of objects
    self.assertEqual(scraper.input[3], 2)    # Iterations (100/50)
    
    if __name__ == '__main__':
        unittest.main()