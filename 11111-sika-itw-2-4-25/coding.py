# unsorted array of integers
# [-2, -3, +2, +5]
# O(n)

def find_high(numbers):
    nb_map = {}
    largest_value = 0
    for i, num in enumerate(numbers):
        if (num * -1) in nb_map and abs(num) > largest_value:
            largest_value = abs(num)
        nb_map[num] = True
    return largest_value


def find_high_first(numbers):
    nb_map = {}
    for num in numbers:
        if num < 0:
            nb_map[abs(num)] = True

    largest_num = min(numbers)
    for num in numbers:
        if num > largest_num and num in nb_map:
            largest_num = num

    return largest_num


rest = find_high([-2, -3, 2, 3, 5])
print(rest)
