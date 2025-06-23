import os
from .dictionary_lib import DictionaryMaxlength

BLUE = "\033[1;34m"
RESET = "\033[0m"

def main(args):
    default_output = {
        "json": "dictionary_maxlength.json"
    }[args.format]

    output_file = args.output or default_output
    output_file_path = os.path.abspath(output_file)  # Get full path
    dictionaries = DictionaryMaxlength.from_dicts()

    if args.format == "json":
        dictionaries.serialize_to_json(output_file_path)
        print(f"{BLUE}Dictionary saved in JSON format at: {output_file_path}{RESET}")

    return 0
