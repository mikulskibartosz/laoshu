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
    """Laoshu.ai - Citation verification tool.

    Laoshu.ai is released under the GNU Affero General Public License v3.0. Commercial entities wishing to use it under a different license should contact me. (https://mikulskibartosz.name)
    """
    pass


@main.command("check")
@click.option("--file", "file_path", type=click.Path(exists=True), required=True)
@click.option("--onlyincorrect", "only_incorrect", is_flag=True, default=False)
def check_file(file_path: str, only_incorrect: bool) -> None:
    """Check citations in a file.

    Laoshu.ai is released under the GNU Affero General Public License v3.0. Commercial entities wishing to use it under a different license should contact me. (https://mikulskibartosz.name)
    """
    results = asyncio.run(verify_citations_in_file(file_path))
    __show_results(results, only_incorrect)


@main.command("web")
@click.option("--host", "host", type=str, default="0.0.0.0")
@click.option("--port", "port", type=int, default=8000)
def web(host: str, port: int) -> None:
    """Start the web server.

    Laoshu.ai is released under the GNU Affero General Public License v3.0. Commercial entities wishing to use it under a different license should contact me. (https://mikulskibartosz.name)
    """
    import uvicorn
    from laoshu.api.api import app

    uvicorn.run(app, host=host, port=port)


def __show_results(results: List[VerificationResult], only_incorrect: bool) -> None:
    console = Console()

    table = Table(
        show_header=True,
        header_style="bold magenta",
        title="Verification Results",
        show_lines=True,
    )
    table.add_column("Claim")
    table.add_column("Sources")
    table.add_column("Is based on provided sources?")

    for result in results:
        if only_incorrect and all(source.is_correct for source in result.sources):
            continue

        first_source = result.sources[0].source
        first_is_correct = result.sources[0].is_correct

        table.add_row(
            result.claim,
            first_source,
            "Yes" if first_is_correct else "No",
        )

        for source in result.sources[1:]:
            table.add_row(
                "↑",
                source.source,
                "Yes" if source.is_correct else "No",
            )

    console.print(table)


if __name__ == "__main__":
    setup_logger()
    main()
