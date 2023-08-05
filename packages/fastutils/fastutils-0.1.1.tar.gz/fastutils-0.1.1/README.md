# fastutils

Collection of simple utils.

## Install

```
pip install fastutils
```

## Installed Utils

- aesutils
- dictutils
- hashutils
- listutils
- strutils

## Usage Example

```
from fastutils import strutils
assert strutils.split("a,b.c", [",", "."]) == ["a", "b", "c"]
```



## Release Notice

### v0.1.1 2019.08.27

- Add strutils.wholestrip function, use to remove all white spaces in text.
- Fix strutils.is_urlsafeb64_decodable, strutils.is_base64_decodable and strutils.is_unhexlifiable functions, that have problem to test text contains whitespaces.

### v0.1.0 2019.08.23

- Add simple utils about operations of aes, dict, hash, list and str.
