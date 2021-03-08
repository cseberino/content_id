#!/usr/bin/env python3

import sys
sys.path.append("..")

import content_id
import unittest
import warnings

DPB_B_SIZE = 2 ** 18

class Tester(unittest.TestCase):
        def setUp(self):
                warnings.simplefilter("ignore", ResourceWarning)
                warnings.simplefilter("ignore", DeprecationWarning)

        def test_ipfs_obj(self):
                output = content_id.ipfs_obj(b"Hello World\n")
                answer = b"\n\x12\x08\x02\x12\x0cHello World\n\x18\x0c"
                self.assertEqual(output, answer)

                bytes_ = DPB_B_SIZE * b"A" + 3 * b"B"
                output = content_id.ipfs_obj(bytes_)
                answer = (b"\x12*\n\"\x12 d\x07\x1c^\xdd]\xe9D\x03/\xf4\xb5\xfd"
                          b"@[Zz\x16-8g\x8c\x0b\xdf\xf2\xd5b\x00\x03\x94\xf5"
                          b"\xd5\x12\x00\x18\x8e\x80\x10\x12(\n\"\x12 \xb8\xe8y"
                          b"\xb1\xaf\x06B\'C\x8e\xd20-\xac8C\xfe0$%\xd7\xf9\x10"
                          b"6\xcep\xd9sG8\x1c\x9e\x12\x00\x18\x0b\n\x0c\x08\x02"
                          b"\x18\x83\x80\x10 \x80\x80\x10 \x03")
                self.assertEqual(output, answer)

                bytes_ = 100 * DPB_B_SIZE * b"A"
                output = content_id.ipfs_obj(bytes_)
                answer = open("big_ipfs_obj", "rb").read()
                self.assertEqual(output, answer)

        def test_content_id(self):
                output = content_id.content_id(b"Hello World\n")
                answer = "bafybeiduiecxoeiqs3gyc6r7v3lymmhserldnpw62qjnhmqsulqjxjmtzi"
                self.assertEqual(output, answer)

                bytes_ = 100 * DPB_B_SIZE * b"A"
                output = content_id.content_id(bytes_)
                answer = "bafybeibgrqvgcjz4eysvvlieulgv4hyw5f65wjoc7rqro66o4ridebhqmq"

                self.assertEqual(output, answer)

unittest.main()
