# ANK - Python streaming system
# Build: docker build -t ank .
# Run:   docker run --rm -v $(pwd):/workspace -w /workspace ank create MyApp

FROM python:3.11-alpine

LABEL maintainer="Sunary <v2nhat@gmail.com>"
LABEL description="ANK - Python streaming system for pipelines, REST APIs, and message queues"

# Build deps for Python packages (pyzmq, cryptography, etc.)
RUN apk --no-cache add gcc python3-dev libffi-dev openssl-dev zeromq-dev libpq-dev git

WORKDIR /app

# Copy and install ank
COPY requirements.txt setup.py README.md LICENSE CHANGES.md ./
COPY ank ./ank

RUN pip install --no-cache-dir .

WORKDIR /workspace
ENTRYPOINT ["ank"]
CMD ["--help"]
