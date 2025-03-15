"""
test_extractor.py

This module contains unit tests for the `llm_code_prep` script.
It tests the functionality of:
- Generating a directory tree while respecting ignored directories/files.
- Extracting a JSON representation of the codebase.
- Counting tokens in a text using `tiktoken` if available.

Each test creates a temporary directory and files, ensuring that the tests are
isolated and do not depend on an actual codebase.

Usage:
    Run pytest to execute all tests.
"""
import os
import tempfile
import shutil
import json
from extractor import llm_code_prep

def create_sample_directory(base_dir: str) -> None:
    """
    Create a sample directory structure for testing.

    The structure includes:
      - A subdirectory 'src' containing a sample file.
      - A directory 'node_modules' that should be ignored.
      - A sample file 'file1.txt' in the base directory.
      - An ignored file 'llm_code_prep.py' in the base directory.
    """
    os.makedirs(os.path.join(base_dir, "src"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "node_modules"), exist_ok=True)  # Should be ignored

    # Create a valid file in the base directory.
    with open(os.path.join(base_dir, "file1.txt"), "w", encoding="utf-8") as f:
        f.write("Content of file1")

    # Create a valid file in the 'src' subdirectory.
    with open(os.path.join(base_dir, "src", "file2.txt"), "w", encoding="utf-8") as f:
        f.write("Content of file2")

    # Create an ignored file in the base directory.
    with open(os.path.join(base_dir, "llm_code_prep.py"), "w", encoding="utf-8") as f:
        f.write("This file should be ignored.")

def test_get_directory_tree() -> None:
    """
    Test that the directory tree is generated correctly
    and that ignored directories and files are excluded.

    Expected behavior:
      - 'node_modules' and 'llm_code_prep.py' should not appear in the output.
      - 'file1.txt' and 'file2.txt' should be present.
    """
    temp_dir = tempfile.mkdtemp()
    try:
        create_sample_directory(temp_dir)

        # Define ignored rules matching the ones used in the application.
        ignored_dirs = {"node_modules"}
        ignored_files = {"llm_code_prep.py"}

        # Generate the directory tree.
        tree = llm_code_prep.get_directory_tree(temp_dir, ignored_dirs, ignored_files)

        # Verify that the ignored directory and file are not in the tree.
        assert "node_modules" not in tree
        assert "llm_code_prep.py" not in tree

        # Verify that valid files are listed.
        assert "file1.txt" in tree
        assert "file2.txt" in tree
    finally:
        shutil.rmtree(temp_dir)

def test_json_output() -> None:
    """
    Test that the JSON output is generated correctly.

    The JSON should include:
      - A 'directory_tree' key with the generated directory tree.
      - A 'files' key that is a list containing metadata for each file.
      - A 'total_tokens' key representing the total token count.
    Additionally, files in ignored directories or with ignored names should not appear.
    """
    temp_dir = tempfile.mkdtemp()
    output_file = os.path.join(temp_dir, "output.json")
    try:
        create_sample_directory(temp_dir)

        # Define ignored rules.
        ignored_dirs = {"node_modules"}
        ignored_files = {"llm_code_prep.py"}

        # Generate JSON output.
        llm_code_prep.extract_code_json(temp_dir, output_file, ignored_dirs, ignored_files)

        # Load the JSON file.
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check that required keys are present.
        assert "directory_tree" in data
        assert "files" in data
        assert "total_tokens" in data

        # Ensure that ignored files/directories are not present.
        for file_info in data["files"]:
            assert "node_modules" not in file_info["filename"]
            assert "llm_code_prep.py" not in file_info["filename"]

    finally:
        shutil.rmtree(temp_dir)

def test_token_count() -> None:
    """
    Test the token counting functionality.

    This test verifies that the function 'count_tokens_in_text' returns an integer
    greater than zero when tiktoken is installed, or None otherwise.
    """
    sample_text = "Hello, world! This is a test."
    token_count = llm_code_prep.count_tokens_in_text(sample_text, model="gpt-4")

    # If token_count is available, it should be an integer greater than zero.
    if token_count is not None:
        assert isinstance(token_count, int)
        assert token_count > 0

if __name__ == "__main__":
    test_get_directory_tree()
    test_json_output()
    test_token_count()
