"""Meeting-level schedule data for HONR 46400 (Fall 2026).

One dict per meeting, 32 fields each (the brief §8 columns). Authored from
planning/COURSE_MASTER_PLAN.md + planning/CALENDAR_BACKBONE.csv; serialized by
scripts/build_meeting_schedule.py into planning/MEETING_SCHEDULE.{csv,md}.

RDSS chapter titles verified against book.declaredesign.org and the local
replication materials (_adm/_references/book/); declaration/diagnosis numbers
verified against the files on disk. Never invent a chapter, declaration, or
dataset — see planning/SOURCE_AUDIT.md §11.
"""

from .part1 import MEETINGS_P1
from .part2 import MEETINGS_P2
from .part3 import MEETINGS_P3
from .part4 import MEETINGS_P4

MEETINGS = MEETINGS_P1 + MEETINGS_P2 + MEETINGS_P3 + MEETINGS_P4

COLUMNS = [
    "meeting", "date", "day", "modality", "unit", "title",
    "driving_question", "secondary_questions", "inquiry",
    "claim_permitted", "claim_not_permitted",
    "rdss_reading", "cb_reading", "other_material", "provenance",
    "concepts", "python_r_dependency", "dataset_simulation",
    "minute_dynamic", "hands_on_activity", "practice", "discussion_prompt",
    "project_connection", "milestone_developed", "milestone_work_time",
    "milestone_presentation_review", "student_prep", "student_artifact",
    "exit_ticket", "homework_next_milestone", "instructor_prep",
    "risks_contingency",
]
