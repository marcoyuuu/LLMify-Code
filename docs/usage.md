# Usage Guide

## Setting Up

Before running **LLMify-Code**, ensure that Python can locate the `extractor` module by setting the `PYTHONPATH` to the `src/` directory.

### On Windows (PowerShell)
```powershell
$env:PYTHONPATH = "$PWD\src"
```

### On Mac/Linux (Bash)
```bash
export PYTHONPATH="$(pwd)/src"
```

## Running LLMify-Code

From the project root, run the following commands based on your needs:

### 1. Plain Text Extraction (with Tokenization)
```bash
python -m extractor.llm_code_prep --directory . --output codebase.txt --tokenize
```
**Sample Output:**
```
[21:42:30] Target directory: %s LLMify-Code
Configuration loaded from %s. llmify_config.yaml
Proceed with code extraction? [y/N]: y
[21:42:32] ✅ Code extracted successfully into %s codebase.txt
[21:42:33] Total token count: %s 6061
```

### 2. JSON Extraction
```bash
python -m extractor.llm_code_prep --directory . --output codebase.json --output-format json
```
**Sample Output:**
```
[21:44:57] Target directory: %s LLMify-Code
Configuration loaded from %s. llmify_config.yaml
Proceed with code extraction? [y/N]: y
[21:44:59] ✅ JSON output generated successfully into %s codebase.json
```

### 3. Plain Text Extraction (Without Tokenization)
```bash
python -m extractor.llm_code_prep --directory . --output codebase.txt
```
**Sample Output:**
```
[21:48:09] Target directory: %s LLMify-Code
Configuration loaded from %s. llmify_config.yaml
Proceed with code extraction? [y/N]: y
[21:48:11] ✅ Code extracted successfully into %s codebase.txt
```

### Using a Custom Configuration File

If your target project does not include its own `llmify_config.yaml`, you can specify an external configuration file:

```bash
python -m extractor.llm_code_prep --directory "/path/to/target_project" --output codebase.txt --config "/path/to/LLMify-Code/llmify_config.yaml"
```
This ensures consistent ignore rules across different projects.
