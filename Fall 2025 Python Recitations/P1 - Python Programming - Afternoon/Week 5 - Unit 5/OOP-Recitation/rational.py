class Rational:
    def __init__(self, numerator, denominator=1):
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero.")
        self._numerator = numerator
        self._denominator = denominator
        self.reduce()

    def __str__(self):
        return f"{self._numerator}/{self._denominator}"

    def __repr__(self):
        return f"Rational({self._numerator}, {self._denominator})"

    def gcd(self, num1, num2):
        while num1 != num2:
            if num1 > num2:
                num1 = num1 - num2
            else:
                num2 = num2 - num1
        return num1

    def reduce(self):
        common_divisor = self.gcd(abs(self._numerator), abs(self._denominator))
        self._numerator //= common_divisor
        self._denominator //= common_divisor
        if self._denominator < 0:
            self._numerator *= -1
            self._denominator *= -1

    def reciprocal(self):
        return Rational(self._denominator, self._numerator)
    
    def get_numerator(self):
        return self._numerator
    
    def get_denominator(self):
        return self._denominator
    
    def set_numerator(self, numerator):
        self._numerator = numerator

    def set_denominator(self, denominator):
        self._denominator = denominator

    def __add__(self, other):
        new_numerator = self._numerator * other.get_denominator() + other.get_numerator() * self._denominator
        new_denominator = self._denominator * other.get_denominator()
        return Rational(new_numerator, new_denominator)

    def __sub__(self, other):
        new_numerator = self._numerator * other.get_denominator() - other.get_numerator() * self._denominator
        new_denominator = self._denominator * other.get_denominator()
        return Rational(new_numerator, new_denominator)

    def __mul__(self, other):
        new_numerator = self._numerator * other.get_numerator()
        new_denominator = self._denominator * other.get_denominator()
        return Rational(new_numerator, new_denominator)

    def __truediv__(self, other):
        return self * other.reciprocal()

    def __eq__(self, other):
        return self._numerator == other.get_numerator() and self._denominator == other.get_denominator()
