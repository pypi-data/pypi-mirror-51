import itertools
from abc import abstractmethod
from numpy import linspace
import logging


from prophesy.data.interval import BoundType
from prophesy.data.point import Point
from prophesy.adapter.pycarl import Rational
import prophesy.config

logger = logging.getLogger(__name__)


class Sampler:
    """
    Base class for performing sampling of given set of points
    """

    def __init__(self):
        pass

    def perform_uniform_sampling(self, parameters, region, samples_per_dimension):
        """
        Samples a uniform grid of points.

        Given a list of intervals (i.e., the first and last point;
        for each dimension, in order) and the number of samples per
        dimension, a uniformly-spaced grid of points (the cartesian
        product) is sampled.
        
        :param parameters: Parameters together with their region.
        :param samples_per_dimension: In how many points should the region be divided.
        """
        logger.debug("Uniform sampling: Fallback to sampling list of samples")
        if samples_per_dimension <= 1:
            raise RuntimeError("No. of samples per dimension must be >= 2")

        # points evenly spaced over the interval, for each dimension
        ranges = []

        if region:
            intervals = region.intervals
        else:
            intervals = parameters.get_parameter_bounds()
        for i in intervals:
            minNum = i.left_bound() if i.left_bound_type() == BoundType.closed else i.left_bound() + prophesy.config.configuration.get_sampling_epsilon()
            maxNum = i.right_bound() if i.right_bound_type() == BoundType.closed else i.right_bound() - prophesy.config.configuration.get_sampling_epsilon()
            ranges.append(map(Rational, linspace(float(minNum), float(maxNum), samples_per_dimension)))
        # turned into grid via cartesian product
        all_points = itertools.product(*ranges)
        all_points = [Point(*coords) for coords in all_points]

        sample_points = parameters.instantiate(all_points)

        return self.perform_sampling(sample_points)

    @abstractmethod
    def perform_sampling(self, samplepoints, ensure_welldefinedness = False):
        """
        Given some parameter instantiations, perform sampling on these instantiations.
        
        :param samplepoints: An iterable yielding parameter instantiations
        :return: A collection with the results of these samples
        :rtype: InstantiationResultDict
        """
        raise NotImplementedError("Abstract sampling function called")
