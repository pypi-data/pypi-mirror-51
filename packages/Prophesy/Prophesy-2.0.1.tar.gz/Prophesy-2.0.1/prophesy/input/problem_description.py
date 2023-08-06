from prophesy.data.hyperrectangle import HyperRectangle
from prophesy.data.interval import BoundType
import prophesy.adapter.pycarl as pc

class ProblemDescription:
    def __init__(self, solution_function=None, parameters=None, model=None, property=None, wd_constraints=None,
                 gp_constraints=None, threshold=None, samples=None):
        """
        Constructor.
        :param solutionfunction: Rational function representing reachability probability.
        :param parameters: Parameters occuring in model and solution function.
        :param model: Model.
        :param property: Property.
        :param wd_constraints: Constraints for well formedness.
        :param gp_constraints: Constraints for graph preservation.
        """
        self.solution_function = solution_function
        self.parameters = parameters
        self.model = model
        self.property = property
        self.welldefined_constraints = wd_constraints
        self.graph_preserving_constraints = gp_constraints
        self.samples = samples
        self.threshold = threshold
        self.monotonicity = None
        self.parameter_space = None

    def set_open01_parameter_space(self):
        self.parameter_space = HyperRectangle.cube(pc.Rational(0), pc.Rational(1), len(self.parameters), BoundType.open)

    def set_closed_epsilon_parameter_space(self, epsilon):
        self.parameter_space = HyperRectangle.cube(pc.Rational(epsilon), pc.Rational(1) - epsilon, len(self.parameters), BoundType.closed)

    def set_parameter_space_from_region_string(self, input):
        self.parameter_space = HyperRectangle.from_region_string(input, self.parameters)

