def get_length(array: any, min_length: int = 0) -> int:
    """Get length of array and return if it's longer or equal to min length."""
    if array is not None and len(array) >= min_length:
        return len(array)
    else:
        return 0
