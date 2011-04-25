"""
Block ID conversion utilities.
"""
# Copyright (C) 2011 by Wladimir van der Laan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from binascii import a2b_base64, b2a_base64
import string

BLOCK_SIZE=4*1024*1024
HASH_SIZE=43

DIGEST_TO_BLOCK_ID=string.maketrans("=+/", "~-_")
BLOCK_ID_TO_DIGEST=string.maketrans("~-_", "=+/")

def digest_to_block_id(digest):
    block_id = b2a_base64(digest)[0:HASH_SIZE]
    block_id = block_id.translate(DIGEST_TO_BLOCK_ID)
    return block_id
    
def block_id_to_digest(block_id):
    block_id = block_id.translate(BLOCK_ID_TO_DIGEST)
    return a2b_base64(block_id + "=")

def to_base64(binary):
    base64 = b2a_base64(binary)
    base64 = base64.translate(DIGEST_TO_BLOCK_ID, "\n")
    return base64
    
def from_base64(base64):
    base64 = base64.translate(BLOCK_ID_TO_DIGEST)
    return a2b_base64(base64)
