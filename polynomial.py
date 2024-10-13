from __future__ import annotations
from typing import List, Union
import numpy as np
import math
from complex import Complex
from scipy.signal import fftconvolve


class Polynomial:
    def __init__(self, coefficients: List[Union[int, float]]):
        self.coef = np.array(coefficients)
        self.degree = len(coefficients)-1 if len(coefficients) != 0 else -math.inf

        roots = [Complex(r.real, r.imag) for r in np.roots(self.coef).tolist()]
        self.roots = {r: roots.count(r) for r in set(roots)}

    def coefficients(self):
        return self.coef.tolist()

    def __add__(self, other: Union[Polynomial, int, float]) -> Polynomial:
        if isinstance(other, Polynomial):
            return Polynomial((self.coef + other.coef).tolist())
        elif isinstance(other, (int, float)):
            temp = self.coefficients()
            temp[0] += other
            return Polynomial(temp)
        else:
            raise NotImplementedError

    __radd__ = __add__

    def __sub__(self, other: Union[Polynomial, int, float]) -> Polynomial:
        if isinstance(other, Polynomial):
            return Polynomial((self.coef - other.coef).tolist())
        elif isinstance(other, (int, float)):
            temp = self.coefficients()
            temp[0] -= other
            return Polynomial(temp)
        else:
            raise NotImplementedError

    def __neg__(self):
        return Polynomial(-self.coefficients())

    def __rsub__(self, other: Union[int, float]):
        return self.__neg__() + other

    def __str__(self):
        pieces = []

        for i, c in enumerate(reversed(self.coefficients())):
            if c == 0:
                continue
            sign = '+ ' if c > 0 else '- '
            coef = '' if abs(c) == 1 and i != 0 else f'{abs(c)}'

            if i == 0:
                coef = '-' + coef if c < 0 else coef
                pieces.append(coef)
            elif i == 1:
                coef = sign + coef
                pieces.append(f'{coef}x')
            else:
                coef = sign + coef
                pieces.append(f'{coef}(x^{i})')
        return ' '.join(pieces)

    def __mul__(self, other: Polynomial):
        return Polynomial(fftconvolve(self.coefficients(), other.coefficients()).tolist())

    __rmul__ = __mul__

    def __truediv__(self, other: Union[int, float]):
        if not other:
            raise ZeroDivisionError
        return Polynomial((self.coef / other).tolist())

    def div(self, other: Polynomial):
        if len(set(other.coefficients())) == 1 and 0 in other.coefficients():
            raise ZeroDivisionError
        p1 = self.roots
        p2 = other.roots

        # remove similar roots if there are any
        if len(set(self.coefficients()) - set(other.coefficients())) != 0:
            for k in self.roots.keys():
                if k not in p2.keys():
                    continue
                p1[k] -= min(p2[k], p1[k])

        # polynomial division
        dividend = self.polynomial_from_roots(list(np.array([[r] * t for r, t in p1.items()]).flatten()))
        divisor = self.polynomial_from_roots(list(np.array([[r] * t for r, t in p2.items()]).flatten()))

        quotient = []
        remainder = dividend[:]  # Copy dividend to remainder

        degree_dividend = len(dividend) - 1
        degree_divisor = len(divisor) - 1

        if degree_dividend < degree_divisor:
            return [0], dividend

        while degree_dividend >= degree_divisor:
            leading_coefficient = remainder[0] / divisor[0]
            quotient.append(leading_coefficient)
            remainder = [remainder[i] - leading_coefficient * divisor[i] for i in range(len(divisor))] + remainder[
                                                                                                 len(divisor):]
            while len(remainder) > 1 and remainder[0] == 0:
                remainder = remainder[1:]
            degree_dividend = len(remainder) - 1
        return quotient, remainder

    @classmethod
    def polynomial_from_roots(cls, roots):
        coeffs = [1]
        for root in roots:
            coeffs = np.convolve(coeffs, [1, -root])
        return coeffs.tolist()


if __name__ == '__main__':
    p1 = Polynomial([1, 6, 7, 2])
    p2 = Polynomial([1, 1])
    print(p1)
    print(p1.div(p2))
