from numpy import arange
from itertools import product
from prophesy.data.interval import BoundType


class Range:
    """
    A container similar to the Python native range construct, consisting of a lower bound, an upper bound
    and a step size
    """
    def __init__(self, lower_bound, upper_bound, step_size):
        self.start = lower_bound
        self.stop = upper_bound
        self.step = step_size

    def values(self):
        """
        :return: A list with all values encoded by the range
        """
        return list(arange(self.start, self.stop, self.step)) + [self.stop]


def create_range_from_interval(interval, nr_samples, epsilon=0):
    """
    Given closed interval [l,h], generate a Range with nr_sample
    steps in this interval
    """
    assert nr_samples > 1
    assert not interval.empty()
    if epsilon==0:
        assert interval.is_closed()
    return Range(interval.left_bound() + epsilon if interval.left_bound_type() == BoundType.open else 0, interval.right_bound() - epsilon if interval.right_bound_type() == BoundType.open else 0, (interval.width() / (nr_samples - 1)))


def create_cartesian_product(ranges):
    """
    :param ranges: Iterable containing Range elements
    :return: An iterator for the Cartesian product of the ranges.
    """
    lists = [r.values() for r in ranges]
    return product(*lists)
