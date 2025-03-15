# LLMify-Code

**LLMify-Code** is a lightweight Python tool that transforms your local codebase into a single, well-structured text file—ready to be ingested by large language models like ChatGPT. The tool extracts the entire directory tree and file contents (handling encoding issues gracefully) and optionally counts tokens using tiktoken. Output can be generated in plain text or JSON format.

## Features

- **Enhanced CLI Experience:**  
  Built with [Typer](https://typer.tiangolo.com/) for a modern, user-friendly command-line interface.

- **Rich Terminal Output:**  
  Uses [Rich](https://rich.readthedocs.io/) to display attractive, informative log messages.

- **Configurable Ignore Rules:**  
  Loads ignore rules from a YAML configuration file (`llmify_config.yaml`) in the project root. Customize which directories and files to skip without modifying the code.

- **Output Format Options:**  
  Choose between plain text output (default) and JSON output (including directory tree, file metadata, and token counts) via the `--output-format` option.

- **Tokenization Support:**  
  Optionally count tokens (using [tiktoken](https://github.com/openai/tiktoken)) to help you stay within token limits.

- **Robust File Reading:**  
  Files are read with `errors="replace"` to handle undecodable bytes gracefully.

## Repository Structure

```
LLMify-Code/
├── .github/                   # GitHub workflows and related files
├── .pytest_cache/             # Cache for pytest runs
├── .venv/                     # Virtual environment (hidden)
├── src/
│   └── extractor/
│       ├── __init__.py        # Package initializer for extractor
│       └── llm_code_prep.py   # Main extraction script
├── tests/
│   └── test_extractor.py      # Unit tests for the extraction tool
├── venv/                      # (Alternate) Virtual environment directory
├── .gitignore                 # Files/directories to be ignored by Git
├── .pre-commit-config.yaml    # Pre-commit hook configuration
├── .pylintrc                  # Pylint configuration
├── codebase.txt               # Example output file (generated)
├── CONTRIBUTING.md            # Contribution guidelines
├── llmify_config.yaml         # YAML configuration for ignore rules
├── README.md                  # This documentation file
└── requirements.txt           # Required Python packages with version numbers
```

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/LLMify-Code.git
   cd LLMify-Code
   ```

2. **(Optional) Create a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run LLMify-Code using one of the following commands (from the project root). The tool loads ignore rules from `llmify_config.yaml` in the project root and uses them to exclude specified directories and files.

#### **Before Running the Script**
Before using **LLMify-Code**, ensure that Python can locate the `extractor` module. You need to set the `PYTHONPATH` to the `src/` directory:

##### **On Windows (PowerShell):**
```powershell
$env:PYTHONPATH = "$PWD\src"
```
*(This sets `PYTHONPATH` for the current session.)*

##### **On Mac/Linux (Bash):**
```bash
export PYTHONPATH="$(pwd)/src"
```
*(If you want to persist it, add this to your `.bashrc`, `.zshrc`, or `.bash_profile`.)*

---

### **🔹 Why is This Needed?**
By default, Python does not recognize `src/extractor` as a module. Setting `PYTHONPATH` ensures that running:

```powershell
python -m extractor.llm_code_prep --directory . --output codebase.txt
```
works correctly without a **ModuleNotFoundError**.

1. **Plain Text Extraction (with Tokenization):**

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

2. **JSON Extraction:**

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

3. **Plain Text Extraction (Without Tokenization):**

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

> **Note:** The log messages shown are sample outputs. Your actual timestamps and values may vary. The directory tree and file contents are written directly into the output file, and the tool does not print the full tree to the terminal.

## Configuration

LLMify-Code loads ignore rules from `llmify_config.yaml` in the project root. Here’s an example configuration file:

```yaml
# llmify_config.yaml
# This configuration file allows you to customize ignore rules for LLMify-Code.

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
  - "llm_code_prep.py"  # Ignore the extraction script itself if desired
```

Adjust the `ignored_dirs` and `ignored_files` lists as needed.

## Testing

Unit tests are provided in the `tests/` directory. To run the tests, simply execute:

```bash
pytest
```

## Contributing

Contributions are welcome! Please follow these guidelines:

- Fork the repository and create your feature branch.
- Write tests for new features.
- Ensure your code adheres to [PEP 8](https://www.python.org/dev/peps/pep-0008/) standards.
- Open a pull request with a clear description of your changes.

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**LLMify-Code** – Making your code LLM-ready, one file at a time!

Happy Coding!
