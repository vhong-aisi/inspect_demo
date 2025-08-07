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

## Run bomb evals

We use the python eval call, so simply run the script.

```
python single_turn/bomb.py
```

## Following Doomla tutorial (cyber range)

Check out [./doomla/README.md](./doomla/README.md)

## View logs

```
inspect view --log-dir assets/
```

## View example notebooks

```
jupyter notebook
```

Then connect to http://localhost:8888 and open the `.ipynb` files
