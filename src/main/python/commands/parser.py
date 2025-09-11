from pathlib import Path
from .errors import *

RULE_ACTIONS = {"Accept", "Drop", "Ask", "Inform", "Reject", "User Auth", "Client Auth", "Apply Layer"}
NAME = 0
SOURCE = 1
DEST = 2
SERVICES = 3
ACTION = 4
POSITION = 5
LAYER = 6
ADD_RULE_COUNT = 7

def parse_text_file(filename):
    current_dir = Path(__file__).resolve().parent
    target_dir = current_dir.parent.parent.parent.parent
    file_path = target_dir / filename
    lines = []
    with file_path.open('r') as file:
        for line in file:
            line = line.strip()
            if len(line) != 0:
                lines.append(line)
    return lines

def parse_command_args(args):
    result = []
    current_str = ''
    current_arg = []
    in_quote = False
    for char in args:
        if not in_quote:
            if char == '"':
                in_quote = True
            elif char == ',':
                current_arg.append(current_str)
                current_str = ''
            elif char.isspace():
                if len(current_str) != 0:
                    current_arg.append(current_str)
                if len(current_arg) == 1:
                    result.append(current_arg[0])
                elif len(current_arg) != 0:
                    result.append(current_arg)
                current_arg = []
                current_str = ''
            else:
                current_str = current_str + char
        else:
            if char == '"':
                in_quote = False
            else:
                current_str = current_str + char
    if len(current_str) != 0:
        result.append(current_str)
    return result

def parse_command_add_rule(args):
    if len(args) == 1 and '.json' in args[0]:
        return args[0]
    if len(args) != ADD_RULE_COUNT:
        raise CommandException(f'expected 7 arguments, got {len(args)}')
    if not isinstance(args[NAME],str):
        raise ValueError('rule name must be a string')
    for obj in args[SOURCE:ACTION]:
        if not isinstance(obj, str) and not (isinstance(obj, list) and all(isinstance(item, str) for item in obj)):
            raise ValueError('rule source, destination, and services must be a string or list of strings')
    if args[ACTION] not in RULE_ACTIONS:
        raise ValueError(f'action must be one of the following: {RULE_ACTIONS}')
    if args[POSITION] != 'top' and args[5] != 'bottom' and not isinstance(args[5],int):
        raise ValueError(f'rule position must be the top, bottom, or a specific rule number position')
    return args


