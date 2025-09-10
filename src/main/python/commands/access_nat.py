from client.client import Client
from .parser import *
from .errors import *
import json,uuid,os,shutil,datetime
import logging

logger = logging.getLogger(__name__)

def add_rule(client: Client,args: list):
    if '?' in args:
        print('add-rule NAME SOURCE DESTINATION SERVICES ACTION POSITION LAYER')
        return
    args = parse_command_add_rule(args)
    if isinstance(args,str):
        json_file_path = f'deleted_rules/{args}'
        if not os.path.exists(json_file_path):
            raise FileNotFoundError(f"File not found: {json_file_path}")
        with open(json_file_path, 'r') as f:
            payload = json.load(f)
        if not isinstance(payload, dict):
            raise ValueError("The JSON file does not contain a dictionary at the top level.")
    else:
        payload = {
            'name': args[NAME],
            'layer': args[LAYER],
            'position': args[POSITION],
            'action': args[ACTION],
            'source': args[SOURCE],
            'destination': args[DEST],
            'service': args[SERVICES],
            'enabled':True,
            'install-on':'Policy Targets',
            'track':{
                'accounting':False,
                'alert':'snmp',
                'per-session':True,
                'type':'Log'
            }
        }
    _ = client.api_call('add-access-rule',payload)
    logger.info(f' - added rule {args[NAME]} at position {args[POSITION]}')

def review_no_hit(client: Client, rulebase: list[str]):
    if rulebase!= None and len(rulebase) != 1:
        raise CommandException(f'expected one rulebase, got {len(rulebase)}')
    result = client.api_call('show-access-rulebase',{'name':rulebase[0],'show-hits':True}).response()['data']['rulebase']
    for rule in result:
        if rule['hits']['value'] < 10:
            decision = input(f'The following rule:\n{rule['name']}\nhas the following hit count: {rule['hits']['value']}\nDisable?(y/n): ')
            if decision == 'y':
                disable_rule(client,[rule['name'],rulebase[0]])

def review_disabled(client: Client, rulebase: list[str]):
    if rulebase!= None and len(rulebase) != 1:
        raise CommandException(f'expected one rulebase, got {len(rulebase)}')
    result = client.api_call('show-access-rulebase',{'name':rulebase[0],'filter':'disabled'}).response()['data']['rulebase']
    for rule in result:
        decision = input(f'The following rule is disabled:\n{rule['name']}\nComments:{rule['comments']}\nDelete?(y/n): ')
        if decision == 'y':
            delete_rule(client,[rule['name'],rulebase[0]])

def get_rule(client: Client, rules: list[str]):
    if len(rules) != 2:
        raise CommandException(f'expected two arguments, got {len(rules)}')
    rule, layer = rules
    if not isinstance(rule,str) and not isinstance(rule,int):
        raise ValueError(f'expected a string or number')
    identifier = 'rule-number' if isinstance(rule,int) else 'name'
    payload = {identifier: rule,'layer': layer}
    rule = client.api_call('show-access-rule',payload).response()['data']
    return rule, layer

def backup_rule(data):
    fields = [
        "layer", "position", "name", "action", "action-settings", "content", 
        "content-direction", "content-negate", "custom-fields", "destination", 
        "destination-negate", "enabled", "inline-layer", "install-on", 
        "service", "service-negate", "service-resource", "source", 
        "source-negate", "tags", "time", "track", "user-check", "vpn", 
        "comments", "details-level", "ignore-warnings", "ignore-errors"
    ]
    result = {}
    for field in fields:
        if field in data:
            if field == 'action':
                result[field] = data[field]['name']
            elif field == 'track':
                result[field] = data[field]
                result[field]['type'] = result[field]['type']['name']
            elif isinstance(data[field],list):
                objects = []
                for item in data[field]:
                    objects.append(item['name'])
                result[field] = objects
            else:
                result[field] = data[field]
    result['position'] = 'Bottom'
    os.makedirs('deleted_rules', exist_ok=True)
    random_filename = f"{uuid.uuid4().hex}.json"
    file_path = os.path.join('deleted_rules', random_filename)
    with open(file_path, 'w') as f:
        json.dump(result, f, indent=4)
    mapping = f"{result['name']} -> {random_filename}\n"
    mapping_path = os.path.join('deleted_rules', 'rule_mapping.txt')
    logger.info(f' - backed up rule {result['name']} to file {random_filename}')
    with open(mapping_path, 'a') as f:
        f.write(mapping)

def clear_backups(client: Client, args: list[str]):
    if os.path.exists('deleted_rules') and os.path.isdir('deleted_rules'):
        shutil.rmtree('deleted_rules')
    else:
        return

def delete_rule(client: Client, args: list[str]):
    rules = parse_command_args(args)
    if '?' in rules:
        print('delete-rule [NAME | NUMBER] LAYER')
        return
    rule, layer = get_rule(client,rules)
    backup_rule(rule)
    decision = input(f'You chose to delete rule {rule['name']}\nConfirm(y/n)>>').lower()
    if decision == 'y':
        _ = client.api_call('delete-access-rule',{'name': rule['name'],'layer':layer})
        logger.info(f' - deleted rule {rule['name']}')
    pass

def enable_rule(client: Client, args: list[str]):
    rules = parse_command_args(args)
    if '?' in rules:
        print('enable-rule [NAME | NUMBER] LAYER')
        return
    rule, layer = get_rule(client,rules)
    decision = input(f'You chose to enable rule {rule['name']}\nConfirm(y/n)>>').lower()
    if decision == 'y':
        new_name = rule['name'][(rule['name'].find(' - ') + 3):]
        _ = client.api_call('set-access-rule',{'name': rule['name'],'layer':layer,'enabled':True,'new-name':new_name})
        logger.info(f' - enabled rule {rule['name']}')
        
def disable_rule(client: Client,args: list[str]):
    rules = parse_command_args(args)
    if '?' in rules:
        print('disable-rule [NAME | NUMBER] LAYER')
        return
    rule, layer = get_rule(client,rules)
    decision = input(f'You chose to disable rule {rule['name']}\nConfirm(y/n)>>').lower()
    if decision == 'y':
        new_name = f'Disabled by {client.username} on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - {rule['name']}'
        _ = client.api_call('set-access-rule',{'name': rule['name'],'layer':layer,'enabled':False,'new-name':new_name})
        logger.info(f' - disabled rule {rule['name']}')
