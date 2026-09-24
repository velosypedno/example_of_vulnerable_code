# example_of_vulnerable_code

### Requirements

*Python 3.14.7*

### Installation 

1. git clone git@github.com:velosypedno/example_of_vulnerable_code.git
2. cd example_of_vulnerable_code
3. python -m venv .venv
4. source ./.venv/bin/activate
5. pip install -r requirements.txt 

Also you can install necessary tools for sast

```bash
pip install -r requirements_with_sast.txt
```

**Usage:**

```bash
semgrep --config auto ./
```

```bash
bandit -r src/ -f html -o ./bandit_reports/{report_name}.html
```
