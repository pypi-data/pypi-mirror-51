import logging
import itertools

from prophesy.regions.region_generation import RegionGenerator
from prophesy.regions.welldefinedness import check_welldefinedness, WelldefinednessResult
from prophesy.data.hyperrectangle import HyperRectangle
from prophesy.data.interval import BoundType
from prophesy.data.point import Point
from prophesy.data.samples import ParameterInstantiation
from prophesy.smt.Z3cli_solver import Z3CliSolver

logger = logging.getLogger(__name__)


class _AnnotatedRegion:
    """
    Named tuple holding the region and additional information.
    """

    def __init__(self, region, samples, safe=None, well_defined=WelldefinednessResult.Undecided,
                 graph_preserving=WelldefinednessResult.Undecided, closest_sample=None,
                 closest_inverse_sample_distance=None):
        self.region = region
        self.samples = samples
        self.safe = safe
        self.graph_preserving = graph_preserving
        self.well_defined = well_defined
        self.closest_sample = closest_sample
        self.closest_inverse_sample_distance = closest_inverse_sample_distance
        self.empty_checks = 0 if len(samples) > 0 else 1


class HyperRectangleRegions(RegionGenerator):
    """
    Region generation using hyperrectangles.
    """

    def __init__(self, samples, parameters, region, threshold, checker, wd_constraints, gp_constraints, split_uniformly=False, generate_plots=False, allow_homogeneity=False, sampler = None):
        super().__init__(samples, parameters, region, threshold, checker, wd_constraints, gp_constraints, generate_plot=generate_plots, allow_homogeneity=allow_homogeneity)

        self.regions = []
        self.parked_regions = []
        self.accepted_regions_safe = []
        self.accepted_regions_unsafe = []

        self.sample_generator = sampler
        # Number of maximal consecutive recursive splits.
        self.check_depth = 5
        if split_uniformly:
            self.split = HyperRectangleRegions.split_uniformly_in_every_dimension
        else:
            self.split = HyperRectangleRegions.split_by_growing_rectangles

        # Setup initial region
        regionsamples = []

        # Add all samples to region
        for instantiation, value in self.safe_samples.items():
            if region.contains(instantiation.get_point(parameters)):
                regionsamples.append((instantiation.get_point(parameters), True))
        for instantiation, value in self.bad_samples.items():
            if region.contains(instantiation.get_point(parameters)):
                regionsamples.append((instantiation.get_point(parameters), False))

        # Check initial region
        self.check_region(_AnnotatedRegion(region, regionsamples))
        self._sort_regions()

    def _sort_regions_by_size(self, reverse=True):
        """
        Sort regions by size.
        :param reverse: Flag indicating if order should be reversed.
        """
        self.regions.sort(key=lambda x: x.region.size(), reverse=reverse)

    def _sort_regions(self):
        """
        Sort regions by size and closest inverse sample distance.
        """
        self.regions.sort(key=lambda x: (x.well_defined != WelldefinednessResult.Illdefined, -x.region.size(),
                                         -x.closest_inverse_sample_distance if x.closest_inverse_sample_distance else 0))

    def plot_candidate(self):
        boxes = [self.regions[0].region]
        if self.regions[0].safe:
            self.plot_results(poly_blue_dotted=boxes, display=False)
        else:
            self.plot_results(poly_blue_crossed=boxes, display=False)

    def _compute_closest_inverse_sample(self, hypothesis_safe, region):
        """
        Get sample clostest to the region center.
        :param hypothesis_safe: Flag iff the region is considered safe.
        :param region: Region.
        :return: Closest sample to region center or None if no sample was found.
        """
        if hypothesis_safe:
            inverse_samples = self.bad_samples
        else:
            inverse_samples = self.safe_samples

        if len(inverse_samples) == 0:
            return None
        else:
            center = region.center()
            dist = None
            for sample in inverse_samples.items():
                new_dist = sample[0].get_point(self.parameters).distance(center)
                if not dist or new_dist <= dist:
                    dist = new_dist
            return dist

    def _guess_hypothesis(self, region):
        """
        Get hypothesis for region according to closest sample.
        :param region: Region.
        :return: True iff the region hypothesis is safe.
        """
        logger.debug("Guess hypothesis for region {}".format(region))

        if len(self.safe_samples.items()) == 0:
            return False
        if len(self.bad_samples.items()) == 0:
            return True

        sublogger = logger.getChild("_guess_hypothesis")
        center = region.center()
        sublogger.debug("Center is at {}".format(center))
        dist = None
        for sample in self.safe_samples.items():
            new_dist = sample[0].get_point(self.parameters).distance(center)
            if not dist or new_dist <= dist:
                sublogger.debug("Currently closest safe sample: {}".format(sample[0]))
                dist = new_dist
        for sample in self.bad_samples.items():
            new_dist = sample[0].get_point(self.parameters).distance(center)
            if not dist or new_dist < dist:
                sublogger.debug("Currently closest bad sample {} is closer than any safe sample".format(sample[0]))
                return False
        sublogger.debug("We have no samples available, assume safe for now.")
        return True
        # TODO Consider close regions for this.

    @staticmethod
    def split_by_growing_rectangles(region):
        """
        Split the region according to growing rectangles.
        :param region: Region.
        :return: New regions after splitting.
        """
        logger.debug("Split region {}".format(region.region))

        # Get all anchor points
        bounds = [(interv.left_bound(), interv.right_bound()) for interv in region.region.intervals]
        anchor_points = [Point(*val) for val in itertools.product(*bounds)]

        best_candidate = None
        for anchor in anchor_points:
            for anchor2, safe_anchor in region.samples:
                rectangle = HyperRectangle.from_extremal_points(anchor, anchor2,
                                                                BoundType.closed)  # TODO handle open intervals
                size = rectangle.size()
                if size <= 0 or size >= region.region.size():
                    # Rectangle too small or too large
                    continue
                if best_candidate is not None and size <= best_candidate[0]:
                    # Larger candidate already known
                    continue

                # Check candidate
                valid = True
                for pt, safe in region.samples:
                    if rectangle.contains(pt) and safe != safe_anchor:
                        valid = False
                        break
                if valid:
                    # Found better candidate
                    best_candidate = (size, anchor, anchor2)

        if best_candidate is None:
            # No good sample inside the region found -> split uniformly
            logger.debug("No candidate region found, split uniformly as fallback.")
            return HyperRectangleRegions.split_uniformly_in_every_dimension(region)

        logger.debug(
            "Candidate: {} for anchor {} and sample {}".format(best_candidate[0], best_candidate[1], best_candidate[2]))
        # Construct hyperrectangle for each anchor and the sample point
        result = []
        for anchor in anchor_points:
            new_rectangle = HyperRectangle.from_extremal_points(anchor, best_candidate[2], BoundType.closed)
            result.append(new_rectangle)

        logger.debug("New regions:\n\t{}".format("\n\t".join([str(region) for region in result])))
        return result

    @staticmethod
    def split_uniformly_in_every_dimension(region):
        """
        Split the region uniformly in every region.
        :param region: Region.
        :return: New regions after splitting.
        """
        return region.region.split_in_every_dimension()

    def check_region(self, region, depth=0):
        """
        Check if the given region can be assumed safe or bad based on known samples.
        If samples are mixed, split the region and retry.
        Resulting regions are added to self.regions.
        :param region: Region.
        :param depth: Maximal depth for region refining.
        """
        if depth >= self.check_depth:
            self.parked_regions.append(region)
            return

        if self.checker.supports_only_closed_regions():
            region.region = region.region.close()

        # TODO check graph preserving seperately.
        if region.well_defined == WelldefinednessResult.Undecided:
            logger.info("Check well-definedness for the region")
            solver = Z3CliSolver()
            solver.run()
            wd_res = check_welldefinedness(solver, self.parameters, region.region,
                                           self.gp_constraints + self.wd_constraints)
            solver.stop()
            if wd_res == WelldefinednessResult.Illdefined:
                region.well_defined = WelldefinednessResult.Illdefined
                self.regions.append(region)
                return
            if wd_res == WelldefinednessResult.Welldefined:
                region.well_defined = WelldefinednessResult.Welldefined
                region.graph_preserving = WelldefinednessResult.Welldefined

        if region.well_defined == WelldefinednessResult.Welldefined:
            mixed = True

            if self.sample_generator and len(region.samples) == 0:
                logger.debug("Sampling as there is no sample in the region.")
                sampledict  =  self.sample_generator.perform_sampling([ParameterInstantiation.from_point(region.region.center(), self.parameters)], surely_welldefined=True)
                region.samples = [(region.region.center(), list(sampledict.items())[0][1] > self.threshold)]
                region.empty_checks = 0
            if len(region.samples) == 1:
                hypothesis_safe = region.samples[0][1]
                mixed = False
            elif len(region.samples) == 0:

                hypothesis_safe = self._guess_hypothesis(region.region)
                mixed = False
            elif all([sample[1] for sample in region.samples]):
                # All safe
                hypothesis_safe = True
                mixed = False
            elif all([not sample[1] for sample in region.samples]):
                # All bad
                hypothesis_safe = False
                mixed = False

            if not mixed:
                dist = self._compute_closest_inverse_sample(hypothesis_safe, region.region)
                region.safe = hypothesis_safe
                region.closest_inverse_sample_distance = dist
                self.regions.append(region)
                return

        # Mixed region, split.
        newelems = self.split(region)
        if newelems is None:
            return None
        for newregion in newelems:
            newsamples = []
            for pt, safe in region.samples:
                if newregion.contains(pt):
                    newsamples.append((pt, safe))
            self.check_region(_AnnotatedRegion(newregion, newsamples, well_defined=region.well_defined,
                                               graph_preserving=region.graph_preserving), depth + 1)

    def fail_region(self, homogeneity=False):
        logger.debug("Failed checking the region.")
        # Split region and try again
        regionelem = self.regions[0]

        # failure ony applies for region that was already consistent
        self.regions = self.regions[1:]
        if regionelem.empty_checks == 1 and not homogeneity:
            logger.debug("Region has not been checked for inverse.")
            dist = self._compute_closest_inverse_sample(not regionelem.safe, regionelem.region)
            self.regions.insert(0, _AnnotatedRegion(regionelem.region, regionelem.samples, not regionelem.safe,
                                                    well_defined=regionelem.well_defined,
                                                    graph_preserving=regionelem.graph_preserving,
                                                    closest_inverse_sample_distance=dist))
            self.regions[0].empty_checks = 2
        else:
            logger.debug("Region has to be split.")
            newelems = self.split(regionelem)
            for newregion in newelems:

                wd = regionelem.well_defined
                gp = regionelem.graph_preserving
                if self.checker.supports_only_closed_regions():
                    newregion = newregion.close()
                elif True:#self.checker.prefers_closed_regions():
                    #newregion = newregion.close()
                    solver = Z3CliSolver()
                    solver.run()
                    wd_res = check_welldefinedness(solver, self.parameters, newregion.close(),
                                                   self.gp_constraints + self.wd_constraints)
                    solver.stop()
                    if wd_res == WelldefinednessResult.Welldefined:
                        newregion = newregion.close()
                logger.debug("Add region to consider later: {}".format(newregion))
                newsamples = []

                for pt, safe in regionelem.samples:
                    if not newregion.contains(pt):
                        continue
                    newsamples.append((pt, safe))
                if len(newsamples) == 0:
                    if self.sample_generator:
                        logger.debug("Sampling as there is no sample in the region.")
                        sampledict = self.sample_generator.perform_sampling(
                            [ParameterInstantiation.from_point(newregion.center(), self.parameters)],
                            surely_welldefined=True)
                        hypothesis = list(sampledict.items())[0][1] < self.threshold
                        newsamples = [(newregion.center(), hypothesis)]
                    else:
                        hypothesis = self._guess_hypothesis(newregion)
                else:
                    hypothesis = regionelem.safe

                dist = self._compute_closest_inverse_sample(hypothesis, newregion)
                self.regions.insert(0, _AnnotatedRegion(newregion, newsamples, hypothesis,
                                                        well_defined=wd,
                                                        graph_preserving=gp,
                                                        closest_inverse_sample_distance=dist))

        self._sort_regions()

    def reject_region(self, sample):
        logger.debug("Reject region with %s as counter example", sample)
        # New sample, add it to current region
        self.regions[0].samples.append((sample.get_instantiation_point(self.parameters), not self.regions[0].safe))
        # Check region
        self.check_region(self.regions[0])
        # Also remove failed region
        self.regions = self.regions[1:]
        self._sort_regions()

    def refine_region(self, new_regions):
        """
        If a region could not be checked, but we know that only a region has to be checked afterwards.
        """
        logger.debug("Refine region")
        # get the old state from the checked region
        samples = self.regions[0].samples
        safe = self.regions[0].safe
        graph_preserving = self.regions[0].graph_preserving
        well_defined = self.regions[0].well_defined

        # remove the old region from checking queue
        self.regions = self.regions[1:]
        for region in new_regions:
            # check which samples belong to which region
            samplesContained = []
            for sample in samples:
                if region.contains(sample[0]):
                    samplesContained.append(sample)
            if self.checker.supports_only_closed_regions():
                region = region.close()

            # create a new AnnotatedRegion for each region which was cutoff
            toAdd = _AnnotatedRegion(region, samplesContained, safe, well_defined, graph_preserving)
            self.regions.append(toAdd)

        # sort the regions (reversed by default)
        self._sort_regions_by_size()

    def accept_region(self):
        logger.debug("Accept region")
        # Done with the region
        if self.regions[0].safe:
            self.accepted_regions_safe.append(self.regions[0])
        else:
            self.accepted_regions_unsafe.append(self.regions[0])
        # Remove from all regions
        self.regions = self.regions[1:]

    def ignore_region(self):
        # Remove region
        self.regions = self.regions[1:]

    def next_region(self):
        if len(self.regions) == 0:
            return None

        region = self.regions[0]
        if self.checker.supports_only_closed_regions():
            while len(self.regions) > 0:
                regions_opposite = self.accepted_regions_unsafe if region.safe else self.accepted_regions_safe
                refuted = False
                for r in regions_opposite:
                    if r.region.non_empty_intersection(region.region):
                        self.fail_region()
                        region = self.regions[0]
                        refuted = True
                        break
                if not refuted:
                    break
        logger.debug("Consider %s as next region with hypothesis %s", region.region, region.safe)
        assert region.well_defined != WelldefinednessResult.Undecided
        check_for_eq = self.allow_homogenous_check #and len(region.samples) > 0
        return region.region, region.well_defined, region.safe, check_for_eq
