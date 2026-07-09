# Demo 2: Python Error Diagnosis

## Goal

Show how RepoPilot Hy3 diagnoses a common Python reproduction error.

## Input

Paste the project context from `examples/demo-python-error/README.md` and this terminal log:

```text
Traceback (most recent call last):
  File "main.py", line 1, in <module>
    import requests
ModuleNotFoundError: No module named 'requests'
```

## Expected Hy3 Output

- Identifies the missing dependency.
- Points to `requirements.txt` as the evidence source.
- Suggests creating/activating a virtual environment.
- Suggests `pip install -r requirements.txt`.
- Adds verification with `python main.py`.

