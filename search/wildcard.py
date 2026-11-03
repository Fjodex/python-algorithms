"""Match strings against simple '*' wildcard patterns."""


def wildcard_match(pattern: str, value: str) -> bool:
    """Return whether value matches pattern; '*' matches any sequence, incl. empty."""
    if "*" not in pattern:
        return pattern == value
    parts = pattern.split('*')
    anchored_start = not pattern.startswith('*')
    anchored_end = not pattern.endswith('*')
    position = 0
    if anchored_start:
        prefix = parts.pop(0)
        if not value.startswith(prefix):
            return False
        position = len(prefix)
    suffix = parts.pop() if anchored_end else None
    end_limit = len(value) - len(suffix) if suffix is not None else len(value)
    if end_limit < position or (suffix is not None and not value.endswith(suffix)):
        return False
    for part in parts:
        found = value.find(part, position, end_limit)
        if found == -1:
            return False
        position = found + len(part)
    return position <= end_limit


def search_files(files: list[str], pattern: str) -> list[str]:
    return [name for name in files if wildcard_match(pattern, name)]
