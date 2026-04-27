from rational import Rational

# Create Rational objects
r1 = Rational(5, 6)
r2 = Rational(-1, 4)
r3 = Rational(3, -12)
# r4 = Rational(2, 0)    # This should cause an exception

print(f"r1: {r1}")
# Output: r1: 5/6
print(f"r2: {r2}")
# Output: r2: -1/4
print(f"r3: {r3}")
# Output: r3: -1/4

# Reciprocal
r4 = r1.reciprocal()
print(f"reciprocal of r1: {r4}")
# Output: reciprocal of r1: 6/5

# Addition
r1_plus_r2 = r1 + r2
print(f"{r1} + {r2} = {r1_plus_r2}")
# Output: 5/6 + -1/4 = 7/12

# Subtraction
r1_minus_r2 = r1 - r2
print(f"{r1} - {r2} = {r1_minus_r2}")
# Output: 5/6 - -1/4 = 13/12

# Multiplication
r1_times_r2 = r1 * r2
print(f"{r1} * {r2} = {r1_times_r2}")
# Output: 5/6 * -1/4 = -5/24

# Division
r1_divided_by_r2 = r1 / r2
print(f"{r1} / {r2} = {r1_divided_by_r2}")
# Output: 5/6 / -1/4 = -10/3

# Equality
print(f"{r1} == {r2} is {r1 == r2}")
# Output: 5/6 == -1/4 is False
print(f"{r2} == {r3} is {r2 == r3}")
# Output: -1/4 == -1/4 is True