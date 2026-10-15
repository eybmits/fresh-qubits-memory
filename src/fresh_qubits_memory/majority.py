"""Majority-refresh scalar model from the supplied manuscript.

Sources: Eq. (2), the exact binomial tail; Eqs. (3)/(28), lambda=1-2*p_r;
Eq. (4), the lower guarantee; Table I, T=max{t >= 0: lambda**t >= 1/2}.
This computes the classical scalar model, not a quantum circuit simulation.
"""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
from math import comb

DEFAULT_PRECISION = 80
MAX_COPIES = 255
MAX_Q_PLACES = 100
MAX_WORK_PRECISION = 4096


def _q_fraction(q: str | Decimal | float | int) -> tuple[Decimal, Fraction]:
    """Interpret floats through str(); decimal strings give explicit input precision."""
    if isinstance(q, bool) or not isinstance(q, (str, Decimal, float, int)):
        raise ValueError("q must be a finite decimal number with 0 < q < 1")
    if len(str(q)) > 256:
        raise ValueError("q has too many digits")
    try:
        value = Decimal(str(q))
    except InvalidOperation as exc:
        raise ValueError("q must be a finite decimal number") from exc
    if not value.is_finite() or not Decimal(0) < value < Decimal(1):
        raise ValueError("q must satisfy 0 < q < 1")
    if value.as_tuple().exponent < -MAX_Q_PLACES:
        raise ValueError(f"q must use at most {MAX_Q_PLACES} decimal places")
    return value, Fraction(value)


def _validate_r(r: int) -> None:
    if isinstance(r, bool) or not isinstance(r, int) or not 1 <= r <= MAX_COPIES or r % 2 == 0:
        raise ValueError(f"r must be an odd integer from 1 to {MAX_COPIES}")


def _validate_precision(precision: int) -> None:
    if isinstance(precision, bool) or not isinstance(precision, int) or not 30 <= precision <= 512:
        raise ValueError("precision must be an integer from 30 to 512 decimal digits")


def _tail(q: Fraction, r: int) -> Fraction:
    p = (1 - q) / 2
    a, b = p.numerator, p.denominator
    c = b - a
    start = (r + 1) // 2
    # Each summand has the common denominator b**r. No floating subtraction
    # from one is used, even when the logical error is extremely small.
    term = comb(r, start) * a**start * c ** (r - start)
    numerator = term
    for j in range(start, r):
        term = term * (r - j) * a // ((j + 1) * c)
        numerator += term
    return Fraction(numerator, b**r)


def majority_error(q: str | Decimal | float | int, r: int) -> Fraction:
    """Return the exact rational binomial majority-error probability, Eq. (2).

    q is in (0, 1), r is odd and at most 255, and q has at most 100 decimal
    places. Floats are interpreted via str(q); prefer strings or Decimal.
    """
    _, q_fraction = _q_fraction(q)
    _validate_r(r)
    return _tail(q_fraction, r)


def _decimal(value: Fraction, precision: int) -> Decimal:
    with localcontext() as context:
        context.prec = precision
        return Decimal(value.numerator) / Decimal(value.denominator)


def _bounds(value: Fraction) -> tuple[Decimal, Decimal]:
    """Outward-rounded bounds at the active Decimal precision."""
    with localcontext() as context:
        context.rounding = ROUND_FLOOR
        lower = Decimal(value.numerator) / Decimal(value.denominator)
        context.rounding = ROUND_CEILING
        upper = Decimal(value.numerator) / Decimal(value.denominator)
        return lower, upper


def _integer_interval(numerator: tuple[Decimal, Decimal], denominator: tuple[Decimal, Decimal]) -> int | None:
    with localcontext() as context:
        context.rounding = ROUND_FLOOR
        lower = numerator[0] / denominator[1]
        context.rounding = ROUND_CEILING
        upper = numerator[1] / denominator[0]
        low_int = int(lower.to_integral_value(rounding=ROUND_FLOOR))
        high_int = int(upper.to_integral_value(rounding=ROUND_FLOOR))
    return low_int if low_int == high_int else None


def _lifetime(error: Fraction, precision: int) -> tuple[int, int]:
    decay = 1 - 2 * error
    if decay == Fraction(1, 2):
        # Exact equality belongs to the readable interval (>=, not >).
        return 1, precision
    # The lifetime has approximately D digits when error ~ 10**(-D).
    # Keeping 2D extra digits protects both 1-2*error and the integer floor.
    small_error_digits = max(0, -_decimal(error, 30).adjusted())
    work = precision + 2 * small_error_digits
    while work <= MAX_WORK_PRECISION:
        with localcontext() as context:
            context.prec = work
            low, high = _bounds(decay)
            if low > 0 and high < 1:
                ln_two = Decimal(2).ln()
                numerator = (ln_two.next_minus(), ln_two.next_plus())
                # Decimal.ln is correctly rounded; one ulp on either side
                # encloses it. Monotonicity then encloses -ln(exact decay).
                denominator = (-high.ln().next_plus(), -low.ln().next_minus())
                result = _integer_interval(numerator, denominator)
                if result is not None:
                    return result, work
        work *= 2
    raise ArithmeticError(f"cannot certify lifetime within {MAX_WORK_PRECISION} working digits; reduce r or the extremity of q")


def readable_lifetime(error: Fraction, *, precision: int = DEFAULT_PRECISION) -> int:
    """Largest integer T with (1-2*error)**T >= 1/2, certified by log bounds.

    The error must be an exact Fraction in (0, 1/2). Precision is 30..512;
    internal precision increases as needed, up to 4096 decimal digits.
    """
    _validate_precision(precision)
    if not isinstance(error, Fraction) or not Fraction(0) < error < Fraction(1, 2):
        raise ValueError("error must be an exact Fraction with 0 < error < 1/2")
    return _lifetime(error, precision)[0]


def _guarantee(q: Fraction, r: int, precision: int) -> tuple[int, int]:
    # exp(alpha_q*r)/4 = 1/(4*sqrt((1-q*q)**r)), Eq. (4).
    base = (1 - q * q) ** r
    work = precision
    while work <= MAX_WORK_PRECISION:
        with localcontext() as context:
            context.prec = work
            lower, upper = _bounds(base)
            lower = lower.sqrt().next_minus()
            upper = upper.sqrt().next_plus()
            result = _integer_interval((Decimal("0.25"), Decimal("0.25")), (lower, upper))
            if result is not None:
                return result, work
        work *= 2
    raise ArithmeticError(f"cannot certify guarantee within {MAX_WORK_PRECISION} working digits")


@dataclass(frozen=True)
class MajorityResult:
    q: Decimal
    copies: int
    fresh_qubits: int
    total_qubits: int
    logical_error: Decimal
    decay_factor: Decimal
    lifetime_cycles: int
    guaranteed_cycles: int
    decimal_precision: int
    working_precision: int

    def as_dict(self) -> dict[str, str | int]:
        """JSON/CSV representation; decimal values remain decimal strings."""
        return {key: str(value) if isinstance(value, Decimal) else value for key, value in vars(self).items()}


def analyze_majority(q: str | Decimal | float | int, r: int, *, precision: int = DEFAULT_PRECISION) -> MajorityResult:
    """Evaluate a row of Table I; time counts hold cycles after the write.

    Integer lifetime and guarantee use outward-rounded bounds. Reported
    probabilities are rounded to ``precision`` digits. A rounded decay_factor
    may print as 1 for extreme inputs, but it is never used for the lifetime.
    """
    q_decimal, q_fraction = _q_fraction(q)
    _validate_r(r)
    _validate_precision(precision)
    error = _tail(q_fraction, r)
    lifetime, work = _lifetime(error, precision)
    guarantee, guarantee_work = _guarantee(q_fraction, r, work)
    return MajorityResult(
        q=q_decimal,
        copies=r,
        fresh_qubits=r + 2,
        total_qubits=2 * r + 2,
        logical_error=_decimal(error, precision),
        decay_factor=_decimal(1 - 2 * error, precision),
        lifetime_cycles=lifetime,
        guaranteed_cycles=guarantee,
        decimal_precision=precision,
        working_precision=max(work, guarantee_work),
    )
