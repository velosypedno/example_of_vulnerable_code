# example_of_vulnerable_code

### Requirements

1. *Python 3.14.7*
2. *Trivy 0.73.0*
3. *Docker 29.7.2*
4. *Syft 1.51.0*

### Installation 

1. Clone repo
```bash
git clone git@github.com:velosypedno/example_of_vulnerable_code.git
```
2. Change working dir
```bash
cd example_of_vulnerable_code
```
3. Create virtual enviroment
```bash
python -m venv .venv
```
4. Activate virtual environmnet
```bash
source ./.venv/bin/activate
```
5. Install dependencies 
```bash
pip install -r requirements.txt 
```

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

### Build docker iamge and scan

```bash
docker build -t example:latest .
```

```bash
trivy image example:latest
```

If we need sbom only for out source code:

```bash
trivy fs --format json -o report-files.json .
```

OR

```bash
trivy fs --format table -o report-files.txt .
```

### SBOM usage

```bash
syft dir:. -o cyclonedx-json > sbom.json
```

```bash
trivy sbom sbom.json
```
