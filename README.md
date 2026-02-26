# ANK

Python streaming system for building pipelines with REST APIs, scheduled tasks, and message queues (RabbitMQ, ZeroMQ, Kafka).

## Overview

ANK lets you compose processors into chains and pipelines. Each processor is a link in the chain; connect them to form data flows.

**Features:**
- Pipeline and streaming processing
- REST API interface (Flask)
- Scheduled tasks (cron-style)
- Message queues: RabbitMQ, ZeroMQ, Kafka, Redis

## Use Cases

| Use Case | Description |
|----------|-------------|
| **ETL pipelines** | Extract, transform, load data between systems (DB → queue → API) |
| **Event processing** | Consume events from Kafka/RabbitMQ, process, and forward |
| **API backends** | REST endpoints that trigger pipelines or queue operations |
| **Scheduled jobs** | Cron-style tasks (reports, cleanup, sync) |
| **Batch processing** | Join multiple messages, process in batches, split results |
| **Microservice glue** | Connect services via queues without heavy orchestration |
| **Data transformation** | Chain processors for validation, enrichment, formatting |

## Similar Projects

| Project | Focus | When to prefer |
|---------|-------|----------------|
| **Celery** | Distributed task queue, async workers | Complex async tasks, retries, rate limiting |
| **Luigi** | Data pipelines, dependency graphs | DAGs, file-based workflows, Hadoop/Spark |
| **Apache Airflow** | Workflow orchestration | Complex DAGs, scheduling, monitoring UI |
| **Prefect** | Modern workflow | Cloud-native, observability, dynamic flows |
| **Kafka Streams** | Stream processing (JVM) | High-throughput, exactly-once, stateful streams |
| **ANK** | Lightweight pipelines, queues, REST | Simple chains, minimal setup, YAML config |

## Requirements

- Python 3.10+

## Installation

**From PyPI:**
```bash
pip install ank
```

**From Docker** (no local Python required):
```bash
# Build from source
git clone git@github.com:sunary/ank.git
cd ank
docker build -t ank .

# Or pull from Docker Hub (when published)
# docker pull sunary/ank
```

**From source:**
```bash
git clone git@github.com:sunary/ank.git
cd ank
pip install -e .
```

## Quick Start

### 1. Create a new service

**With ank installed (pip/Docker):**
```bash
ank create TestService
# or with app type:
ank create TestService -c APIApp
cd TestService
```

**With Docker only** (no local install):
```bash
docker run --rm -v $(pwd):/workspace -w /workspace ank create TestService
cd TestService
```

App types: `BaseApp` (pipeline, default), `APIApp` (REST API), `ScheduleApp` (cron-based).

### 2. Define your processor

Edit `processor.py`:

```python
from ank.components.pipe_app import PipeApp

class ExampleApp(PipeApp):

    def start(self):
        for i in range(100):
            self.chain_process({'content': i})

    def process(self, message=None):
        return message['content'] + 1
```

### 3. Configure services and chains

Edit `services.yml` to wire processors and dependencies:

```yaml
services:
  StartApp:
    class: processor.StartApp
    arguments: [$Redis, '%batch_size%']

  Redis:
    class: redis.Redis
    arguments: ['%redis_host%', '%redis_port%']

  LogApp:
    class: ank.components.log_app.LogApp
    arguments: ~

chains:
  - StartApp
  - LogApp
```

### 4. Configure settings

Edit `settings.yml` with your parameters:

```yaml
parameters:
  redis_host: localhost
  redis_port: 6379
  batch_size: 100
```

### 5. Run

```bash
ank run -fs settings.yml
```

Or programmatically:

```python
from ank.program_loader import main
main(file_setting='settings.yml')
```

## Chain Models

| Pattern | Description |
|---------|-------------|
| **1–1** | Single processor → single processor |
| **1–n** | One processor → multiple branching processors |
| **n–1** | Multiple processors → merge into one |
| **n–n** | Multiple processors → multiple processors |
| **Join** | Combine messages: `[msg1, msg2, msg3]` |
| **Split** | Split message into multiple messages |

### Branching with `flags`

For branching processors, return a message with a `flags` key to control routing:

```python
def process(self, message=None):
    return {
        'content': result,
        'flags': [True, False]  # Process 1st branch only
    }
```

- `[True, True]` → process both branches
- `[True, False]` → process 1st branch only
- `[False, True]` → process 2nd branch only
- `[False, False]` → stop chain

## Base Apps

| App | Description |
|-----|-------------|
| **PipeApp** | Base pipeline processor |
| **APIApp** | REST API interface (Flask) |
| **ScheduleApp** | Scheduled tasks (cron format) |

## Component Apps

| Component | Description |
|-----------|-------------|
| **LogApp** | Log every message |
| **JoinApp** | Join multiple messages into one |
| **SplitApp** | Split message into multiple |
| **\*Consumer** | Consume from queue (Redis, Kafka, RabbitMQ, ZMQ) |
| **\*Producer** | Produce to queue |

## CLI Reference

| Command | Description |
|---------|-------------|
| `ank create <name> [-c BaseApp\|APIApp\|ScheduleApp]` | Create new service |
| `ank gen_setting -fs _setting.yml` | Generate settings template |
| `ank gen_processor -fs settings.yml` | Generate processor from settings |
| `ank run -fs settings.yml` | Run service |
| `ank run -d` | Run as daemon (background) |
| `ank test` | Run tests |
| `ank build` | Build Docker image |

## Configuration

### services.yml syntax

```yaml
services:
  ServiceName:
    class: module.ClassName
    arguments: [$OtherService, '%param%']  # ~ for no args

chains:
  - Service1
  - Service2
  - [BranchA, BranchB]  # branching
```

- `$Service` — inject another service
- `%param%` — value from `settings.yml`

### settings.yml

Parameters referenced in `services.yml` are read from `settings.yml`. Use `ank gen_setting` to create a template.

## Examples

See the `examples/` directory:

- `streaming_app/` — pipeline with Join/Split
- `api_app/` — REST API
- `schedule_app/` — scheduled tasks

## Docker

### Run ANK via Docker

Use ank without installing Python locally:

```bash
# Create new app (output in current directory)
docker run --rm -v $(pwd):/workspace -w /workspace ank create MyApp

# Run a service
docker run --rm -v $(pwd):/workspace -w /workspace ank run -fs settings.yml

# Generate settings
docker run --rm -v $(pwd):/workspace -w /workspace ank gen_setting -fs _setting.yml
```

### Build your app's Docker image

From your project directory (after `ank create`):

```bash
ank build
docker run --entrypoint /bin/sh <image_id>
```

## License

See [LICENSE](LICENSE).
