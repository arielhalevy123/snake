from functools import reduce


def fibonacci(n):
    res = [0, 1]

    any(map(lambda a: res.append(sum(res[-2:])),    # sum the last two elements
            range(2, n)))                           # do this for 2 to n

    return res


print(fibonacci(10))


def strcat(lst):
    print(reduce(lambda a,b: a + " " + b, lst))


strcat(['This', 'is', 'a', 'trial'])


def q3(lst):

    filter_evens = lambda sublist: filter(lambda e: e % 2 == 0, sublist)

    square_numbers = lambda evens: map(lambda a: a * a, evens)

    cumulative_sum = lambda squares: reduce(lambda a, b: a + b, squares, 0)

    process_sublist = lambda sublist: cumulative_sum(square_numbers(filter_evens(sublist)))

    return list(map(process_sublist, lst))


print(q3([[4, 5, 6], [5, 3, 2], [7, 3, 10], [8, 2]]))

def comlambda(bin_op):
    return lambda lst: reduce(bin_op, lst)

factorial = comlambda(lambda x,y: x * y)
compower = comlambda(lambda x,y: x ** y)

print(factorial(range(1,11)))
print(compower([4,3,2,1])) # right association



def q5(lst):

    return reduce(lambda x, y: x + y, map(lambda x: x ** 2, filter(lambda num: num % 2 == 0, lst)))

print(q5([2, 3, 4, 5]))


from functools import reduce

def count_palindromes(lists):
    return list(map(lambda sublist: reduce(lambda count, s: count + (s == s[::-1]), sublist, 0), lists)) # this uses a default 3rd parameter for the reduce function. We tried to do without it, for example with a shortened if, but we get a type error of impossible concatenation. Casting is also impossible, apparently.


# Example usage
lists_of_strings = [["level", "world", "radar"], ["hello", "madam"], ["python", "noon"], []]
print(count_palindromes(lists_of_strings))


# 7: lazy evaluation vs eager evaluation
# lazy evaluation refers to evaluating expressions only as soon as they are needed,
# in comparison to eager evaluation, wherein they are evaluated as soon as they are encountered
# in our example, the values = list(generate_values()) instruction generates 1,2,3 in a continuous manner,
# "in a single shot", and only then the square() function is used over the entire list of values.
# On the other hand, with the squared_values = [ square(x) for x in generate_values() ] instruction,
# the values are yielded in a piecemeal fashion and the square(x) is called alternately with the yielding,
# i.e yield call yield call yield call. Thus eager evaluation can possibly be more memory consumptive.


primes_sorted_desc = lambda lst: sorted([x for x in lst if x > 1 and all(x % i != 0 for i in range(2, x))], reverse=True)

# we can use the range(2, sqrt(x) + 1) to save calculations, values beyond this one aren't needed, since
# if they cannot divide the element x in question (the product will be larger than x)

    # Example usage
print(primes_sorted_desc([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]))