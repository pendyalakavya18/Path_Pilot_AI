"""
roadmap_agent.py — Roadmap Monitoring & Adaptation Agent

Detects when a student is falling behind schedule and adapts the roadmap:
  - Compresses remaining topics
  - Increases hours_per_day
  - Adds revision sessions for failed tests
  - Returns updated weekly_plan JSON
"""

from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.roadmap import Roadmap


class RoadmapAgent:

    async def adapt(self, roadmap: "Roadmap") -> list[dict]:
        """
        Smart adaptation of remaining weeks based on current progress.
        Returns updated weekly_plan.
        """
        plan: list[dict] = list(roadmap.weekly_plan or [])
        completed_week = roadmap.current_week
        total_weeks = roadmap.total_weeks

        if not plan:
            return plan

        # How many weeks behind are we?
        days_since_start = (datetime.now(timezone.utc) - roadmap.created_at.replace(tzinfo=timezone.utc)).days
        expected_week = min(days_since_start // 7, total_weeks)
        weeks_behind = max(0, expected_week - completed_week)

        if weeks_behind <= 1:
            return plan  # On track, no changes needed

        # Remaining weeks in plan
        remaining = [w for w in plan if w.get("week", 0) > completed_week]

        if not remaining:
            return plan

        # Intensity boost: increase hours_per_day proportionally
        intensity_multiplier = 1 + (weeks_behind / max(len(remaining), 1)) * 0.4

        for week in remaining:
            base_hours = week.get("hours_per_day", 2)
            week["hours_per_day"] = min(round(base_hours * intensity_multiplier, 1), 6.0)
            week["adapted"] = True
            week["note"] = f"Schedule compressed — you are {weeks_behind} week(s) behind. Increase daily study time."

        # If very far behind (3+ weeks), merge some topic-light weeks
        if weeks_behind >= 3 and len(remaining) >= 2:
            merged = self._merge_light_weeks(remaining)
            # Replace remaining weeks in full plan
            completed_plan = [w for w in plan if w.get("week", 0) <= completed_week]
            plan = completed_plan + merged

        return plan

    def _merge_light_weeks(self, weeks: list[dict]) -> list[dict]:
        """Merge consecutive weeks that have fewer than 3 topics into one."""
        merged = []
        i = 0
        while i < len(weeks):
            current = weeks[i]
            topics = current.get("topics", [])
            if len(topics) < 3 and i + 1 < len(weeks):
                next_week = weeks[i + 1]
                combined_topics = topics + next_week.get("topics", [])
                merged.append({
                    **current,
                    "topics": combined_topics[:6],  # max 6 per week
                    "theme": f"{current.get('theme','')} + {next_week.get('theme','')}",
                    "merged": True,
                })
                i += 2
            else:
                merged.append(current)
                i += 1

        # Renumber weeks sequentially
        start_week = merged[0].get("week", 1) if merged else 1
        for j, w in enumerate(merged):
            w["week"] = start_week + j

        return merged
