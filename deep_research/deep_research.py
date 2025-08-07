"""
A fun "deep research" task that Jacob Merizian created.
"""

import asyncio
from pathlib import Path

from anthropic import AsyncAnthropic
from inspect_ai import Task, eval_async, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import Score, Scorer, Target, accuracy, scorer
from inspect_ai.solver import TaskState, basic_agent
from inspect_ai.tool import bash, python, text_editor, web_browser
from inspect_ai.util import sandbox
from datetime import datetime
import fire  # type: ignore

MODEL = "anthropic/claude-sonnet-4-20250514"

INITIAL_PROMPT = """
You are assisting a user in creating a large literature review / report on a particular topic of interest (i.e. a "deep research").

The report should be thorough and should incorporate as many internet web pages as possible to satisfy the query.

This process will take a long time with a lot of back and forth with the web browser and/or any additional tools you may require, therefore you should make sure you have all the relevant details of the search query as possible before starting your search.

For now, here's the user's initial prompt. Please request any additional information or clarifications you think you need in order to go off and begin searching the internet to satisfy the search request.

Notes:
- Try not to ask more than 2-3 questions.
- Try to keep the questions relatively simple, such that a few words could answer it sufficiently.

<user_query>
{user_query}
</user_query>
""".strip()


DEEP_RESEARCH_PROMPT = """
You are assisting a user in creating a large literature review / report on a particular topic of interest (i.e. a "deep research").

The report should be thorough and should incorporate as many internet web pages as possible to satisfy the query.

Your final report should be saved to /report.md. Please use the text editor to create and edit this file. It has been created for you.

The information below is the user's query along with some follow ups taken. Please use this information to complete the task.

Notes:
- Your search should ideally be as thorough as possible, and you shouldn't be worried about continuing your research for a long time. Only end your search when you struggle to find relevant papers, and be persistent.
- You might at any point be stopped during your submission (due to response length limits), so you should make sure to continually update the report with your findings just in case. Try to keep a running copy of the report most of the time.
- You may create any other scratchpad files as necessary. But only report.md will be ultimately submitted.
- If exploring research, you should actually read the papers in your web browser and explore the citations.
- You should always include links to sources you find (not just citations, if you choose to include those). When including links, you should always format them using markdown syntax, as they otherwise won't be rendered properly.
- Don't include a table of contents, as one will be automatically generated for you.
- Only include a top-level markdown title (i.e. a single "#") at the top of the report and nowhere else.
- Avoid inflated language, and opt instead for a dry, factual tone of voice throughout your report.
- Don't arrive at your own conclusions. Everything you write in your report should be supported somewhere else.
- Once you believe your search to be complete, use the submit tool.

<user_query>
{user_query}
</user_query>
"""


ant = AsyncAnthropic()


async def _claude(prompt: str) -> str:
    output = await ant.messages.create(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        model=MODEL.split("/")[-1],
    )
    return output.content[0].text  # type: ignore


def _sanitize_string_for_filename(name: str) -> str:
    new_name = ""
    for c in name:
        if c in ["\\", "/"]:
            new_name += " "
        else:
            new_name += c
    return new_name


@scorer(metrics=[accuracy()])
def retrieve_report() -> Scorer:
    async def _scorer(state: TaskState, target: Target):
        report = await sandbox().read_file("report.md")
        return Score(
            value=1,
            answer=report,
        )

    return _scorer


@task
def deep_research_task(prompt: str):
    return Task(
        dataset=[
            Sample(
                DEEP_RESEARCH_PROMPT.format(user_query=prompt),
                files={"report.md": "# TODO"},
            )
        ],
        solver=basic_agent(
            tools=[
                text_editor(),
                # web_search(provider=["anthropic", "tavily"]),
                *web_browser(),
                python(60),
                bash(),
            ],
        ),
        scorer=[retrieve_report()],
        message_limit=200,
        sandbox="docker",
    )


async def main(existing_prompt: str | None = None, epochs: int = 1):
    if existing_prompt:
        with open(existing_prompt, "r") as f:
            full_query = f.read()
    else:
        print("Type your query below. Press CTRL-C twice to quit.")
        user_query = input(" > ")
        prompt = INITIAL_PROMPT.format(user_query=user_query)
        llm_follow_up = await _claude(prompt)
        print()
        print(llm_follow_up)
        print()
        print("Type your query below. Press CTRL-C twice to quit.")
        user_follow_up = input(" > ")
        full_query = f"User: {user_query}\n\nAssistant: {llm_follow_up}\n\nUser: {user_follow_up}".strip()

    current_year = datetime.now().year
    current_month = datetime.now().month
    current_day = datetime.now().day

    eval_logs = await eval_async(
        tasks=[deep_research_task(prompt=full_query)],
        model=MODEL,
        epochs=epochs,
        log_dir=f"logs/{current_year}/{current_month:02}/{current_day:02}",
    )
    num_epochs = len(eval_logs)
    for epoch_idx, eval_log in enumerate(eval_logs):
        # estimate cost:
        model_usage = eval_log.stats.model_usage[MODEL]
        input_price = 3
        output_price = 15
        cache_read_price = 0.30
        cache_write_price = 6
        cost = (
            model_usage.input_tokens / 1e6 * input_price
            + model_usage.output_tokens / 1e6 * output_price
            + (model_usage.input_tokens_cache_read or 0) / 1e6 * cache_read_price
            + (model_usage.input_tokens_cache_write or 0) / 1e6 * cache_write_price
        )
        total_tokens = (
            model_usage.input_tokens
            + model_usage.output_tokens
            + (model_usage.input_tokens_cache_read or 0)
            + (model_usage.input_tokens_cache_write or 0)
        )

        # Calculate elapsed time
        start = datetime.fromisoformat(eval_log.stats.started_at)
        end = datetime.fromisoformat(eval_log.stats.completed_at)
        elapsed_time = end - start
        minutes, seconds = divmod(elapsed_time.total_seconds(), 60)
        elapsed_str = f"{int(minutes)}m {int(seconds)}s"

        # pull out the report from the scorer:
        report: str = eval_log.samples[0].scores["retrieve_report"].answer  # type: ignore

        # add metadata to the report:
        current_date = datetime.now().strftime("%d %B %Y")
        metadata = f"*This report was generated using `{MODEL}` on {current_date}. It finished in {elapsed_str}, required approximately {total_tokens:0.2e} total tokens, and would have costed ${cost:.2f} to generate according to the public API pricing page.*\n"
        report += "\n\n---\n\n## Generation Info\n\n"
        report += metadata
        report = report.strip()

        # extract the title
        first_line = report.split("\n")[0]
        report_base_filename = _sanitize_string_for_filename(first_line.lstrip("# "))
        if num_epochs > 1:
            report_base_filename += f" (epoch {epoch_idx + 1})"
        while Path(f"reports/{report_base_filename}.md").exists():
            report_base_filename += " (new)"

        base_dir = Path(f"reports/{current_year}/{current_month:02}/{current_day:02}")

        base_dir.mkdir(exist_ok=True, parents=True)

        report_markdown_filename = base_dir / f"{report_base_filename}.md"
        report_pdf_filename = base_dir / f"{report_base_filename}.pdf"
        prompt_info_filename = base_dir / f"{report_base_filename} (prompts).txt"

        # write the markdown version
        with open(report_markdown_filename, "w") as f:
            f.write(report)

        # convert to pdf
        # markdown_to_pdf(str(report_markdown_filename), str(report_pdf_filename))

        # write the prompt info
        with open(prompt_info_filename, "w") as f:
            f.write(full_query)

        print(f"Created report '{report_pdf_filename}' :)")


def cli(existing_prompt: str | None = None, epochs: int = 1):
    asyncio.run(main(existing_prompt=existing_prompt, epochs=epochs))


if __name__ == "__main__":
    fire.Fire(cli)
