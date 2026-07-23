"""Meeting-level schedule data for HONR 46400 (Fall 2026) — v2 rebuild.

One dict per meeting, 34 fields each. Authored from the Fall 2026 master prompt
architecture (16 weekly topics nb00–nb15, milestones M0–M15, Student Research
Lead flipped classroom) + planning/CALENDAR_BACKBONE.csv; serialized by
scripts/build_meeting_schedule.py into planning/MEETING_SCHEDULE.{csv,md}.

43 meetings = 41 in-person + 2 async (Fri Oct 2, Mon Nov 23). No class on
Labor Day (Sep 7), October Break (Oct 12), the post-Expo Wednesday (Nov 18),
and Thanksgiving (Nov 25/27).

RDSS chapter titles verified against book.declaredesign.org and the local
replication materials (_adm/_references/book/); never invent a chapter,
declaration, or dataset — see planning/SOURCE_AUDIT_V2.md. The v1 (44-meeting,
compass-sequenced) data is archived at _production_kit/schedule_data_v1/ and
at git tag v1-compass-build.

SRL fields: `srl_slot` = "SRL slot NN — rotation seat X" for the 25 leadable
Mon/Wed lectures (empty for Week 1's two instructor-led lectures, studios, and
async modules); `srl_focus` = the one-line puzzle/challenge the Student
Research Lead owns that day. Rotation seats A–E map to the roster in the SRL
handbook, never to names here.
"""

from .part1 import MEETINGS_P1
from .part2 import MEETINGS_P2
from .part3 import MEETINGS_P3
from .part4 import MEETINGS_P4

MEETINGS = MEETINGS_P1 + MEETINGS_P2 + MEETINGS_P3 + MEETINGS_P4

COLUMNS = [
    "meeting", "date", "day", "modality", "unit", "title",
    "driving_question", "secondary_questions", "inquiry",
    "srl_slot", "srl_focus",
    "claim_permitted", "claim_not_permitted",
    "rdss_reading", "cb_reading", "other_material", "provenance",
    "concepts", "python_r_dependency", "dataset_simulation",
    "minute_dynamic", "hands_on_activity", "practice", "discussion_prompt",
    "project_connection", "milestone_developed", "milestone_work_time",
    "milestone_presentation_review", "student_prep", "student_artifact",
    "exit_ticket", "homework_next_milestone", "instructor_prep",
    "risks_contingency",
]
