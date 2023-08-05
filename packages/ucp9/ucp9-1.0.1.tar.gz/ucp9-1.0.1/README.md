# UCP9 - Unicode To CP932 Transcoder
A small python package which helps transcode cp932-incompatible kanji characters to their cp932-compatible equivalents

### This module provides a transcoding service:
- FROM: An arbitrary unicode character.
- TO: A cp932-compatible, semantically similar but differently encoded version of the same character.
    
### Usage:
```
    import ucp9
    ucp9.convert(string, option)
```
**[string]**: a string that contains cp932-incompatible characters

**[option]**: Option to handle cp932-inconvertible characters.
 - "keep": keep the cp932-inconvertible characters. NOTE: the return string WON'T be cp932-compatible.
 - "remove": remove the cp932-inconvertible characters.
 - "replace": (Default behaviour) replace the cp932-inconvertible characters with "?"
    
### Currently supported unicode character blocks:
- [x] Kangxi Radicals
- [x] Print Standard Character
- [x] Old type
- [x] CJK Radicals Supplement
- [x] Katakana Phonetic Extensions
- [x] CJK Unified Ideographs
- [x] CJK Compatibility Ideographs
- [x] CJK Compatibility Ideographs Supplements

### Note:
- cp932-incompatible: characters which cannot encode to cp932 using string.encode(), but could potentially have equivalent cp932-encodable versions of themselves.
- cp932-inconvertible: characters which cannot encode to cp932, and doesn't have a cp932-encodable version.