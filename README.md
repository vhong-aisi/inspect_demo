# inspect_demo

Demo repository for Inspect AI presentation in Vegas 2025

# Installation

```
uv sync
```

Then activate the virtual environment. Otherwise, you'll need to prepend `uv run` to the commands below:

```
source .venv/bin/activate
```

# Commands

## Run MMLU evals

Run MMLU eval:

```
inspect eval mmlu.py --model openai/gpt-4
```

Run MMLU eval with eval-set command:

```
inspect eval-set mmlu.py --model openai/gpt-4 \
--max-connections 20 \
--token-limit 2000 \
--epochs 5
```

## View logs

```
inspect view --log-dir assets/
```

## Run the example analysis notebook

```
jupyter notebook
```

Then connect to http://localhost:8888 and open to `analysis.ipynb`.
