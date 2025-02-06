# 🔬📖 X-ray GPT
[![PyPI version](https://badge.fury.io/py/xraygpt.svg)](https://badge.fury.io/py/xraygpt) [![Release Building](https://github.com/iaalm/xraygpt/actions/workflows/release.yml/badge.svg)](https://github.com/iaalm/xraygpt/actions/workflows/release.yml) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) 

Generate kindle-like x-ray for e-books with LLM

## 🚀 Usage

```shell
pip install xraygpt
python -m xraygpt [epub_file]
```

## 🤖 LLM Support

Current this tool only support OpenAI and Azure OpenAI by setting environment variables.

## 🧑‍💻 Dev Setup
```shell
pip install -e '.[dev]'
```

### 🎩 Static analysis
```shell
make format
```
