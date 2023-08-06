import logging
from enum import Enum
from prophesy.smt.smt import Answer
import prophesy.adapter.pycarl as pc

logger = logging.getLogger(__name__)


class WelldefinednessResult(Enum):
    Welldefined = 0
    Undecided = 1
    Illdefined = 2


def is_welldefined(result):
    return result == WelldefinednessResult.Welldefined

def check_welldefinedness(checker, parameters, region, constraints):
    """

    :param checker:
    :param parameters:
    :param region:
    :param constraints:
    :rtype: WelldefinednessResult
    :return:
    """
    for p in parameters:
        checker.add_variable(p.name)
    checker.assert_constraint(region.to_formula(parameters))
    welldefinedness = pc.Constraint(True)
    checker.push()
    for c in constraints:
        welldefinedness = (welldefinedness & c)
    checker.assert_constraint(~welldefinedness)
    result = checker.check()
    if result == Answer.sat:
        logger.debug("Part of the region %s is ill-defined.", str(region))
        checker.pop()
        checker.assert_constraint(welldefinedness)
        result = checker.check()
        if result == Answer.sat:
            logger.debug("Region %s is neither well- nor ill-defined.", str(region))
            return WelldefinednessResult.Undecided
        elif result == Answer.unsat:
            logger.debug("Region %s is ill-defined.", str(region))
            return WelldefinednessResult.Illdefined
    elif result == Answer.unsat:
        logger.debug("Region %s is well-defined.", str(region))
        return WelldefinednessResult.Welldefined
    elif result == Answer.unknown:
        raise RuntimeError("Unknown answers for well-definedness-checks are currently not supported")


class SampleWelldefinedChecker():
    def __init__(self, checker, parameters, constraints):
        """
        
        :param checker: 
        :param parameters: 
        :param constraints: 
        """
        self.checker = checker
        self.parameters = parameters
        self.contraints = constraints
        for p in self.parameters:
            self.checker.add_variable(p.variable)

        for c in self.contraints:
            self.checker.assert_constraint(c)

    def check(self, sample):
        logger.debug("Check %s", sample)
        formula = sample.to_formula()
        self.checker.push()
        self.checker.assert_constraint(formula)
        check_result = self.checker.check()
        if check_result == Answer.sat:
            result = WelldefinednessResult.Welldefined
        elif check_result == Answer.unsat:
            result = WelldefinednessResult.Illdefined
        elif check_result == Answer.unknown:
            raise RuntimeError("Unknown answers for well-definedness-checks are currently not supported")
        self.checker.pop()

        logger.debug("Checked %s, result: %s", sample, result)
        return result

