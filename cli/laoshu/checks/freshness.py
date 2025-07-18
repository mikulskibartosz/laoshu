from laoshu.baml_client.types import PublicationTime
from laoshu.baml_client import b
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass
from typing import Optional


@dataclass
class FreshnessCheckResult:
    publication_date_iso8601: Optional[str]
    relative_to_now: Optional[str]


class FreshnessCheck:
    async def check_freshness(self, source_markdown: str) -> FreshnessCheckResult:
        publication_time = await self._check_freshness(source_markdown)
        if not publication_time.is_in_the_text:
            return FreshnessCheckResult(
                publication_date_iso8601=None, relative_to_now=None
            )

        publication_date = datetime(
            year=publication_time.year,
            month=publication_time.month,
            day=publication_time.day,
        )

        # Assume timezone UTC for publication_date
        publication_date = publication_date.replace(tzinfo=timezone.utc)
        delta = self._today() - publication_date
        relative_to_now = self._get_relative_to_now(delta)

        return FreshnessCheckResult(
            publication_date_iso8601=publication_date.strftime("%Y-%m-%d"),
            relative_to_now=relative_to_now,
        )

    async def _check_freshness(self, source_markdown: str) -> PublicationTime:
        return await b.GetPublicationTime(source_markdown)

    def _today(self) -> datetime:
        return datetime.now(timezone.utc)

    def _get_relative_to_now(self, delta: timedelta) -> str:
        days = delta.days
        if days < 30:
            if days == 0:
                relative_to_now = "today"
            elif days == 1:
                relative_to_now = "yesterday"
            else:
                relative_to_now = f"{days} days ago"
        elif days < 365:
            months = days // 30
            if months == 1:
                relative_to_now = "1 month ago"
            else:
                relative_to_now = f"{months} months ago"
        else:
            years = days // 365
            if years == 1:
                relative_to_now = "1 year ago"
            else:
                relative_to_now = f"{years} years ago"
        return relative_to_now
