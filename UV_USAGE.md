# Using `uv` for Dependency Management

## Overview

This project uses **`uv`** (by Astral) for Python dependency management. **Always use `uv`, never use `pip` directly.**

## Why `uv`?

- **Fast**: 10-100x faster than pip
- **Reliable**: Deterministic dependency resolution
- **Modern**: Python packaging done right
- **Compatible**: Works with existing requirements.txt
- **Simple**: Easy to use, single tool for everything

## Installation

### One-Time Setup

```bash
# Install uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Restart your terminal or:
source ~/.bashrc  # or ~/.zshrc
```

### Verify Installation

```bash
uv --version
# Should show: uv 0.x.x
```

## Daily Usage

### Install/Update Dependencies

Instead of `pip install -r requirements.txt`:
```bash
cd backend
uv sync
```

This:
- Creates `.venv/` virtual environment automatically
- Installs all dependencies from `requirements.txt`
- Locks versions for reproducibility

### Run Management Commands

Instead of `python manage.py <command>`:
```bash
uv run python manage.py migrate
uv run python manage.py runserver 8000
uv run python manage.py seed_cards
uv run python manage.py createsuperuser
uv run python manage.py test
```

### Add New Dependencies

Instead of `pip install <package>`:
```bash
uv pip install <package>
# Then update requirements.txt:
uv pip freeze > requirements.txt
```

### Run Python Scripts

Instead of `python script.py`:
```bash
uv run python script.py
```

## How It Works

1. **`uv sync`**: Reads `requirements.txt` or `pyproject.toml`, creates/updates `.venv/`
2. **`uv run`**: Automatically activates the virtual environment and runs your command
3. **No manual activation needed**: `uv run` handles it for you

## Virtual Environment

`uv` creates `.venv/` in your project directory:

```
backend/
├── .venv/          # Created by uv sync
│   ├── bin/
│   └── lib/
├── requirements.txt
└── manage.py
```

**You don't need to activate it manually** - `uv run` does it automatically.

## Common Commands Cheatsheet

| Old (pip) | New (uv) |
|-----------|----------|
| `pip install -r requirements.txt` | `uv sync` |
| `source venv/bin/activate && python manage.py runserver` | `uv run python manage.py runserver` |
| `python manage.py migrate` | `uv run python manage.py migrate` |
| `pip install django` | `uv pip install django` |
| `pip freeze > requirements.txt` | `uv pip freeze > requirements.txt` |

## Deployment Note

**For local development**: Always use `uv`

**For production (Render)**: The `build.sh` script installs `uv` automatically and uses it for deployment

## Troubleshooting

### "uv: command not found"

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Restart terminal or source your profile
source ~/.bashrc  # or ~/.zshrc
```

### Need to use a different Python version?

```bash
uv python install 3.12  # Install Python 3.12
uv venv --python 3.12   # Create venv with specific version
```

### Want to manually activate venv?

You can, but you don't need to:
```bash
source .venv/bin/activate  # Unix
.venv\Scripts\activate     # Windows
```

## Benefits Summary

✅ **Faster**: Install dependencies 10-100x faster
✅ **Simpler**: No manual virtual environment activation
✅ **Consistent**: Everyone on the team uses the same versions
✅ **Modern**: Best practices built-in
✅ **Compatible**: Works with existing Python ecosystem

## Learn More

- [uv Documentation](https://github.com/astral-sh/uv)
- [uv vs pip Comparison](https://github.com/astral-sh/uv#highlights)

---

**Remember: Always use `uv`, never `pip` directly!** 🚀
