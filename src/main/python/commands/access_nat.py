from client.client import Client
from .parser import *
from .errors import *
import json,uuid,os,shutil,datetime
import logging
from .filter import *

logger = logging.getLogger(__name__)

def add_rule(client: Client,args: list):
    '''
    Function: add_rule()
    Description: adds a rule to rulebase either by manual input, or through cached .json file.
    '''
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

def review_no_hit(client: Client, args: list[str]):
    '''
    Function: review_not_hit()
    Description: Queries the rulebase for rules with hit counts less than 10 and gives user decision in disabling of the rule.
    '''
    if args!= None and len(args) != 1:
        raise CommandException(f'expected one rulebase, got {len(args)}')
    num = client.api_call('show-access-rulebase',{'name':args[0],'show-hits':True,'limit':1}).response()['data']['total']
    result = get_rulebase(client,args[0],num)
    for rule in result:
        if 'hits' in rule:
            if rule['hits']['value'] < 10:
                decision = input(f'The following rule:\n{rule['name']}\nhas the following hit count: {rule['hits']['value']}\nDisable?(y/n): ')
                if decision == 'y':
                    disable_rule(client,[rule['name'],args[0]])

def review_disabled(client: Client, args: list[str]):
    '''
    Function: Queries the rulebase for rules that are currently disabled, and gives user decision in deleting the rule. 
    If deleted, a .json object containing the original object is created.
    Description: 
    '''
    if args!= None and len(args) != 1:
        raise CommandException(f'expected one rulebase, got {len(args)}')
    num = client.api_call('show-access-rulebase',{'name':args[0],'show-hits':True,'limit':1}).response()['data']['total']
    result = get_rulebase(client,args[0],num)
    for rule in result:
        if 'enabled' in rule and rule['enabled'] == False:
            decision = input(f'The following rule is disabled:\n{rule['name']}\nComments:{rule['comments']}\nDelete?(y/n): ')
            if decision == 'y':
                delete_rule(client,[rule['name'],args[0]])

def get_rule(client: Client, rules: list[str]) -> tuple[dict,str]:
    '''
    Function: get_rule()
    Description: obtains a rule object from the rulebase.
    '''
    if len(rules) != 2:
        raise CommandException(f'expected two arguments, got {len(rules)}')
    rule, layer = rules
    if not isinstance(rule,str):
        raise ValueError(f'expected a string or number')
    identifier = 'rule-number' if rule.isdigit() else 'name'
    payload = {identifier: rule,'layer': layer}
    rule = client.api_call('show-access-rule',payload).response()['data']
    return rule, layer

def backup_rule(data: dict):
    '''
    Function: backup_rule()
    Description: Backs up a rule object as a .json file
    '''
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
    '''
    Function: clear_backups()
    Description: clears out the cached deleted rules.
    '''
    if os.path.exists('deleted_rules') and os.path.isdir('deleted_rules'):
        shutil.rmtree('deleted_rules')
    else:
        return

def delete_rule(client: Client, args: list[str]):
    '''
    Function: delete_rule()
    Description: Deletes a rule from the rulebase after client decision, requests a back up be made if deleted.
    '''
    if '?' in args:
        print('delete-rule [NAME | NUMBER] LAYER')
        return
    rule, layer = get_rule(client,args)
    backup_rule(rule)
    decision = input(f'You chose to delete rule {rule['name']}\nConfirm(y/n)>>').lower()
    if decision == 'y':
        _ = client.api_call('delete-access-rule',{'name': rule['name'],'layer':layer})
        logger.info(f' - deleted rule {rule['name']}')
    pass

def enable_rule(client: Client, args: list[str]):
    '''
    Function: enable_rule()
    Description: Enables a rule in the rulebase.
    '''
    if '?' in args:
        print('enable-rule [NAME | NUMBER] LAYER')
        return
    rule, layer = get_rule(client,args)
    decision = input(f'You chose to enable rule {rule['name']}\nConfirm(y/n)>>').lower()
    if decision == 'y':
        new_name = rule['name'][(rule['name'].find(' - ') + 3):]
        _ = client.api_call('set-access-rule',{'name': rule['name'],'layer':layer,'enabled':True,'new-name':new_name})
        logger.info(f' - enabled rule {rule['name']}')
        
def disable_rule(client: Client,args: list[str]):
    '''
    Function: disable_rule()
    Description: Disables a rule in the rulebase.
    '''
    if '?' in args:
        print('disable-rule [NAME | NUMBER] LAYER')
        return
    rule, layer = get_rule(client,args)
    decision = input(f'You chose to disable rule {rule['name']}\nConfirm(y/n)>>').lower()
    if decision == 'y':
        new_name = f'Disabled by {client.username} on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - {rule['name']}'
        _ = client.api_call('set-access-rule',{'name': rule['name'],'layer':layer,'enabled':False,'new-name':new_name})
        logger.info(f' - disabled rule {rule['name']}')
