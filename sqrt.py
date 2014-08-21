#!/usr/bin/env python
#
# Julien Leider
#
# This program allows the user to calculate the square root of
# any integer to arbitrary precision using the continued
# fraction expansion for integer square roots.
# It includes a Ratio class for representing rational numbers,
# with tests.

from math import floor, sqrt
import unittest

def gcd(m, n):
    """Compute the greatest common divisor of m and n using Euclid's algorithm."""
    while n != 0:
        r = m % n
        m = n
        n = r
    return m

def lcm(a, b):
    """Compute the least common multiple of a and b."""
    return abs(a * b) / gcd(a, b)

class Ratio:
    """Represent a rational number."""
    
    def __init__(self, num, den=1):
        """Constructor."""
        self.num = num
        self.den = den

    def __add__(self, other):
        """Add two rational numbers; result is in lowest terms."""
        lcd = lcm(self.den, other.den)
        return Ratio(self.num * lcd / self.den + other.num * lcd / other.den,\
                         lcd)

    def __sub__(self, other):
        """Subtract two numbers by adding the negative of one to the other."""
        return self + Ratio(-other.num, other.den)

    def __eq__(self, other):
        """Test equality of two rational numbers."""
        lcd = lcm(self.den, other.den)
        return self.num * lcd / self.den == other.num * lcd / other.den

    def __lt__(self, other):
        """Check if self is less than other."""
        lcd = lcm(self.den, other.den)
        return self.num * lcd/self.den < other.num * lcd/other.den

    def __str__(self):
        """Return string representation of self."""
        if self.num * self.den < 0:
            s = "-"
        else:
            s = ""
        return s + ("%d/%d" % (abs(self.num), abs(self.den)))

    def __abs__(self):
        """Return absolute value of self."""
        return Ratio(abs(self.num), abs(self.den))

    def rec(self):
        """Take reciprocal of self; changes value."""
        self.num, self.den = self.den, self.num

class RatioTest(unittest.TestCase):
    """Class of test cases for the Ratio class."""

    def test_add(self):
        """Test addition."""
        R1 = Ratio(1, 3)
        R2 = Ratio(2, 3)
        R3 = R1 + R2
        self.assertTrue(R3.num == 3)
        self.assertTrue(R3.den == 3)
        self.assertTrue(R1 + R2 == Ratio(3, 3))
        self.assertTrue(Ratio(1, 1) + Ratio(1, 2) == Ratio(3, 2))

    def test_sub(self):
        """Test subtraction."""
        self.assertTrue(Ratio(1, 1) - Ratio(1, 2) == Ratio(1, 2))
        self.assertTrue(Ratio(5, 4) - Ratio(3, 4) == Ratio(1, 2))
        self.assertTrue(Ratio(3, 1) - Ratio(2, 1) == Ratio(1, 1))

    def test_eq(self):
        """Test equality."""
        self.assertTrue(Ratio(5, 4) == Ratio(15, 12))
        self.assertTrue(Ratio(-5, 4) == Ratio(5, -4))
        self.assertTrue(Ratio(2, 3) == Ratio(2, 3))

    def test_lt(self):
        """Test less than."""
        self.assertTrue(Ratio(500, 400) < Ratio(3, 1))
        self.assertTrue(Ratio(1, -3) < Ratio(1, 3))
        self.assertTrue(Ratio(1, 3) < Ratio(1, 2))

    def test_str(self):
        """Test __str__() method for computing string representation of number."""
        self.assertTrue(str(Ratio(5, 4)) == "5/4")
        self.assertTrue(str(Ratio(1, -2)) == "-1/2")

    def test_abs(self):
        """Test absolute value."""
        self.assertTrue(abs(Ratio(1, 5)) == Ratio(1, 5))
        self.assertTrue(abs(Ratio(1, -5)) == Ratio(1, 5))

    def test_rec(self):
        """Test taking the reciprocal."""
        R = Ratio(1, 2)
        R.rec()
        self.assertTrue(R == Ratio(2, 1))
        R = Ratio(-3, 5)
        R.rec()
        self.assertTrue(R == Ratio(5, -3))

def test():
    """Run test cases on Ratio class."""
    unittest.main()

def precSqrt(n, dig = 100):
    """Calculate square root of n, where n is an integer, to dig digits.
    Returns a string.
    
    This function uses the fact that we can write any square root as a continued
    fraction, as discussed on the Wikipedia page on methods of
    computing square roots."""
    pc = None # This will store intermediate approximations to the square root.
    # m, d, and a are the key values we keep track of.
    m = 0
    d = 1
    a = [int(floor(sqrt(n)))]
    if (sqrt(n) == a[0]):
        # The number is a perfect square.
        return str(a[0])
    while True:
        # We update the values of m, d, and a.
        m = d*a[-1] - m # a[-1] is the last value in the sequence.
        d = (n - m**2) / d
        a.append(int(floor((a[0] + m) / d)))
        # We calculate our current approximation to the square root.
        c = Ratio(a[-1])
        for i in reversed(range(len(a) - 1)):
            c.rec()
            c += Ratio(a[i])
        # If we have reached the desired level of accuracy, we terminate.
        if pc != None and abs(c - pc) < Ratio(1, int('1' + '0' * (dig + 1))):
            break
        pc = Ratio(0)
        pc.num = c.num
        pc.den = c.den
    s = str(c.num * int('1' + '0' * dig) / c.den)
    return s[:-dig] + '.' + s[-dig:]

def main():
    """Run program."""
    while True:
        n = input("Enter an integer (press Ctrl-C to quit): ")
        dig = input("Enter number of digits of precision (at least 1): ")
        if dig < 1:
            print "Error: number of digits of precision must be at least 1."
            continue
        if n != int(n) or dig != int(dig):
            print "Error: both numbers must be integers."
            continue
        ans = precSqrt(n, dig)
        print ans

main()
