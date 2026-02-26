# ANK Tests

## Prerequisites

Install ank and dependencies first:

```bash
pip install -e .
```

## Running Tests

From project root:

```bash
python -m unittest discover -s ank/tests -p 'test_*.py' -v
```

Or from ank/tests directory:

```bash
cd ank/tests
python -m unittest test_deploy -v
```

## Test Structure

- **test_deploy.py** – Integration tests for ProgramLoader, GenerateProcessor, GenerateSetting
- **processor.py** – Test processor classes (FirstApp, ConditionalApp, etc.) used by test_deploy
- **services.yml** – Service definitions for tests
- **settings.yml** – Test parameters (range_from, range_to, batch_size)

## Notes

- Tests run from `ank/tests/` directory (setUp changes cwd)
- `test_program_loader` executes the full pipeline (FirstApp → JoinApp → SplitApp → etc.)
- Generated files (`_processor.py`, `_settings.yml`) are written to ank/tests/ and gitignored
