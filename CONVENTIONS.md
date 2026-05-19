# ColdGuard — Development Conventions & Standards

## Introduction

This document defines the coding standards, naming conventions, and 
workflows for the ColdGuard project.

**All contributors must read and follow these conventions before 
writing any code.**

ColdGuard is built by a small team — consistency is what keeps the 
codebase readable and maintainable as we grow. When in doubt, follow 
these conventions. If something is not covered here, discuss with the 
team and update this document.

---

## Golden Rules

1. **English only** — code, comments, commits, PRs, documentation
2. **Never push directly to main** — always Branch → PR → Review → Merge
3. **Never merge your own PR** — another person must review and approve
4. **Never use magic numbers** — always use constants
5. **Never just `pip install`** — always update requirements.in first
6. **Tests must pass** — never merge a PR with failing CI

---

## Python (Backend)

| Type | Format | Example |
|---|---|---|
| Files | snake_case | `models.py`, `views.py` |
| Variables | snake_case | `temp_reading`, `device_key` |
| Classes | PascalCase | `TemperatureReading`, `Device` |
| Constants | UPPER_CASE | `TEMP_MAX`, `API_KEY` |
| Functions | snake_case | `send_alarm()`, `get_temperature()` |

---

## C++ (Firmware)

| Type | Format | Example |
|---|---|---|
| Files | snake_case | `main.cpp` |
| Variables | camelCase | `tempC`, `failedRequests` |
| Functions | camelCase | `connectWiFi()`, `sendToAPI()` |
| Constants | UPPER_CASE | `ONE_WIRE_BUS`, `TEMP_MAX` |
| Classes | PascalCase | `SensorManager` |

---

## Git Workflow

### Branch naming
Format:  KAN-{number}-{short-description}
Example: KAN-15-Dashboard-Chartjs
KAN-43-Temperature-GET-Endpoint

### Commit messages
Format:  [KAN-{number}]: {description}
Example: [KAN-43]: add GET endpoint for temperature readings
[KAN-44]: fix alarm email sent on every reading

### Pull Requests
- Title: `[KAN-{number}]: {description}`
- Fill out the PR template completely
- Link the Jira ticket in the description
- Never merge your own PR
- Only merge when CI is green ✅

### Commit types
| Type | When |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code restructuring |
| `test` | Adding or updating tests |
| `chore` | Dependencies, config, tooling |

---

## Adding Python Packages

**NEVER just run `pip install package` and forget!**

Always follow these steps:

```bash
# Step 1 — Add to requirements.in
echo "django-cors-headers" >> requirements.in

# Step 2 — Compile with pip-compile (inside venv!)
source venv/bin/activate
pip-compile requirements.in

# Step 3 — Install locally
pip install -r requirements.txt

# Step 4 — Commit both files
git add requirements.in requirements.txt
git commit -m "chore: add django-cors-headers"
```

**Why?**
- `requirements.in` = what you need (human readable)
- `requirements.txt` = exact versions (generated, never edit manually)
- GitHub Actions reads `requirements.txt` → missing package = CI fails
- Hetzner server reads `requirements.txt` → missing package = production down!

---

## API Endpoints

- Always lowercase
- Use hyphens: `/api/temperature-readings/`
- Always trailing slash
- Always document with docstrings

---

## Database

- Tables: snake_case → `temperature_reading`
- Columns: snake_case → `created_at`, `device_key`

---

## Constants & Magic Numbers

Never use magic strings or numbers directly in code.
All constants go in `constants.py` in the relevant app.

```python
# Wrong ❌
if status == 'ALARM_HIGH':
if temperature > 8.0:

# Correct ✅
if status == TemperatureStatus.ALARM_HIGH:
if temperature > TemperatureThreshold.MAX:
```

---

## Documentation

- Google Style docstrings for all functions and classes
- Sphinx for auto-generating documentation
- Every public function must have a docstring

```python
def send_alarm(self, device_key: str, temperature: float) -> None:
    """
    Sends an alarm email to the device owner.

    Args:
        device_key: The unique identifier of the device.
        temperature: The current temperature in Celsius.

    Returns:
        None
    """
```

---

## Questions?

Open a discussion in the GitHub repository or ask in the team chat.
If a convention is missing or unclear → update this document!