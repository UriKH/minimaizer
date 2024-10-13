from __future__ import annotations
from typing import Tuple, Union
from math import tan, cos, sin, pow, sqrt, pi

""" Implementation of complex numbers (we don't want to use j, only i) """


class Complex:
    def __init__(self, re: Union[int, float], im: Union[int, float] = 0):
        """
        Create a complex number
        :param re: real part
        :param im: imaginary part
        """
        self.re = float(re)
        self.im = float(im)
        self.r = sqrt(pow(self.re, 2) + pow(self.im, 2))
        self.phase = tan(self.im / self.re) if self.re != 0 else pi / 2

    @classmethod
    def from_polar(cls, r: float, theta: float) -> Complex:
        """
        Create a Complex instance from polar coordinates (r, θ).
        :param r: radius vector
        :param theta: angle θ of the vector
        :return: a complex number instance
        """
        return cls(r * cos(theta), r * sin(theta))

    def polar(self) -> Tuple[float, float]:
        """
        Converts the complex number into polar form
        :return: the polar form of the complex number (r, θ)
        """
        return self.r, self.phase

    def cartesian(self) -> Tuple[float, float]:
        """
        Converts the complex number into cartesian form
        :return: the cartesian form of the number as (real, imaginary)
        """
        return self.re, self.im

    def conjugate(self) -> Complex:
        """
        :return: the complex conjugate (a + bi) -> (a - bi)
        """
        return Complex(self.re, -self.im)

    def __add__(self, other: Union[int, float, Complex]) -> Complex:
        """
        Complex + Complex or Complex + int/float
        :param other: Complex / int / float
        :return: the sum
        """
        if isinstance(other, Complex):
            return Complex(self.re + other.re, self.im + other.im)
        elif isinstance(other, (int, float)):
            return Complex(self.re + other, self.im)
        else:
            raise NotImplementedError

    def __radd__(self, other: Union[int, float]) -> Complex:
        """
        int/float + Complex
        :param other: int / float
        :return: the sum
        """
        return self.__add__(other)

    def __sub__(self, other: Union[int, float, Complex]):
        """
        Complex - Complex or Complex - int/float
        :param other: Complex / int / float
        :return: the sum
        """
        self.__add__(-other)

    def __rsub__(self, other: Union[int, float]):
        """
        int/float - Complex
        :param other: int / float
        :return: the sum
        """
        self.__sub__(other)

    def __mul__(self, other: Union[int, float, Complex]) -> Complex:
        """
        Complex * Complex or Complex * int/float
        :param other: Complex / int / float
        :return: the product
        """
        if isinstance(other, Complex):
            real_part = self.re * other.re - self.im * other.im
            imag_part = self.re * other.im + self.im * other.re
            return Complex(real_part, imag_part)
        elif isinstance(other, (int, float)):
            return Complex(self.re * other, self.im * other)
        else:
            raise NotImplementedError

    def __rmul__(self, other: Union[int, float]) -> Complex:
        """
        int/float * Complex
        :param other: int / float
        :return: the product
        """
        return self.__mul__(other)

    def __truediv__(self, other: Union[int, float, Complex]) -> Complex:
        """
        Complex / Complex or Complex / int/float
        :param other: Complex / int / float
        :return: the fraction
        """
        if isinstance(other, Complex):
            if other == Complex(0, 0):
                raise ZeroDivisionError

            real_part = (self.re * other.re + self.im * other.im) / (other.__abs__() ** 2)
            imag_part = (self.im * other.re - self.re * other.im) / (other.__abs__() ** 2)
            return Complex(real_part, imag_part)
        elif isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError

            return Complex(self.re / other, self.im / other)
        else:
            raise NotImplementedError

    def __rtruediv__(self, other: Union[int, float]) -> Complex:
        """
        int/float / Complex
        :param other: int / float
        :return: the fraction
        """
        if isinstance(other, (int, float)):
            denom = self.__abs__() ** 2
            return self.conjugate().__truediv__(denom)
        else:
            raise NotImplementedError

    def __eq__(self, other: Union[int, float, Complex]) -> bool:
        """
        Check if the numbers are equal
        :param other: a complex number
        :return: true if equal else false
        """
        if isinstance(other, (int, float)):
            return self.re == other and self.im == 0
        elif isinstance(other, Complex):
            return self.re == other.re and self.im == other.im
        else:
            raise NotImplementedError

    def __ne__(self, other) -> bool:
        """
        Check if the numbers are not equal
        :param other: a complex number
        :return: true if not equal else false
        """
        return not self.__eq__(other)

    def __abs__(self) -> float:
        """
        :return: the distance between the number and the origin in the complex plain
        """
        return self.r

    def __neg__(self) -> Complex:
        """
        :return: the negated complex number (a+bi) -> (-a-bi)
        """
        return Complex(-self.re, -self.im)

    def __str__(self):
        return f'{self.re:.3f}+{self.im:.3f}i'

    def __repr__(self):
        return f'({self.re}+{self.im}i)'

    def __pow__(self, power, modulo=None):
        r = pow(self.r, power)
        phase = self.phase * power
        return Complex.from_polar(r, phase)


# complex constant i
i = Complex(0, 1)
