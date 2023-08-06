# Amharic Number to Word

[![CircleCI](https://circleci.com/gh/mitiku1/AmharicNumber2Word.svg?style=svg)](https://circleci.com/gh/mitiku1/AmharicNumber2Word)  
[![PyPI version](https://badge.fury.io/py/am-num2word.svg)](https://badge.fury.io/py/am-num2word)
[![PyPI version](https://img.shields.io/pypi/dm/am-num2word.svg)](https://img.shields.io/pypi/dm/am-num2word.svg)
[![image](https://secure.travis-ci.org/mitiku1/AmharicNumber2Word.png)](http://travis-ci.org/mitiku1/AmharicNumber2Word)
[![Waffle.io - Columns and their card count](https://badge.waffle.io/mitiku1/AmharicNumber2Word.svg?columns=all)](https://waffle.io/mitiku1/AmharicNumber2Word)
[![Coverage Status](https://coveralls.io/repos/github/mitiku1/AmharicNumber2Word/badge.svg?branch=master)](https://coveralls.io/github/mitiku1/AmharicNumber2Word?branch=master)

<p>
Converters Numbers from decimal representation to Amharic language word representation. The package supports numbers up-to 999,999,999,999,999. These are the numbers that could often comeup in real world. 
</p>

### Usage
This package provides one class(`am_num2word.Number2WordsConverter`) to handle number to words conversion.
```python
import am_num2word

number = 45232945075
converter = am_num2word.Number2WordsConverter()
words, coma_separated = converter.convert(number)
print(words) # አርባ አምስት ቢሊዮን ሁለት መቶ ሰላሳ ሁለት ሚሊዮን ዘጠኝ መቶ አርባ አምስት ሺህ ሰባ አምስት
print(coma_separated) # 45,232,945,075'
```

### How to install
```console
pip install am-num2word
```

### Lincense

MIT License

Copyright (c) 2019 Mitiku Yohannes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
