import unittest
from unittest.mock import patch, mock_open
import json
import pandas as pd
from datacleaner import DataCleaner  

dc = DataCleaner()

def test_data_cleaning(self, mock_json_load, mock_to_csv, mock_open):
    """Test the data_cleaning method."""
    mock_json_load.return_value = json.loads(mock_open().read_data)

    self.cleaner.data_cleaning()

    mock_to_csv.assert_called_once_with('final_data_for_DB.csv', index=False)
        
    if __name__ == '__main__':
        unittest.main()