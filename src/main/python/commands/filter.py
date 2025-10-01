from client.client import Client
from .parser import *
from .errors import *
import openpyxl
import os
import logging

logger = logging.getLogger(__name__)

GROUP_SIZE = 10

def append_list_to_excel(file_name, data_list):
    if os.path.exists(file_name):
        # Load existing workbook
        wb = openpyxl.load_workbook(file_name)
        ws = wb.active
    else:
        # Create new workbook
        wb = openpyxl.Workbook()
        ws = wb.active

    # Append the list as a new row
    ws.append(data_list)

    # Save the workbook
    wb.save(file_name)
    logger.info(f"Appended {data_list[1]} to {file_name}")

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
            if 'rulebase' in rule:
                for sect_rule in rule['rulebase']:
                    result.append(sect_rule)
            else:
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
    append_list_to_excel('filtered_list.xlsx', ['Rule Number','Rule Name','Hit Count'])
    for rule in filtered_rules:
        if 'hits' in rule.keys(): 
            if rule['hits']['value'] < 100 and rule['enabled'] == True:
                rule_num = find_rule_num(unfiltered_rules,rule) + 1
                name = '' if 'name' not in rule else rule['name']
                append_list_to_excel('filtered_list.xlsx', [rule_num,name,rule['hits']['value']])

            
