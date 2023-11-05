import unittest
import requests


class Tests(unittest.TestCase):
    def test_bitcoin_block_height(self):
        block_hash = "0000000000000000000505ab2c8ce35d3dc09e161141d86bb618f616d1326c6b"
        block_height_message = f"https://blockstream.info/api/block/{block_hash}"
        response = requests.get(block_height_message)
        block_height = response.json()['height']
        self.assertEqual(block_height, 787763)


if __name__ == '__main__':
    unittest.main()
