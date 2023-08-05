import re

import six

_hexdig = '0123456789ABCDEFabcdef'
_asciire = re.compile('([\x00-\x7f]+)')


if six.PY2:

    _hextochr = dict((a + b, chr(int(a + b, 16)))
                     for a in _hexdig for b in _hexdig)

    def _unquote(s, ignore=''):
        """unquote('abc%20def') -> 'abc def'."""
        if isinstance(s, unicode):
            if '%' not in s:
                return s
            bits = _asciire.split(s)
            res = [bits[0]]
            append = res.append
            for i in range(1, len(bits), 2):
                append(_unquote(str(bits[i]), ignore).decode('utf-8'))
                append(bits[i + 1])
            return ''.join(res)

        bits = s.split('%')
        # fastpath
        if len(bits) == 1:
            return s
        res = [bits[0]]
        append = res.append
        ignore = {b'%02x' % ord(c) for c in ignore}
        for item in bits[1:]:
            code = item[:2].lower()
            if code in _hextochr and code not in ignore:
                append(_hextochr[item[:2]])
                append(item[2:])
            else:
                append(b'%')
                append(item)
        return ''.join(res)

elif six.PY3:

    _hextobyte = None

    def _unquote_to_bytes(string, ignore=''):
        """unquote_to_bytes('abc%20def') -> b'abc def'."""
        # Note: strings are encoded as UTF-8. This is only an issue if it contains
        # unescaped non-ASCII characters, which URIs should not.
        if not string:
            # Is it a string-like object?
            string.split
            return b''
        if isinstance(string, str):
            string = string.encode('utf-8')
        bits = string.split(b'%')
        if len(bits) == 1:
            return string
        res = [bits[0]]
        append = res.append
        # Delay the initialization of the table to not waste memory
        # if the function is never called
        global _hextobyte
        if _hextobyte is None:
            _hextobyte = {(a + b).encode(): bytes.fromhex(a + b)
                          for a in _hexdig for b in _hexdig}
        ignore = {b'%02x' % ord(c) for c in ignore}
        print(ignore)
        for item in bits[1:]:
            code = item[:2].lower()
            if code in _hextobyte and code not in ignore:
                append(_hextobyte[item[:2]])
                append(item[2:])
            else:
                append(b'%')
                append(item)
        return b''.join(res)

    def _unquote(string, encoding='utf-8', errors='replace', ignore=''):
        """Replace %xx escapes by their single-character equivalent. The optional
        encoding and errors parameters specify how to decode percent-encoded
        sequences into Unicode characters, as accepted by the bytes.decode()
        method.
        By default, percent-encoded sequences are decoded with UTF-8, and invalid
        sequences are replaced by a placeholder character.
        unquote('abc%20def') -> 'abc def'.
        """
        if '%' not in string:
            string.split
            return string
        if encoding is None:
            encoding = 'utf-8'
        if errors is None:
            errors = 'replace'
        bits = _asciire.split(string)
        res = [bits[0]]
        append = res.append
        for i in range(1, len(bits), 2):
            append(_unquote_to_bytes(bits[i], ignore).decode(encoding, errors))
            append(bits[i + 1])
        return ''.join(res)
