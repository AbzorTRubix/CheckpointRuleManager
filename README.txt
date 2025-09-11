Check Point Rule Manager
========================
Starting Virtual Environment
----------------------------
### Powershell
```
py -m venv venv
Set-ExecutionPolicy Unrestricted -Scope Process -Force
venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

### Mac OS X/Linux
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

Running the Program
-------------------
### Powershell
```
cd src/main/python
py -m client SMS_IP
```

### Linux
```
cd src/main/python
python3 -m client SMS_IP
```

Command Usage
-------------
***IF ANY STRING CONTAINS WHITESPACE MAKE SURE IT IS ENCAPSULATED IN DOUBLE QUOTES ""***  
***LISTS ARE REPRESENTED BY COMMAS i.e. ITEM1,ITEM2,"ITEM 3"***
### Add Rule - Manual
```
>>add-rule NAME SOURCE DESTINATION SERVICES ACTION POSITION LAYER
```
NAME (String) - Rule Name  
SOURCE (String | List) - Designated source(s)  
DESINTATION (String | List) - Designated Destination(s)  
SERVICE (String | List) - Designated Services(s)  
ACTION (String) - Must be "Accept", "Drop", "Ask", "Inform", "Reject", "User Auth", "Client Auth", "Apply Layer"  
POSITION (Number | "top" | "bottom") - Position to be placed in rule base.
LAYER (String) - Layer to contain the rule  

### Add Rule - Restoring from JSON
Access rule's, when deleted with this client, store a backup in folder designated folder called "deleted_rules".  
In there you will find a text file mapping a deleted rule to it's JSON file. That file can be used as follows to restore a deleted rule.
```
>>add-rule JSON_FILE
```
JSON_FILE (String) - Name of the JSON file to use.

### Delete Rule
```
>>delete-rule RULE LAYER
```
RULE (Number | String) - Rule to be deleted  
LAYER (String) - Access Rule Layer Containing the rule

### Disable Rule
```
>>disable-rule RULE LAYER
```
RULE (Number | String) - Rule to be disabled  
LAYER (String) - Access Rule Layer Containing the rule

### Enable Rule
```
>>enable-rule RULE LAYER
```
RULE (Number | String) - Rule to be deleted  
LAYER (String) - Access Rule Layer Containing the rule

### Clear Backups Folder
Deletes the folder containing the JSON backups
```
>>clear-backups
```

### Cleanup Rulebase
Goes through the requested rule base and identifies rules with a hit count < 10 to be disabled.
```
>>cleanup-rulebase LAYER
```
LAYER (String) - Access Rule Layer Containing the rule

### Cleanup Disabled Rules
Goes through the requested rule base and identifies rules that are disabled to be deleted.
```
>>cleanup-disabled-rules LAYER
```
LAYER (String) - Access Rule Layer Containing the rule

### Publish Changes
```
>>publish
```
### Logout
```
>>exit
```

Running Tests
-------------
### Powershell
```
$env:PYTHONPATH="src\main\python"
pytest src\test\python --verbose
```

### Linux
```
export PYTHONPATH=src/main/python
pytest src/test/python --verbose
```