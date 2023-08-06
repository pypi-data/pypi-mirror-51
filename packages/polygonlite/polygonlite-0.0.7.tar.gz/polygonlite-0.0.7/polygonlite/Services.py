def is_between(number1, number2, number3):
    if number2 >= number1:
        if number2 <= number3:
            return True
    elif number2 >= number3:
        if number1 <= number1:
            return True
    return False


def dot(a, b):
    return sum([a[i] * b[i] for i in range(len(b))])


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0: return 0  # Collinear
    if val > 0: return 1  # Clockwise
    return 2  # Anti clockwise

