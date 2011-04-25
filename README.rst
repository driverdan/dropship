dropship - Dropbox API utilities
============================================================

These utilities make use of the deduplication scheme of Dropbox__
to allow for "teleporting" files into your Dropbox account
given only a list of hashes, provided of course that the files already exist
on their servers. This enables arbitrary, anonymous transfers of files between 
Dropbox accounts.

__ http://www.dropbox.com

This package includes:

* ``dropship``: Inject a file into your account using a JSON 
  description.
* ``hash_blocks``: Produce a description from a file that can
  be used with ``dropship``.

How does it work?
------------------
Dropbox its deduplication scheme works by breaking files into blocks. 
Each of these blocks is hashed with the SHA256__
algorithm and represented by the digest. Only blocks that are not yet
known are uploaded to the server when syncing.

By using the same API as the native client, Dropship pretends to sync a
file to the dropbox folder without actually having the contents. This bluff
succeeds because the only proof needed server-side is the hash of each 4MB block
of the file, which is known. The server then adds the file metadata to the folder,
which is, as usual, propagated to all clients. These will then start downloading
the file.

__ http://en.wikipedia.org/wiki/SHA-2#SHA-256_.28a_SHA-2_variant.29_pseudocode

Configuration
------------------------
To be able to access the Dropbox server, the utilities need your credentials. These
can be provided in the following way:

- Copy ``config.py.example`` to ``config.py``.

::

    $ cp config.py.example config.py
    $ chmod 600 config.py

- Extract host_id and root_ns from your Dropbox configuration. In the current version of Dropbox
  this can be done with:

::

    $ ./sqlite_dump ~/.dropbox/config.db
    ...
    INSERT INTO "config" VALUES('host_id','00000000000000000000000000000000');
    INSERT INTO "config" VALUES('root_ns',12345);
    ...

``sqlite_dump`` is provided with this package for convenience.

- Edit ``config.py``, fill in host_id and root_ns as follows.

::

    host_id='00000000000000000000000000000000'
    root_ns=12345

Usage
-----------------

A quick example of using ``dropship``. It is very simple, type:

::

    $ ./dropship examples/sintel_trailer-1080p.mp4.json
    File /sintel_trailer-1080p.mp4 dropshipped succesfully.

After this, the file ``sintel_trailer-1080p.mp4`` (a trailer for the open source movie Sintel__ 
by the Blender Foundation) will magically  appear in your Dropbox folder. It will be synced to all devices attached to it.

If it fails with an error message, make sure that there is enough room on your quota to receive the file.

__ http://www.sintel.org/download/

You can hash your own files to ``.json`` format with the ``hash_blocks`` utility:

::

    $ ./hash_blocks ~/downloads/ext-4.0-beta3.zip
    {"blocks": ["4f52526814cb28ecb2683c8f365f88cccaa1c213d6f36875ff98fcf980c21daa", ...

::

    $ ./hash_blocks ~/downloads/ext-4.0-beta3.zip > ~/downloads/ext-4.0-beta3.zip.json

The resulting ``.json`` file can be shared as you wish. It contains only data from the file, 
and is not bound to your account in any way.

``.json`` file format
----------------------

``.json`` files, as their name implies, are in JSON__ format. The top-level object contains the following fields:

__ http://www.json.org/

*blocks*
    List of SHA256 hashes. Each hash is a 64 character hexadecimal string.

*size*
    Size of the file, in bytes.

*name*
    Name of the file.

*mtime*
    Last modification time of the file as UNIX timestamp. If not provided
    it defaults to the current time.

Disclaimer
-----------
Currently this is only a proof of concept, satisfying my own curiosity as 
to how Dropbox works. However, this probably has some interesting
applications as well. Feel free to fork this project if you want to
add a fancy interface or user-friendlyness.

License
---------
Copyright (C) 2011 by Wladimir van der Laan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Authors
---------

- Wladimir van der Laan laanwj@gmail.com

Kudos
-------

- Krzysztof Dziądziak mentioned the theoretical possibility of this on `his blog`__.

__ http://forwardfeed.pl/index.php/2011/03/23/theoretical-vulnerability-of-dropbox-platform-to-quick-exchange-files/
