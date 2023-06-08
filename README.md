# autobean-format
[![build](https://github.com/SEIAROTg/autobean-format/actions/workflows/build.yml/badge.svg)](https://github.com/SEIAROTg/autobean-format/actions/workflows/build.yml)
[![pypi](https://img.shields.io/pypi/v/autobean-format)](https://pypi.org/project/autobean-format/)
[![Test Coverage](https://api.codeclimate.com/v1/badges/0c09f58b4d6735d7d991/test_coverage)](https://codeclimate.com/github/SEIAROTg/autobean-format/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/0c09f58b4d6735d7d991/maintainability)](https://codeclimate.com/github/SEIAROTg/autobean-format/maintainability)
[![license](https://img.shields.io/github/license/SEIAROTg/autobean-format.svg)](https://github.com/SEIAROTg/autobean-format)

Yet another formatter for beancount.

## Features

* Deep cleanup.
  * Normalizes **all** spacing.
  * Full beancount v2 syntax support (except out-of-line tags / links in `transaction`).
* Currency / cost aligning.
  * Works for `open`, `balance`, `price` and posting.
* Entry sorting.
  * Honors `pushtag` / `pushmeta`.
  * Honors `time` meta (`HH:MM` / `HH:MM:SS` / epoch seconds / epoch ms / epoch us).
  * Preserves comments.
  * Preserves existing structure and ordering whenever possible.
* Thousands separator normalization.
  * Adds / removes / keeps thousands separators.
* Recursive formatting.
  * Recursively formats included files.
  * Honors glob includes.
* Flexible output.
  * Prints results / prints diff / writes back to file.
* Typed and extensible.
  * For example, the code for thousands separators is as simple as [this](autobean_format/formatters/number.py).

## Usage

```sh
pip install autobean-format

# format and print results
autobean-format foo.bean
# format and write back to file
autobean-format foo.bean --output-mode=inplace
# format and print the diff
autobean-format foo.bean --output-mode=diff

# sort entries by date and time
autobean-format foo.bean --sort

# recursively format all included files
autobean-format foo.bean --recursive

# add thousands separators to all numbers
autobean-format foo.bean --thousands-separator=add

# see more options
autobean-format -h
```

## Examples

```sh
autobean-format foo.bean \
    --indent='    ' \
    --currency-column=30 \
    --cost-column=35 \
    --thousands-separator=add \
    --spaces-in-braces \
    --sort \
    --recursive \
    --output-mode=inplace
```

<table>
<tr>
<th align="center">Before</th>
<th align="center">After</th>
</tr>
<tr>
<td>

`foo.bean`:

```beancount
2000-01-01 open Assets:Foo USD,XXX
2000-01-01  *  "foo"   ^aa  #bb
  meta:123
     Assets:Foo  -1.23*4000USD    ;X
    Assets:Foo 1000 XXX {4.92  USD}
   meta:456


include "price.*"
2000-01-02 balance Assets:Foo -4920USD
2000-01-02 balance Assets:Foo 1000XXX

```

`price.bean`:

```beancount
2021-01-01 price EUR 1.21 USD
 ;inner comment
2021-01-04 price GBP  1.36 USD  ; Y
;leading comment
2021-01-01 price JPY  0.009 USD

2020-01-01 price EUR  1.12 USD
2020-01-02 price GBP  1.32USD
2020-01-01 price JPY  0.009 USD
```

</td>
<td>

`foo.bean`:

```beancount
2000-01-01 open Assets:Foo    USD, XXX

2000-01-01 * "foo" ^aa #bb
    meta: 123
    Assets:Foo  -1.23 * 4,000 USD ; X
    Assets:Foo          1,000 XXX  { 4.92 USD }
        meta: 456

include "price.*"

2000-01-02 balance Assets:Foo -4,920 USD
2000-01-02 balance Assets:Foo 1,000 XXX
```

`price.bean`:

```beancount
2020-01-01 price EUR     1.12 USD
2020-01-01 price JPY    0.009 USD
2020-01-02 price GBP     1.32 USD

2021-01-01 price EUR     1.21 USD
    ; inner comment
; leading comment
2021-01-01 price JPY    0.009 USD
2021-01-04 price GBP     1.36 USD ; Y
```

</td>
</tr>
</table>
