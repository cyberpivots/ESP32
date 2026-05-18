"""Interface placeholder for future prompt/task triage.

This script intentionally does not implement routing yet. The workspace remains
in scaffold mode until model and routing behavior are accepted through docs and
tests.
"""


def classify_task(_text: str) -> str:
    """Return the default route until a routing ADR/tool spec exists."""
    return "standard"


if __name__ == "__main__":
    print("standard")

