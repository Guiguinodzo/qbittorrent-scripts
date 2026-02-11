def human_readable_size(size_in_bytes: int) -> str:
    if abs(size_in_bytes) < 1024:
        return f"{size_in_bytes} bytes"
    elif abs(size_in_bytes) < 1024 * 1024:
        return f"{size_in_bytes / 1024:.2f} KB"
    elif abs(size_in_bytes) < 1024 * 1024 * 1024:
        return f"{size_in_bytes / 1024 / 1024:.2f} MB"
    else:
        return f"{size_in_bytes / 1024 / 1024 / 1024:.2f} GB"
