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
    i = 0
    while i < len(args):
        item = args[i]
        if item.isdigit():
            item = int(item)
        if isinstance(item, str) and ',' in item:
            parts = [part.strip() for part in item.split(',')]
            result.append(parts)
            i += 1
        elif isinstance(item, str) and item.startswith('"') and not item.endswith('"'):
            quoted_parts = [item.strip('"')]
            i += 1
            while i < len(args):
                next_item = args[i]
                quoted_parts.append(next_item.strip('"'))
                if isinstance(next_item, str) and next_item.endswith('"'):
                    break
                i += 1
            result.append(' '.join(quoted_parts))
            i += 1
        else:
            result.append(item)
            i += 1
    return result

def parse_command_add_rule(args):
    args = parse_command_args(args)
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


