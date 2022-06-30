def get_length(array: any, min_length=0):
    if array is not None and len(array) >= min_length:
        return len(array)
    else:
        return 0


def zero_if_none(value: any):
    if value is None:
        return 0
    else:
        return value
