## Overview

For this exercise, we'll try to create a cyber range evaluation called [Doomla](https://inspect.cyber.aisi.org.uk/doomla.html).

## Before you start

Before you start:

- You'll need an API key to run the eval.
  - If you don't have one, you can sign up for Google AI Studio:
    https://ai.google.dev/gemini-api/docs/pricing#gemini-1.5-flash
  - I tried using model `google/gemini-1.5-flash` and it was able to use the
    bash tool to call the solution script. Not sure if it'd work without the
    hints though.
  - Follow https://inspect.aisi.org.uk/providers.html to configure your model
    provider (i.e., `pip install X` and `export X_API_KEY=...`)
- **Always set a limit (e.g., max_tokens)** when running evals.
  - What this means is that `eval(doomla, model="openai/gpt-4o")` should
    really be `eval(doomla, model="openai/gpt-4o, max_tokens=10_000)` or a
    higher token value.
  - This range is not that easy so I expect non-frontier models might struggle
    with the "example" variant even with 1-2M tokens.

## Setup

Create a new directory:

```
mkdir ~/doomla
cd ~/doomla
```

Setup dependencies

```
python -m venv .venv
source ./venv/bin/activate
```

```
pip install "inspect-ai>=0.3.86,<0.4.0" "inspect-cyber>=0.1.0,<0.2.0"
```

## Create the range

Follow the instructions in: https://inspect.cyber.aisi.org.uk/doomla.html

Here is the expected directory structure:

```
├── evals
│   └── doomla
│       ├── compose.yaml
│       ├── eval.yaml
│       ├── images
│       │   ├── joomla
│       │   │   ├── Dockerfile
│       │   │   └── custom-entrypoint.sh
│       │   ├── mysql-setup
│       │   │   ├── Dockerfile
│       │   │   └── setup-script.sh
│       │   ├── vpn
│       │   │   ├── Dockerfile
│       │   │   └── authorized_keys
│       │   └── workstation
│       │       ├── Dockerfile
│       │       └── root
│       ├── resources
│       │   └── flag.txt
│       └── solution
│           └── solution.sh
├── images
│   └── agent
│       └── Dockerfile
└── task.py
```

## Wrapping up

- If you finish early, consider:
  - add more variants with various level of hints to identify the bottleneck
  - add extra hosts to the range
  - use model graded scorer to perform automatic transcript analysis
