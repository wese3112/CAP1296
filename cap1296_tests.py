import unittest
import cap1296


class TestCAP1296Driver(unittest.TestCase):

    def test_keys_to_byte(self):
        input_result = (
            ([], b'\x00'),
            ([0], b'\x01'),
            ([4], b'\x10'),
            ([1, 2], b'\x06'),
            ([2, 5], b'\x24'),
            ([0, 1, 2, 3, 4, 5], b'\x3f'),
        )

        for keys, output in input_result:
            self.assertEqual(cap1296._keys_to_byte(keys), output)
        
        for default in [bytes([ii]) for ii in (13, 52, 1, 32)]:
            self.assertEqual(cap1296._keys_to_byte([], default=default), default)


if __name__ == '__main__':
    unittest.main()
