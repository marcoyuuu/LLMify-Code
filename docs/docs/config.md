# Configuration Guide

**LLMify-Code** uses a YAML configuration file to determine which directories and files to ignore during extraction. This configuration file is named `llmify_config.yaml`.

## How It Works

When you run **LLMify-Code**:
- The tool first looks for a `llmify_config.yaml` file in the **target directory**.
- If it doesn't find one there, it falls back to the `llmify_config.yaml` in the **project root**.

## Example Configuration (`llmify_config.yaml`)

```yaml
# llmify_config.yaml
# Customize the ignore rules for LLMify-Code.

ignored_dirs:
  - .github
  - .pytest_cache
  - .pytest_cache/v
  - .pytest_cache/v/cache
  - .venv
  - venv
  - __pycache__

ignored_files:
  - .pylintrc
  - .gitignore
  - codebase.txt
  - codebase.json
  - "*.pyc"
  - "*.pyd"
  - "*.so"
  - "llm_code_prep.py"  # Optionally ignore the extraction script itself
```

## Customization

- **`ignored_dirs`**: List directories that should be skipped (e.g., `node_modules`, log directories, virtual environments).
- **`ignored_files`**: List individual files or file patterns (e.g., `.pyc` files, configuration files) that should be excluded.

You can adjust these lists based on the needs of your project.