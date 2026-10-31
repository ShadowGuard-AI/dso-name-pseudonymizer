![Banner](banner.png)

# dso-name-pseudonymizer
Replaces names in text with pseudonyms generated from a configurable list or algorithmically. Allows preserving name format (e.g., first name last name) and gender. - Focused on Tools for sanitizing and obfuscating sensitive data within text files and structured data formats

## How names are matched
- Two word names are matched as whole tokens in title case, all capitals, Mc and Mac forms (McDonald, MacArthur), apostrophe forms (O'Brien), and hyphenated forms. A hyphenated name is replaced whole, never partly.
- A single name is replaced only in a marked context: after "name is", "named", or "called", or after an honorific (Mr., Mrs., Ms., Dr., Miss).
- Within one run, each distinct original name gets one pseudonym, reused at every occurrence, and two different original names never share a pseudonym. Records for one person can therefore be followed across the output of a single run. A new run assigns a new set of pseudonyms.

## Known limit
Matching is pattern based and uses no dictionary. Any other two word pair in name shape (two capitalized words in a row) is treated as a name and replaced, since no pattern only check can tell it apart from a real name. Single names outside the marked contexts listed above are left unchanged.

## Install
`git clone https://github.com/ShadowGuard-AI/dso-name-pseudonymizer`

## Usage
`python3 main.py [params] input_file output_file`

## Parameters
- `-h`: Show help message and exit
- `-n`, `--name_list`: Path to a file containing a list of names (one per line).
- `-g`, `--gender`: Gender of names to generate.
- `-l`, `--locale`: Locale for generating fake names (default: en_US).
- `--log_level`: Set the logging level.

## Exit behavior
- Exit 0: at least one name was replaced. The success line reports the replacement count.
- Exit 1: the input file or name list is missing, the output path resolves to the input file (the tool refuses to overwrite its input, under any spelling of the path), or nothing was pseudonymized. A run that finds no names prints a plain "Nothing was pseudonymized" line, writes no output file, and exits 1.

## License
Copyright (c) ShadowGuard-AI
