# Troubleshooting Guide

This document outlines common issues you might encounter while using **LLMify-Code** and provides solutions.

## Common Issues

### 1. ModuleNotFoundError for `extractor`
- **Problem:**  
  When running the tool, Python cannot locate the `extractor` module.
- **Solution:**  
  Ensure you set the `PYTHONPATH` to the `src/` directory before running the command:
  ```powershell
  $env:PYTHONPATH = "$PWD\src"
  ```

### 2. Configuration File Not Found
- **Problem:**  
  The script logs a warning that no configuration file was found.
- **Solution:**  
  - Check if a `llmify_config.yaml` exists in the target directory.
  - If not, the script falls back to the project root's `llmify_config.yaml`.
  - You can also explicitly pass a config file using the `--config` option:
    ```bash
    python -m extractor.llm_code_prep --directory /path/to/target --output codebase.txt --config /path/to/llmify_config.yaml
    ```

### 3. UnicodeDecodeError when Reading Files
- **Problem:**  
  The script fails due to encoding errors.
- **Solution:**  
  Files are opened with `errors="replace"` to handle undecodable characters. If you encounter issues, verify the file encoding.

### 4. Tokenization Errors
- **Problem:**  
  Errors during tokenization may occur if tiktoken is not installed or configured.
- **Solution:**  
  Ensure tiktoken is installed:
  ```bash
  pip install tiktoken
  ```
  If tokenization is disabled, the tool will log a message and skip token counting.

## Additional Help

If you encounter any other issues, please open an issue on GitHub with a detailed description of the problem and steps to reproduce it.