Check Point Rule Deleter
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