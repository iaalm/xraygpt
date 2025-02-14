# 🔬📖 X-ray GPT
[![PyPI version](https://badge.fury.io/py/xraygpt.svg)](https://badge.fury.io/py/xraygpt) [![Release Building](https://github.com/iaalm/xraygpt/actions/workflows/release.yml/badge.svg)](https://github.com/iaalm/xraygpt/actions/workflows/release.yml) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) 

Generate kindle-like X-ray for e-books with LLM

## 🚀 Usage
```shell
pip install xraygpt
python -m xraygpt [epub_file]
```


#### 🤖 LLM Support
Current this tool only support OpenAI (or compatible API like DeepSeek, Kimi, etc.) and Azure OpenAI by setting environment variables.

You can config following environment variables to use different LLM service:
- `OPENAI_API_BASE`: OpenAI API or other compatible API base URL
- `OPENAI_API_KEY`: OpenAI API key
- `OPENAI_API_VERSION`: OpenAI API version
- `AZURE_OPENAI_ENDPOINT`: Use Azure OpenAI endpoint instead of standard OpenAI

Model name can be set by command line argument `--chat_model` and `--embedding_model`.

#### 📚 E-book Support
Currently only support `.epub` format. Output format is a .json file as [WordDumb](https://github.com/xxyzz/WordDumb) style. You can import this file manualy via Calibre. First select the book and click "Open book Folder". Then create/replace `worddumb-custom-x-ray.json` with the generated json file.

Generating X-Ray DB file is in progress.

## 🧑‍💻 Dev Setup
```shell
pip install -e '.[dev]'
```

#### 🎩 Static analysis
```shell
make format
```
