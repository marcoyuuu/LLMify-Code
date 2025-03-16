# Overview

**LLMify-Code** is a lightweight Python tool designed to transform your local codebase into a single, well-structured text file. This output is optimized for ingestion by large language models such as ChatGPT. The tool extracts the entire directory tree and file contents—handling encoding issues gracefully—and can optionally count tokens using [tiktoken](https://github.com/openai/tiktoken).

## Key Features

- **Enhanced CLI Experience:**  
  Built with [Typer](https://typer.tiangolo.com/) for an intuitive command-line interface.

- **Rich Terminal Output:**  
  Uses [Rich](https://rich.readthedocs.io/) for attractive, informative logging.

- **Configurable Ignore Rules:**  
  Loads ignore rules from a YAML configuration file (`llmify_config.yaml`) found in the target directory or, if absent, from the project root.

- **Flexible Output Formats:**  
  Supports both plain text and JSON output (including metadata like token counts).

- **Tokenization Support:**  
  Optionally counts tokens to help manage prompt limits when working with LLMs.

This project was born out of a personal necessity for a tool similar to Gitingest—but tailored for private repositories and local usage.
