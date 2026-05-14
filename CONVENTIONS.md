# ColdGuard — Naming Conventions & Standards

## General Rules
- Language: English (code, comments, commits)
- Everything lowercase unless specified below

## Python (Backend)
| Type | Format | Example |
|---|---|---|
| Files | snake_case | `models.py`, `views.py` |
| Variables | snake_case | `temp_reading`, `device_key` |
| Classes | PascalCase | `TemperatureReading`, `Device` |
| Constants | UPPER_CASE | `TEMP_MAX`, `API_KEY` |
| Functions | snake_case | `send_alarm()`, `get_temperature()` |

## C++ (Firmware)
| Type | Format | Example |
|---|---|---|
| Files | snake_case | `main.cpp` |
| Variables | camelCase | `tempC`, `failedRequests` |
| Functions | camelCase | `connectWiFi()`, `sendToAPI()` |
| Constants | UPPER_CASE | `ONE_WIRE_BUS`, `TEMP_MAX` |
| Classes | PascalCase | `SensorManager` |

## Git
| Type | Format | Example |
|---|---|---|
| Branches | kebab-case | `feature/temperature-api` |
| Commits | Conventional | `feat: add temperature endpoint` |

## Commit Types
- feat: new feature
- fix: bug fix
- docs: documentation
- refactor: code refactoring
- test: adding tests

## API Endpoints
- Always lowercase
- kebab-case: `/api/temperature-readings/`
- Always trailing slash

## Database
- Tables: snake_case → `temperature_reading`
- Columns: snake_case → `created_at`, `device_key`

### Branches
Git format:  KAN-{number}-{description}
PR title:    [KAN-{number}]: {description}

Example:
- Branch: KAN-13-Django-Setup
- PR:     [KAN-13]: Django-Setup

## Language
- Code: English
- Comments: English  
- Commit messages: English
- Branch names: English
- PR titles: English
- Variable names: English
- Documentation: English

## Constants & Magic Numbers

- Never use magic strings or magic numbers directly in code
- All constants go in constants.py in the relevant app
- Use descriptive class names: TemperatureStatus, TemperatureThreshold
- Example:
  
  # Wrong:
  if status == 'ALARM_HIGH':
  if temperature > 8.0:
  
  # Correct:
  if status == TemperatureStatus.ALARM_HIGH:
  if temperature > TemperatureThreshold.MAX: