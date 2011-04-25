#!/usr/bin/env python
"""
Client for metadata server.
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
import json, zlib, urllib2
from urllib import urlencode
import time
from binascii import a2b_hex
import logging

from .util import digest_to_block_id, block_id_to_digest, BLOCK_SIZE, to_base64
from .exceptions import *

logger = logging.getLogger("metadataclient")

class MetadataClient(object):
    def __init__(self, server, host_id, root_ns):
        self.server = server
        self.host_id = host_id
        self.root_ns = root_ns

    def inject_file(self, path, blocks, size, mtime=None):
        """
        Inject a new file into account.
        """
        blocklist = ",".join([digest_to_block_id(a2b_hex(id)) for id in blocks])

        if (size < ((len(blocks)-1)*BLOCK_SIZE+1) or
            size > len(blocks)*BLOCK_SIZE):
            raise ValueError("Invalid file size provided")
            
        if mtime is None:
            mtime = time.time()

        metadata = {
        u'parent_blocklist': None, 
        u'blocklist': blocklist,
        u'ns_id': self.root_ns, 
        u'parent_attrs': None, 
        u'mtime': int(mtime), 
        u'path': path, 
        u'is_dir': False, 
        u'size': size,
        u'target_ns': None, 
        u'attrs': {u'mac': None} # basic attrs
        }

        commit_info = [metadata]
        logger.debug("commit_info %s", commit_info)

        url = "https://"+self.server+"/commit_batch"
        request = [
        ('host_id',self.host_id),
        ('extended_ret','True'),
        ('autoclose',''),
        ('changeset_map',''),
        ('commit_info',to_base64(zlib.compress(json.dumps(commit_info))))
        ]
        logger.debug("commit_batch %s", request)        
        try:
            rv = urllib2.urlopen(url, urlencode(request))
        except urllib2.HTTPError,e:
            raise APIError("Error during commit_batch", e)

        data = rv.read()
        logger.debug("commit_batch returned %s", data)

        data = json.loads(data)
        
        time.sleep(data["chillout"])

        cur_revision = data["results"][0]
        need_blocks = data["need_blocks"]

        if len(need_blocks) > 0:
            raise UnknownBlocksError("Oops, blocks are not known: %s", need_blocks)

        logger.debug("Current revision %i", cur_revision)

        changeset_ids = data["changeset_id"].items()
        logger.debug("Changeset IDs %s", changeset_ids)

        url = "https://"+self.server+"/close_changeset"
        request = [
        ('host_id',self.host_id),
        ('changeset_id',str(changeset_ids[0][1])),
        ('ns_id',str(changeset_ids[0][0]))
        ]
        logger.debug("close_changeset %s", request)        
        try:
            rv = urllib2.urlopen(url, urlencode(request))
        except urllib2.HTTPError,e:
            raise APIError("Error during close_changeset", e)

        data = rv.read()
        logger.debug("close_changeset returned %s", data)

