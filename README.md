# inspect_demo

Demo repository for Inspect AI presentation in Vegas 2025

# Installation

### Install dependencies

```
uv sync --locked
```

### Activate venv

Then activate the virtual environment. Otherwise, you'll need to prepend `uv run` to the commands below:

```
source .venv/bin/activate
```

### Setup API keys

Set up your model provider auth (e.g., OpenAI):

```
export OPENAI_API_KEY=your-openai-api-key
```

For other providers, see https://inspect.aisi.org.uk/providers.html

# Commands

## Run MMLU evals

Run MMLU eval:

```
inspect eval single_turn/mmlu.py --model openai/gpt-4
```

Run MMLU eval with eval-set command:

```
inspect eval-set single_turn/mmlu.py --model openai/gpt-4 \
--max-connections 20 \
--token-limit 2000 \
--epochs 5
```

## View logs

```
inspect view --log-dir assets/
```

## View example notebook for MMLU

```
jupyter notebook
```

Then connect to http://localhost:8888 and open to `single_turn/analysis.ipynb`.
