from hashlib import md5
import math
import os
import pathlib
import re
from urllib.parse import urlsplit


DEFAULT_BLOCK_SIZE = 5 * 2 ** 20


def infer_storage_options(urlpath, inherit_storage_options=None):
    """ Infer storage options from URL path and merge it with existing storage
    options.

    Parameters
    ----------
    urlpath: str or unicode
        Either local absolute file path or URL (hdfs://namenode:8020/file.csv)
    inherit_storage_options: dict (optional)
        Its contents will get merged with the inferred information from the
        given path

    Returns
    -------
    Storage options dict.

    Examples
    --------
    >>> infer_storage_options('/mnt/datasets/test.csv')  # doctest: +SKIP
    {"protocol": "file", "path", "/mnt/datasets/test.csv"}
    >>> infer_storage_options(
    ...          'hdfs://username:pwd@node:123/mnt/datasets/test.csv?q=1',
    ...          inherit_storage_options={'extra': 'value'})  # doctest: +SKIP
    {"protocol": "hdfs", "username": "username", "password": "pwd",
    "host": "node", "port": 123, "path": "/mnt/datasets/test.csv",
    "url_query": "q=1", "extra": "value"}
    """
    # Handle Windows paths including disk name in this special case
    if re.match(r'^[a-zA-Z]:[\\/]', urlpath):
        return {'protocol': 'file',
                'path': urlpath}

    parsed_path = urlsplit(urlpath)
    protocol = parsed_path.scheme or 'file'
    if parsed_path.fragment:
        path = "#".join([parsed_path.path, parsed_path.fragment])
    else:
        path = parsed_path.path
    if protocol == 'file':
        # Special case parsing file protocol URL on Windows according to:
        # https://msdn.microsoft.com/en-us/library/jj710207.aspx
        windows_path = re.match(r'^/([a-zA-Z])[:|]([\\/].*)$', path)
        if windows_path:
            path = '%s:%s' % windows_path.groups()

    if protocol in ["http", "https"]:
        # for HTTP, we don't want to parse, as requests will anyway
        return {"protocol": protocol, "path": urlpath}

    options = {
        'protocol': protocol,
        'path': path,
    }

    if parsed_path.netloc:
        # Parse `hostname` from netloc manually because `parsed_path.hostname`
        # lowercases the hostname which is not always desirable (e.g. in S3):
        # https://github.com/dask/dask/issues/1417
        options['host'] = parsed_path.netloc.rsplit('@', 1)[-1].rsplit(':', 1)[0]

        if protocol in ("s3", "gcs", "gs"):
            options["path"] = options['host'] + options["path"]
        else:
            options["host"] = options['host']
        if parsed_path.port:
            options['port'] = parsed_path.port
        if parsed_path.username:
            options['username'] = parsed_path.username
        if parsed_path.password:
            options['password'] = parsed_path.password

    if parsed_path.query:
        options['url_query'] = parsed_path.query
    if parsed_path.fragment:
        options['url_fragment'] = parsed_path.fragment

    if inherit_storage_options:
        update_storage_options(options, inherit_storage_options)

    return options


def update_storage_options(options, inherited=None):
    if not inherited:
        inherited = {}
    collisions = set(options) & set(inherited)
    if collisions:
        collisions = '\n'.join('- %r' % k for k in collisions)
        raise KeyError("Collision between inferred and specified storage "
                       "options:\n%s" % collisions)
    options.update(inherited)


compressions = {'gz': 'gzip', 'bz2': 'bz2', 'xz': 'xz', 'zip': 'zip'}


def infer_compression(filename):
    extension = os.path.splitext(filename)[-1].strip('.')
    if extension in compressions:
        return compressions[extension]


def build_name_function(max_int):
    """ Returns a function that receives a single integer
    and returns it as a string padded by enough zero characters
    to align with maximum possible integer

    >>> name_f = build_name_function(57)

    >>> name_f(7)
    '07'
    >>> name_f(31)
    '31'
    >>> build_name_function(1000)(42)
    '0042'
    >>> build_name_function(999)(42)
    '042'
    >>> build_name_function(0)(0)
    '0'
    """
    # handle corner cases max_int is 0 or exact power of 10
    max_int += 1e-8

    pad_length = int(math.ceil(math.log10(max_int)))

    def name_function(i):
        return str(i).zfill(pad_length)

    return name_function


def seek_delimiter(file, delimiter, blocksize):
    """ Seek current file to next byte after a delimiter bytestring

    This seeks the file to the next byte following the delimiter.  It does
    not return anything.  Use ``file.tell()`` to see location afterwards.

    Parameters
    ----------
    file: a file
    delimiter: bytes
        a delimiter like ``b'\n'`` or message sentinel
    blocksize: int
        Number of bytes to read from the file at once.
    """

    if file.tell() == 0:
        return

    last = b''
    while True:
        current = file.read(blocksize)
        if not current:
            return
        full = last + current
        try:
            if delimiter in full:
                i = full.index(delimiter)
                file.seek(file.tell() - (len(full) - i) + len(delimiter))
                return
            elif len(current) < blocksize:
                # end-of-file without delimiter
                return
        except ValueError:
            pass
        last = full[-len(delimiter):]


def read_block(f, offset, length, delimiter=None):
    """ Read a block of bytes from a file

    Parameters
    ----------
    fn: string
        Path to filename
    offset: int
        Byte offset to start read
    length: int
        Number of bytes to read
    delimiter: bytes (optional)
        Ensure reading starts and stops at delimiter bytestring

    If using the ``delimiter=`` keyword argument we ensure that the read
    starts and stops at delimiter boundaries that follow the locations
    ``offset`` and ``offset + length``.  If ``offset`` is zero then we
    start at zero.  The bytestring returned WILL include the
    terminating delimiter string.

    Examples
    --------

    >>> from io import BytesIO  # doctest: +SKIP
    >>> f = BytesIO(b'Alice, 100\\nBob, 200\\nCharlie, 300')  # doctest: +SKIP
    >>> read_block(f, 0, 13)  # doctest: +SKIP
    b'Alice, 100\\nBo'

    >>> read_block(f, 0, 13, delimiter=b'\\n')  # doctest: +SKIP
    b'Alice, 100\\nBob, 200\\n'

    >>> read_block(f, 10, 10, delimiter=b'\\n')  # doctest: +SKIP
    b'Bob, 200\\nCharlie, 300'
    """
    if delimiter:
        f.seek(offset)
        seek_delimiter(f, delimiter, 2**16)
        if length is None:
            return f.read()
        start = f.tell()
        length -= start - offset

        f.seek(start + length)
        seek_delimiter(f, delimiter, 2**16)
        end = f.tell()

        offset = start
        length = end - start

    f.seek(offset)
    b = f.read(length)
    return b


def tokenize(*args, **kwargs):
    """ Deterministic token

    (modified from dask.base)

    >>> tokenize([1, 2, '3'])
    '9d71491b50023b06fc76928e6eddb952'

    >>> tokenize('Hello') == tokenize('Hello')
    True
    """
    if kwargs:
        args += (kwargs,)
    return md5(str(args).encode()).hexdigest()


def stringify_path(filepath):
    """ Attempt to convert a path-like object to a string.

    Parameters
    ----------
    filepath : object to be converted

    Returns
    -------
    filepath_str : maybe a string version of the object

    Notes
    -----
    Objects supporting the fspath protocol (Python 3.6+) are coerced
    according to its __fspath__ method.

    For backwards compatibility with older Python version, pathlib.Path
    objects are specially coerced.

    Any other object is passed through unchanged, which includes bytes,
    strings, buffers, or anything else that's not even path-like.
    """
    if hasattr(filepath, "__fspath__"):
        return filepath.__fspath__()
    elif isinstance(filepath, pathlib.Path):
        return str(filepath)
    return filepath
