import asyncio
import click
from typing import List
from rich.console import Console
from rich.table import Table
from laoshu.verification.verification import (
    verify_citations_in_file,
    VerificationResult,
)


@click.group()
def main() -> None:
    pass


@main.command()
@click.argument("file", type=click.Path(exists=True))
def check_file(file: str) -> None:
    results = asyncio.run(verify_citations_in_file(file))
    __show_results(results)


def __show_results(results: List[VerificationResult]) -> None:
    console = Console()

    table = Table(
        show_header=True, header_style="bold magenta", title="Verification Results"
    )
    table.add_column("Claim")
    table.add_column("Sources")
    table.add_column("Is Correct")
    table.add_column("Reasoning")

    for result in results:
        table.add_row(
            result.claim,
            ", ".join(result.sources),
            "Yes" if result.is_correct else "No",
            result.reasoning,
        )

    console.print(table)


if __name__ == "__main__":
    main()
