from typing import Any
from inspect_ai import Task, task
from inspect_ai.dataset import Sample, hf_dataset
from inspect_ai.solver import multiple_choice
from inspect_ai.scorer import choice


def record_to_sample_mmlu(record: dict[str, Any]) -> Sample:
    return Sample(
        input=record["question"],
        choices=record["choices"],
        # converts 0 -> A, 1 -> B, etc.
        target=("ABCD"[record["answer"]]),
        metadata={"subject": record["subject"]},
    )


@task
def mmlu():
    dataset = hf_dataset(
        path="cais/mmlu",
        name="all",
        split="dev",
        sample_fields=record_to_sample_mmlu,
        shuffle=True,
    )

    return Task(
        dataset=dataset,
        solver=multiple_choice(),
        scorer=choice(),
    )
