def path(src: str) -> str:
    """A function to fix paths

    Args:
        src (str): Source directory to be fixed.

    Returns:
        str: Fixed Source directory.
    """
    if src[0] == "/": # Removes the first / from the relative path.
        src = src[1:]
    
    return src