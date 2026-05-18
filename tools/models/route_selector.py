"""Interface placeholder for future model profile selection."""

VALID_PROFILES = {"short", "standard", "deep", "validation"}


def select_profile(profile: str = "standard") -> str:
    """Return a validated profile name."""
    if profile not in VALID_PROFILES:
        raise ValueError(f"unknown profile: {profile}")
    return profile


if __name__ == "__main__":
    print(select_profile())

