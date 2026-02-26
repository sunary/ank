# ANK Examples

## Prerequisites

```bash
pip install ank
```

## Examples

### streaming_app

Pipeline with Join/Split and branching (Odd/Even).

**Requirements:** Redis running on localhost:6379

```bash
cd examples/streaming_app
ank run -fs settings.yml
```

### api_app

REST API with MongoDB storage.

**Requirements:** MongoDB running on localhost:27017

```bash
cd examples/api_app
ank run -fs settings.yml
```

Endpoints:
- `GET /api/add?a=1&b=2`
- `GET /api/sub?a=10&b=5`

### schedule_app

Scheduled task using cron format.

```bash
cd examples/schedule_app
ank run -fs settings.yml
```

Runs every Friday at midnight (or immediately if `start_now: true`).

## Verification

Run from project root:

```bash
python3 examples/verify_examples.py
```
