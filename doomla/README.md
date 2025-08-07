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

Clone doomla repository:

```
cd ~
git clone https://github.com/UKGovernmentBEIS/doomla.git
```

Install dependencies

```
poetry install
```

## Understand the code

- Read through the guide in: https://inspect.cyber.aisi.org.uk/doomla.html
- Explore the code to confirm your understanding
  - Can you tell which part belong to Inspect / Inspect Cyber?
  - And which is the core infra you have to build regardless of the eval
    framework?
- Run the "solution" variant with 10k tokens limit
  - (i.e., update `task.py` and then `python task.py`)
  * Remember to set up model provider
- View the transcript with `inspect view --log-dir ./logs`
- Run the "example" variant with 50k tokens limit
  - Here is an example task.py: [commit #2c8b582e](https://github.com/vhong-aisi/doomla/commit/2c8b582e)
  - This takes a while though. So, (hopefully) I have some traces ready for ya.
- Review the transcript and see where the model failed.

## Extras

If you have extra time, there are a few things you can do:

- Check out [inspect_evals/cybench](https://github.com/UKGovernmentBEIS/inspect_evals/tree/main/src/inspect_evals/cybench) for many more examples
- Try to solve this range yourself by using the [human agent](https://inspect.aisi.org.uk/human-agent.html)
  - Example task.py: [commit #85c232ecf](https://github.com/vhong-aisi/doomla/commit/85c232ecf)
  - Run `python task.py`, then use the `docker exec` command to login to the container.
- Add more variants with different hints to see if you can nudge the model along
- Modify the range to your liking (e.g., removing a host)
