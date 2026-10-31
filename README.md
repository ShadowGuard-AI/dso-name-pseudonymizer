![Banner](banner.png)

# dso-name-pseudonymizer
Replaces names in text with pseudonyms generated from a configurable list or algorithmically. Allows preserving name format (e.g., first name last name) and gender. - Focused on Tools for sanitizing and obfuscating sensitive data within text files and structured data formats

## Install
`git clone https://github.com/ShadowStrikeHQ/dso-name-pseudonymizer`

## Usage
`python main.py input.txt output.txt [-n names.txt] [-g male|female] [-l locale]`

## How names are matched
- Name pairs are replaced as whole tokens: title case pairs, all capitals pairs, Mc and Mac forms (McDonald, MacDonald), O'Brien style apostrophe forms, and hyphenated names (Mary-Jane Watson, John Smith-Jones). A hyphenated name is replaced whole, never in part.
- A single name is replaced only in a marked context: after "name is", after "named", after "called", or after an honorific such as Mr., Mrs., Ms., Dr., or Miss. A single name with no marker is left unchanged.
- Limit: any other two word pair in name shape is treated as a name, since no pattern only check can tell it apart from a real name. A pair such as New York is therefore replaced too.

## Mapping
- Within one run, each distinct original name always receives the same pseudonym, at every occurrence. Records for one person can therefore be followed across the output of a single run. A new run assigns a new set of pseudonyms.
- Two different original names never share a pseudonym in one run.
- If a name list has fewer unused names than the distinct names in the text, further pseudonyms are generated with Faker so that no pseudonym is shared.

## Run results
- The output file may not be the input file. A run that names the same file for input and output, in any spelling, is refused at exit 1 before anything is written.
- A run that replaces nothing, such as an empty or name free input, prints "Nothing was pseudonymized" and exits non-zero instead of reporting success. No output file is written in that case.
- A successful run prints how many replacements it made.

## Parameters
- `-h`: Show help message and exit
- `-n`: Path to a file containing a list of names, one per line
- `-g`: Gender of names to generate.
- `-l`: Locale for generating fake names (default: en_US)
- `--log_level`: Set the logging level.

## License
Copyright (c) ShadowGuard-AI
