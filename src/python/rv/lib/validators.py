def divisible_by(x):
    def validate(instance, attr, value):
        if value % x != 0:
            raise ValueError("Value is not divisible by {}".format(x))

    return validate


def in_range(start, end):
    def validate(instance, attr, value):
        if value < start or value > end:
            raise ValueError("Value is not in range {}-{}".format(start, end))

    return validate


def is_length(x):
    def validate(instance, attr, value):
        if len(value) != x:
            raise ValueError("Value is not of length {}".format(x))

    return validate
