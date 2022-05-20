# Jira Extractor

## Requirements
Python >3.9

## Usage

1. Populate `input` file with the list of JIRA issue IDs (one ID per row)
2. Run `python get_jira.py > output.txt`. It will write to `output.txt` file the issue status changelog of the given IDs.