from datetime import datetime, timezone
from laoshu.baml_client.types import PublicationTime
from laoshu.checks.freshness import FreshnessCheck
import asyncio


class FreshnessCheckWithMocks(FreshnessCheck):
    def __init__(self, returned_publication_time: PublicationTime):
        self.returned_publication_time = returned_publication_time

    async def _check_freshness(self, _: str) -> PublicationTime:
        return self.returned_publication_time

    def _today(self) -> datetime:
        return datetime(2024, 1, 10).replace(tzinfo=timezone.utc)


def test_return_no_publication_date() -> None:
    publication_time = PublicationTime(
        reasoning="",
        is_in_the_text=False,
        year=0,
        month=0,
        day=0,
    )
    object_under_test = FreshnessCheckWithMocks(publication_time)
    result = asyncio.run(object_under_test.check_freshness("markdown"))
    assert result.publication_date_iso8601 is None
    assert result.relative_to_now is None


def test_return_publication_date_today() -> None:
    publication_time = PublicationTime(
        reasoning="",
        is_in_the_text=True,
        year=2024,
        month=1,
        day=10,
    )
    object_under_test = FreshnessCheckWithMocks(publication_time)
    result = asyncio.run(object_under_test.check_freshness("markdown"))
    assert result.publication_date_iso8601 == "2024-01-10"
    assert result.relative_to_now == "today"


def test_return_publication_date_yesterday() -> None:
    publication_time = PublicationTime(
        reasoning="",
        is_in_the_text=True,
        year=2024,
        month=1,
        day=9,
    )
    object_under_test = FreshnessCheckWithMocks(publication_time)
    result = asyncio.run(object_under_test.check_freshness("markdown"))
    assert result.publication_date_iso8601 == "2024-01-09"
    assert result.relative_to_now == "yesterday"


def test_return_publication_date_same_month() -> None:
    publication_time = PublicationTime(
        reasoning="",
        is_in_the_text=True,
        year=2024,
        month=1,
        day=5,
    )
    object_under_test = FreshnessCheckWithMocks(publication_time)
    result = asyncio.run(object_under_test.check_freshness("markdown"))
    assert result.publication_date_iso8601 == "2024-01-05"
    assert result.relative_to_now == "5 days ago"


def test_return_publication_date_last_month() -> None:
    publication_time = PublicationTime(
        reasoning="",
        is_in_the_text=True,
        year=2023,
        month=12,
        day=5,
    )
    object_under_test = FreshnessCheckWithMocks(publication_time)
    result = asyncio.run(object_under_test.check_freshness("markdown"))
    assert result.publication_date_iso8601 == "2023-12-05"
    assert result.relative_to_now == "1 month ago"


def test_return_publication_date_few_months_ago() -> None:
    publication_time = PublicationTime(
        reasoning="",
        is_in_the_text=True,
        year=2023,
        month=11,
        day=5,
    )
    object_under_test = FreshnessCheckWithMocks(publication_time)
    result = asyncio.run(object_under_test.check_freshness("markdown"))
    assert result.publication_date_iso8601 == "2023-11-05"
    assert result.relative_to_now == "2 months ago"


def test_return_publication_date_last_year() -> None:
    publication_time = PublicationTime(
        reasoning="",
        is_in_the_text=True,
        year=2022,
        month=12,
        day=5,
    )
    object_under_test = FreshnessCheckWithMocks(publication_time)
    result = asyncio.run(object_under_test.check_freshness("markdown"))
    assert result.publication_date_iso8601 == "2022-12-05"
    assert result.relative_to_now == "1 year ago"


def test_return_publication_date_few_years_ago() -> None:
    publication_time = PublicationTime(
        reasoning="",
        is_in_the_text=True,
        year=2021,
        month=12,
        day=5,
    )
    object_under_test = FreshnessCheckWithMocks(publication_time)
    result = asyncio.run(object_under_test.check_freshness("markdown"))
    assert result.publication_date_iso8601 == "2021-12-05"
    assert result.relative_to_now == "2 years ago"
