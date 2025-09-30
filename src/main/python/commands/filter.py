from client.client import Client
from .parser import *
from .errors import *

GROUP_SIZE = 10

def find_rule_num(unfiltered_rules: list[dict],requested_rule: dict):
    for rule in unfiltered_rules:
        if rule['uid'] == requested_rule['uid']:
            return unfiltered_rules.index(rule)
    return -1

def get_rulebase(client: Client, rulebase: str, size: int,filter = ''):
    result = []
    offset = 0
    num = size
    while(num > 0):
        if num > GROUP_SIZE:
            rules = client.api_call('show-access-rulebase',{'name':rulebase,'show-hits':True,'limit':GROUP_SIZE,'offset':offset,'filter':filter}).response()['data']['rulebase']
        else:
            rules = client.api_call('show-access-rulebase',{'name':rulebase,'show-hits':True,'limit':num,'offset':offset,'filter':filter}).response()['data']['rulebase']
        for rule in rules:
            result.append(rule)
        num = num - GROUP_SIZE
        offset = offset + GROUP_SIZE
    return result

def filter_low_activity(client: Client,args: list):
    ##TO DO
    ###ADD IN ARG PARSING
    rule_base = client.api_call('show-access-rulebase',{'name':args[0],'show-hits':True,'limit':1}).response()['data']
    filter = '' if len(args) == 1 else args[1]
    N = rule_base['total']
    filtered_rules = get_rulebase(client,args[0],N,filter)
    unfiltered_rules = get_rulebase(client,args[0],N)
    print('Rule Number:\t\tRule Name:')
    for rule in filtered_rules:
        if 'hits' in rule.keys(): 
            if rule['hits']['value'] < 100:
                rule_num = find_rule_num(unfiltered_rules,rule) + 1
                print(rule_num,'\t\t\t',rule['name'])

            
