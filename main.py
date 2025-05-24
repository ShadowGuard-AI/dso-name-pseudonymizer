#!/usr/bin/env python3
import argparse
import logging
import random
import re
import sys
from typing import List, Optional

try:
    from faker import Faker
    import chardet
except ImportError as e:
    print(f"Error: Missing dependencies. Please install them: pip install faker chardet")
    sys.exit(1)


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NamePseudonymizer:
    """
    Replaces names in text with pseudonyms generated from a configurable list or algorithmically.
    Allows preserving name format (e.g., first name last name) and gender.
    """

    def __init__(self, name_list_path: Optional[str] = None, gender: Optional[str] = None, locale: str = 'en_US'):
        """
        Initializes the NamePseudonymizer.

        Args:
            name_list_path (Optional[str]): Path to a file containing a list of names.  One name per line.
            gender (Optional[str]): Gender of names to generate ('male', 'female', or None for both).
            locale (str): Locale to use for generating fake names.
        """
        self.names = []
        self.gender = gender
        self.locale = locale
        self.fake = Faker(self.locale)

        if name_list_path:
            try:
                with open(name_list_path, 'r', encoding='utf-8') as f:
                    self.names = [line.strip() for line in f]
            except FileNotFoundError:
                logging.error(f"Name list file not found: {name_list_path}")
                raise
            except Exception as e:
                logging.error(f"Error reading name list file: {e}")
                raise

    def _generate_pseudonym(self) -> str:
        """
        Generates a pseudonym based on the configured settings.
        """
        if self.names:
            return random.choice(self.names)
        else:
            if self.gender == 'male':
                return self.fake.name_male()
            elif self.gender == 'female':
                return self.fake.name_female()
            else:
                return self.fake.name()

    def pseudonymize_text(self, text: str) -> str:
        """
        Replaces names in the input text with pseudonyms.

        Args:
            text (str): The input text to pseudonymize.

        Returns:
            str: The pseudonymized text.
        """

        # Regular expression to find names.  This is a simplified version and may need to be adjusted for more complex scenarios.
        name_pattern = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b'  # Matches "Firstname Lastname"

        def replace_name(match):
            """
            Replaces a matched name with a pseudonym.
            """
            return self._generate_pseudonym()

        pseudonymized_text = re.sub(name_pattern, replace_name, text)
        return pseudonymized_text


def setup_argparse() -> argparse.ArgumentParser:
    """
    Sets up the command-line argument parser.

    Returns:
        argparse.ArgumentParser: The argument parser.
    """
    parser = argparse.ArgumentParser(description='Replaces names in text with pseudonyms.')
    parser.add_argument('input_file', help='Path to the input text file.')
    parser.add_argument('output_file', help='Path to the output text file.')
    parser.add_argument('-n', '--name_list', help='Path to a file containing a list of names (one per line).', required=False)
    parser.add_argument('-g', '--gender', choices=['male', 'female'], help='Gender of names to generate.', required=False)
    parser.add_argument('-l', '--locale', default='en_US', help='Locale for generating fake names (default: en_US).', required=False)
    parser.add_argument('--log_level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO', help='Set the logging level.')
    return parser


def main():
    """
    Main function to execute the name pseudonymizer.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    # Set logging level
    logging.getLogger().setLevel(args.log_level)

    try:
        # Input validation
        if args.name_list and args.gender:
             logging.warning("Both --name_list and --gender are specified.  Using --name_list and ignoring --gender.") # not fatal
        try:
            pseudonymizer = NamePseudonymizer(args.name_list, args.gender, args.locale)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            sys.exit(1) # critical.
        except Exception as e:
            print(f"Error initializing pseudonymizer: {e}")
            sys.exit(1)

        # Determine file encoding
        with open(args.input_file, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']

        # Read the input file
        try:
            with open(args.input_file, 'r', encoding=encoding) as infile:
                text = infile.read()
        except FileNotFoundError:
            logging.error(f"Input file not found: {args.input_file}")
            print(f"Error: Input file not found: {args.input_file}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"Error reading input file: {e}")
            print(f"Error reading input file: {e}")
            sys.exit(1)

        # Pseudonymize the text
        pseudonymized_text = pseudonymizer.pseudonymize_text(text)

        # Write the output to a file
        try:
            with open(args.output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(pseudonymized_text)
        except Exception as e:
            logging.error(f"Error writing to output file: {e}")
            print(f"Error writing to output file: {e}")
            sys.exit(1)

        logging.info(f"Pseudonymized text written to {args.output_file}")
        print(f"Pseudonymized text written to {args.output_file}")

    except Exception as e:
        logging.critical(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


# Usage Examples:
# 1. Basic usage: python dso-name-pseudonymizer.py input.txt output.txt
# 2. With a name list: python dso-name-pseudonymizer.py input.txt output.txt -n names.txt
# 3. Generating male names: python dso-name-pseudonymizer.py input.txt output.txt -g male
# 4. Specifying locale: python dso-name-pseudonymizer.py input.txt output.txt -l fr_FR
# 5. With debugging logs: python dso-name-pseudonymizer.py input.txt output.txt --log_level DEBUG

# Offensive Tool Considerations:
# This tool, while designed for data sanitization, could be misused to generate realistic-sounding fake documents or communications.  Implement safeguards such as rate limiting, logging of usage, and clearly state the ethical implications in the documentation.  Consider adding a disclaimer that the tool should only be used for legitimate purposes.