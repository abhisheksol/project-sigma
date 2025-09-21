# Sigma Django Backend

A Django backend application configured for development, featuring REST API support, PostgreSQL integration, Swagger documentation, and code linting/formatting using `pre-commit`.

---

## 📁 Project Structure Overview

- **Django Backend**: REST API with Django + DRF.
- **Database**: PostgreSQL
- **Environment Handling**: Managed using `.env` file and `python-decouple`.
- **Documentation**: Swagger UI via `drf-yasg`.
- **Pre-commit Hooks**: Ensures code quality and consistency.

---

## 🚀 Getting Started

### 1. Clone the Repository

```
🛠️ Requirements & Installation
Python Version
Python 3.9 recommended (for compatibility with pre-commit hooks and Black).

Create a Virtual Environment



python3.9 -m venv venv
source venv/bin/activate
Install Dependencies



pip install -r requirements.txt
🔐 Environment Variables
Create a .env file in the root directory with the following content:

ini


# Secret Key
SECRET_KEY = "django-insecure-*4rz(85k3f^j0fs@(z@s2!f=-o9#02z)#$+(^g8tbvqa2(#3_("

# Database Config
DB_NAME = "APTAGRIM_POSTGRES"
DB_USER = "aptagrim"
DB_PASSWORD = "Abcd.1234"
DB_HOST = "localhost"
DB_PORT = "9051"
ENGINE = 'django.db.backends.postgresql'

# Server Type
SERVER_TYPE = "DEV"

# Swagger Config
SWAGGER_TITLE = "Sigma Django Backend"
SWAGGER_API_VERSION = "V1"
SWAGGER_DESCRIPTION = "Sigma Django Backend swagger documentation"
SWAGGER_TERMS_OF_SERVICE = "https://www.example.com/terms/"
SWAGGER_CONTACT_EMAIL = "example@demo.com"
SWAGGER_LICENSE = "BSD License"
⚠️ Note: Never expose sensitive credentials in production repositories. Use .env and .gitignore appropriately.

⚙️ Pre-commit Configuration
This project uses pre-commit to enforce code quality and standards before committing.

Setup Pre-commit

pip install pre-commit
pre-commit install
Run All Hooks Manually


pre-commit run --all-files
Active Hooks
YAML & JSON checks:

check-yaml

end-of-file-fixer

trailing-whitespace

pretty-format-json

Code Formatting:

black (Python code formatter)

Code Cleanup:

autoflake (removes unused imports/variables)

Custom Hooks:

check-variable-naming (enforces custom variable naming rules)

delete-empty-files (removes empty Python files)

Local hooks are defined in:
core_utils/pre_commit/precommit_check_variable_naming.py
core_utils/pre_commit/delete_empty_files.py

```
