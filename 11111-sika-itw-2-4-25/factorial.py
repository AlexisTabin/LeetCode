
# integer input
#

previous_results = {}


def factorial(n: int):
    if n in previous_results:
        return previous_results[n]
    if n < 0:
        raise Exception("Sorry, no numbers below zero")
    if n == 0 or n == 1:
        return 1
    result = n * factorial(n-1)
    previous_results[n] = result
    return result


result = factorial(5)
print(previous_results)
print(result)
