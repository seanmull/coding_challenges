# coding_challenges

## wc

### Requirements

- output number of bytes in a file (-c)
- output number of lines in a file  (-l)
- output the number of words in a file (-w)
- output the number of characters in a file (-m)
- provide a defualt option with no flags that outputs all of the above
- able to read from stdin if no filename is specified

## json parser

### Requirements

- build a lexer and parser
- test it against {"key": "value"}
- test it against:
```json
{
  "key1": true,
  "key2": false,
  "key3": null,
  "key4": "value",
  "key5": 101
}
```
- test it against:
```json
{
  "key": "value",
  "key-n": 101,
  "key-o": {},
  "key-l": []
}
```
- create some useful error messages

