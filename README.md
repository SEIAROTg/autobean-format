# autobean-format
[![build](https://github.com/SEIAROTg/autobean-format/actions/workflows/build.yml/badge.svg)](https://github.com/SEIAROTg/autobean-format/actions/workflows/build.yml)
[![pypi](https://img.shields.io/pypi/v/autobean-format)](https://pypi.org/project/autobean-format/)
[![Test Coverage](https://api.codeclimate.com/v1/badges/0c09f58b4d6735d7d991/test_coverage)](https://codeclimate.com/github/SEIAROTg/autobean-format/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/0c09f58b4d6735d7d991/maintainability)](https://codeclimate.com/github/SEIAROTg/autobean-format/maintainability)
[![license](https://img.shields.io/github/license/SEIAROTg/autobean-format.svg)](https://github.com/SEIAROTg/autobean-format)

Yet another formatter for beancount.

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
