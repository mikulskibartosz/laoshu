import asyncio
import click
from typing import List
from rich.console import Console
from rich.table import Table
from laoshu.config.logger import setup_logger
from laoshu.verification.verification import (
    verify_citations_in_file,
    VerificationResult,
)


@click.group()
def main() -> None:
    pass


@main.command("check")
@click.option("--file", "file_path", type=click.Path(exists=True), required=True)
@click.option("--onlyincorrect", "only_incorrect", is_flag=True, default=False)
def check_file(file_path: str, only_incorrect: bool) -> None:
    results = asyncio.run(verify_citations_in_file(file_path))
    __show_results(results, only_incorrect)


@main.command("web")
@click.option("--host", "host", type=str, default="0.0.0.0")
@click.option("--port", "port", type=int, default=8000)
def web(host: str, port: int) -> None:
    import uvicorn
    from laoshu.api.api import app

    uvicorn.run(app, host=host, port=port)


def __show_results(results: List[VerificationResult], only_incorrect: bool) -> None:
    console = Console()

    table = Table(
        show_header=True, header_style="bold magenta", title="Verification Results"
    )
    table.add_column("Claim")
    table.add_column("Sources")
    table.add_column("Is based on provided sources?")

    for result in results:
        if only_incorrect and result.is_correct:
            continue
        table.add_row(
            result.claim,
            ", ".join(result.sources),
            "Yes" if result.is_correct else "No",
        )

    console.print(table)


if __name__ == "__main__":
    setup_logger()
    main()
