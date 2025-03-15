#!/usr/bin/env python
"""
llm_code_prep.py

A tool to extract a codebase by generating a filtered directory listing and
aggregating source code from files into a single output file. Optionally, it can
count tokens using tiktoken and output results in JSON format with metadata.

Features:
- Loads ignore rules from a YAML configuration file.
  The script first checks for a config file in the target directory.
  If not found there, it falls back to the configuration file in the project root.
- Provides output in plain text (default) or JSON format.
- Optionally counts tokens for the extracted output.

Usage Examples:
  1. Plain text extraction:
     python -m extractor.llm_code_prep --directory . --output codebase.txt
  2. JSON extraction:
     python -m extractor.llm_code_prep --directory . --output codebase.json --output-format json
  3. Extraction with token count:
     python -m extractor.llm_code_prep --directory . --output codebase.txt --tokenize
"""

import os
import json
import logging
from typing import Optional, Dict, Any, Tuple

import typer
from rich.console import Console
from ruamel.yaml import YAML, YAMLError

try:
    import tiktoken
except ImportError:
    tiktoken = None  # Tokenization will be disabled if tiktoken is not installed

app = typer.Typer()
console = Console()

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Loads a YAML configuration file for ignore rules.
    If the file is missing or cannot be parsed, returns empty ignore rules.

    Parameters:
        config_path (str): Path to the YAML configuration file.

    Returns:
        dict: Configuration dictionary containing 'ignored_dirs' and 'ignored_files'.
    """
    yaml = YAML(typ="safe")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.load(f) or {}
        console.log("[green]Configuration loaded from %s.[/green]", config_path)
        return config
    except (FileNotFoundError, PermissionError, YAMLError) as e:
        console.log(
            "[yellow]Could not load config file %s: %s. No ignore rules applied.[/yellow]",
            config_path, e
        )
        return {"ignored_dirs": [], "ignored_files": []}

def merge_ignore_rules(config: Dict[str, Any]) -> Tuple[set, set]:
    """
    Converts configuration lists for ignored directories and files into sets.

    Parameters:
        config (dict): Configuration dictionary with keys 'ignored_dirs' and 'ignored_files'.

    Returns:
        tuple: (ignored_dirs, ignored_files) as sets.
    """
    ignored_dirs = set(config.get("ignored_dirs", []))
    ignored_files = set(config.get("ignored_files", []))
    return ignored_dirs, ignored_files

def determine_config_path(abs_directory: str, config: Optional[str]) -> Optional[str]:
    """
    Determines the configuration file path to use.
    If a config is provided, returns it.
    Otherwise, checks for 'llmify_config.yaml' in the target directory.
    If not found, falls back to the 'llmify_config.yaml' in the project root.

    Parameters:
        abs_directory (str): Absolute path of the target directory.
        config (Optional[str]): User-provided config path.

    Returns:
        Optional[str]: The configuration file path or None.
    """
    if config is not None:
        return config
    target_config = os.path.join(abs_directory, "llmify_config.yaml")
    if os.path.exists(target_config):
        return target_config
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    root_config = os.path.join(project_root, "llmify_config.yaml")
    if os.path.exists(root_config):
        return root_config
    console.log(
        "[yellow]No configuration file found; no ignore rules will be applied.[/yellow]"
    )
    return None

def get_directory_tree(
    directory: str, ignored_dirs: set, ignored_files: set, indent: str = ""
) -> str:
    """
    Recursively builds a string representing the directory tree,
    filtering out ignored directories and files.

    Parameters:
        directory (str): The target directory.
        ignored_dirs (set): Set of directory names to ignore.
        ignored_files (set): Set of file names to ignore.
        indent (str): Indentation for nested items.

    Returns:
        str: The formatted directory tree.
    """
    tree_str = ""
    try:
        entries = sorted(os.scandir(directory), key=lambda e: e.name.lower())
    except OSError as e:
        logging.error("Error scanning directory %s: %s", directory, e)
        return ""

    for entry in entries:
        if entry.is_dir():
            if entry.name not in ignored_dirs:
                tree_str += f"{indent}[DIR]  {entry.name}\n"
                tree_str += get_directory_tree(
                    os.path.join(directory, entry.name),
                    ignored_dirs,
                    ignored_files,
                    indent + "    "
                )
        elif entry.is_file():
            if entry.name not in ignored_files:
                tree_str += f"{indent}[FILE] {entry.name}\n"
    return tree_str

def extract_code_text(
    directory: str, output_file: str, ignored_dirs: set, ignored_files: set
) -> None:
    """
    Extracts the directory tree and file contents into a plain text output file.

    Parameters:
        directory (str): The target directory.
        output_file (str): Output file name.
        ignored_dirs (set): Set of directories to ignore.
        ignored_files (set): Set of files to ignore.
    """
    with open(output_file, "w", encoding="utf-8") as out_file:
        out_file.write("=== Directory Listing ===\n\n")
        tree = get_directory_tree(directory, ignored_dirs, ignored_files)
        out_file.write(tree)
        out_file.write("\n=== End of Directory Listing ===\n\n")
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignored_dirs]
            for file in files:
                if file in ignored_files or file.endswith((".exe", ".dll", ".bin")):
                    continue
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                    out_file.write(f"### FILE: {file_path}\n")
                    out_file.write(content + "\n\n")
                except OSError as e:
                    logging.warning("Skipping %s: %s", file_path, e)
    console.log("[bold green]✅ Code extracted successfully into %s[/bold green]", output_file)

def extract_code_json(
    directory: str, output_file: str, ignored_dirs: set, ignored_files: set
) -> None:
    """
    Extracts the directory tree and file contents into a JSON output file with metadata.
    The JSON includes the directory tree, file metadata (including token counts if available),
    and the total token count.

    Parameters:
        directory (str): The target directory.
        output_file (str): Output file name.
        ignored_dirs (set): Set of directories to ignore.
        ignored_files (set): Set of files to ignore.
    """
    data = {}
    data["directory_tree"] = get_directory_tree(directory, ignored_dirs, ignored_files)
    data["files"] = []
    total_tokens = 0
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        for file in files:
            if file in ignored_files or file.endswith((".exe", ".dll", ".bin")):
                continue
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                file_data = {"filename": file_path, "content": content}
                token_count = count_tokens_in_text(content)
                if token_count is not None:
                    file_data["token_count"] = token_count
                    total_tokens += token_count
                data["files"].append(file_data)
            except OSError as e:
                logging.warning("Skipping %s: %s", file_path, e)
    data["total_tokens"] = total_tokens
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    console.log(
        "[bold green]✅ JSON output generated successfully into %s[/bold green]",
        output_file
    )

def count_tokens_in_text(text: str, model: str = "gpt-4") -> Optional[int]:
    """
    Counts tokens in the given text using tiktoken, if available.

    Parameters:
        text (str): The text to tokenize.
        model (str): Target model for tokenization (default: 'gpt-4').

    Returns:
        Optional[int]: The number of tokens, or None if tiktoken is not installed
                       or an error occurs.
    """
    if not tiktoken:
        console.log("[yellow]Tokenization is disabled because tiktoken is not installed.[/yellow]")
        return None
    try:
        enc = tiktoken.encoding_for_model(model)
        tokens = enc.encode(text)
        return len(tokens)
    except (ValueError, RuntimeError) as e:
        logging.error("Error during tokenization: %s", e)
        return None

@app.command()
def extract(
    directory: str = typer.Option(
        os.getcwd(), "--directory", "-d", help="Target directory to extract."
    ),
    output: str = typer.Option(
        "codebase.txt", "--output", "-o", help="Output file name."
    ),
    output_format: str = typer.Option(
        "text", "--output-format", "-f",
        help="Output format: 'text' or 'json'.", show_default=True
    ),
    tokenize: bool = typer.Option(
        False, "--tokenize", "-t", help="Display token count for the output."
    ),
    config: Optional[str] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to a YAML configuration file with ignore rules. "
             "If not provided, the script first checks for 'llmify_config.yaml' "
             "in the target directory. If not found, it falls back to the "
             "'llmify_config.yaml' in the project root."
    )
):
    """
    Extract the codebase from the given directory and output it in text or JSON format.
    Optionally, count tokens for the output.

    Command-line Options:
        --directory (-d): Target directory to extract from.
        --output (-o): Output file name.
        --output-format (-f): Format of the output file ('text' or 'json').
        --tokenize (-t): If set, counts tokens in the final output.
        --config (-c): Path to a YAML file with ignore rules.
    """
    abs_directory = os.path.abspath(directory)
    console.log("[blue]Target directory:[/blue] %s", abs_directory)

    # Determine the configuration file to use.
    config_path = determine_config_path(abs_directory, config)
    if config_path:
        config_data = load_config(config_path)
    else:
        config_data = {"ignored_dirs": [], "ignored_files": []}

    ignored_dirs, ignored_files = merge_ignore_rules(config_data)

    if not typer.confirm("Proceed with code extraction?"):
        console.log("[red]Extraction cancelled by user.[/red]")
        raise typer.Exit()

    if output_format.lower() == "json":
        extract_code_json(abs_directory, output, ignored_dirs, ignored_files)
    else:
        extract_code_text(abs_directory, output, ignored_dirs, ignored_files)

    if tokenize:
        try:
            with open(output, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            token_count = count_tokens_in_text(content)
            if token_count is not None:
                console.log("[green]Total token count:[/green] %s", token_count)
        except OSError as e:
            logging.error("Error reading output file for tokenization: %s", e)

def main():
    """
    Main entry point for the LLMify-Code extraction tool.
    """
    app()

if __name__ == "__main__":
    main()
