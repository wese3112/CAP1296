import unittest
import cap1296


class TestCAP1296Driver(unittest.TestCase):
    
    test_data = (
            ([], b'\x00'),
            ([0], b'\x01'),
            ([4], b'\x10'),
            ([1, 2], b'\x06'),
            ([2, 5], b'\x24'),
            ([0, 1, 2, 3, 4, 5], b'\x3f'),
        )

    def test_keys_to_byte(self):
        for keys, output in self.test_data:
            self.assertEqual(cap1296._keys_to_byte(keys), output)
        
        # test the default keyword argument: giving an empty list should return
        # the default value
        for default in [bytes([ii]) for ii in (13, 52, 1, 32)]:
            self.assertEqual(cap1296._keys_to_byte([], default=default), default)
    
    def test_byte_to_keys(self):
        for output, keys_byte in self.test_data:
            self.assertEqual(cap1296._byte_to_keys(keys_byte), output)

        # test the num_keys keyword argument: hightest key num should be
        # num_keys - 1 (counting from 0)
        for num_keys in [5, 4, 3]:
            expected = list(range(num_keys))
            self.assertEqual(cap1296._byte_to_keys(b'\xff', num_keys=num_keys), expected)

if __name__ == '__main__':
    unittest.main()
