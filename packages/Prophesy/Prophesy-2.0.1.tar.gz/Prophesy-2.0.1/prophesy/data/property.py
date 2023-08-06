import prophesy.adapter.pycarl as pc
import logging
from enum import Enum
import re

logger = logging.getLogger(__name__)

class OperatorType(Enum):
    """
    Are we interested in probability or in reward
    """
    probability = 0
    reward = 1
    time = 2

    def __str__(self):
        if self == OperatorType.probability:
            return "P"
        elif self == OperatorType.reward:
            return "R"
        else:
            return "T"

class OperatorDirection(Enum):
    min = 0
    max = 1
    unspecified = 2

    def __str__(self):
        if self == OperatorDirection.min:
            return "min"
        elif self == OperatorDirection.max:
            return "max"
        else:
            return ""

class OperatorBound:
    """
    Defines the operator bound. Can be left open to describe an operator bound which asks for the precise value. 
    """

    def __init__(self, relation=pc.Relation.EQ, threshold=None):
        """
        :param relation: The relation with which the actual probability is compared
        :type relation: pycarl.Relation
        :param threshold: The threshold 
        :type threshold: Any number type or None.
        """
        if not threshold and relation != pc.Relation.EQ:
            raise ValueError("If no threshold is given, the relation has to be '='")
        self.relation = relation
        self.threshold = threshold

    def asks_for_exact_value(self):
        """
        True if the bound describes the question for a precise boundary. 
        :return: 
        """
        return self.threshold is None

    def is_satisfied(self, value):
        """Return true if value is within the bound."""
        if self.relation == pc.Relation.LEQ:
            return value <= self.threshold
        elif self.relation == pc.Relation.GEQ:
            return value >= self.threshold
        elif self.relation == pc.Relation.LESS:
            return value < self.threshold
        elif self.relation == pc.Relation.GREATER:
            return value > self.threshold
        elif self.relation == pc.Relation.EQ:
            return value == self.threshold
        elif self.relation == pc.Relation.NEQ:
            return value != self.threshold
        else:
            raise ValueError("This bound has a really weird Relation: {}".format(self.relation))

    def __str__(self):
        if self.asks_for_exact_value():
            return "=?"
        return str(self.relation) + str(self.threshold)

    @classmethod
    def from_string(cls, input):
        """
        Parsing Prism-style operator bounds
        :param input: 
        :type input: str
        :return: the bound
        :rtype: OperatorBound
        """
        if input[:2] == "<=":
            relation = pc.Relation.LEQ
            input = input[2:]
        elif input[:2] == ">=":
            relation = pc.Relation.GEQ
            input = input[2:]
        elif input[:2] == "!=":
            relation = pc.Relation.NEQ
            input = input[2:]
        elif input[0] == "<":
            relation = pc.Relation.LESS
            input = input[1:]
        elif input[0] == ">":
            relation = pc.Relation.GREATER
            input = input[1:]
        elif input[0] == "=":
            relation = pc.Relation.EQ
            if input[1] == "?":
                return cls()
            input = input[2:]
        else:
            raise ValueError("Cannot parse {} as a bound.".format(input))
        threshold = pc.Rational(input)
        return cls(relation, threshold)

class Property:
    """
    
    """
    def __init__(self, operator_type, operator_direction, reward_name, bound, pathformula):
        """
        
        :param operator_type: 
        :type operator_type: OperatorType
        :param bound: 
        :type bound: OperatorBound
        :param pathformula: 
        """
        self.operator = operator_type
        self.operator_direction = operator_direction
        self.reward_name = reward_name
        self.bound = bound
        self.pathformula = pathformula

    @classmethod
    def from_string(cls, input_string):
        """
        Parses prism-style properties
        :param input_string: 
        :type input_string: str
        :return: 
        :rtype: Property
        """
        logger.debug("Parsing {}".format(input_string))

        orig_input_string = input_string.strip()
        input_string = re.sub(r"[\{].*[\}]", "", orig_input_string)
        if input_string[:4] == "Pmin":
            input_string = input_string[4:]
            operator_direction = OperatorDirection.min
            operator_type = OperatorType.probability
        elif input_string[:4] == "Pmax":
            input_string = input_string[4:]
            operator_direction = OperatorDirection.max
            operator_type = OperatorType.probability
        elif input_string[:1] == "P":
            input_string = input_string[1:]
            operator_direction = OperatorDirection.unspecified
            operator_type = OperatorType.probability
        elif input_string[:4] == "Rmin":
            input_string = input_string[4:]
            operator_direction = OperatorDirection.min
            operator_type = OperatorType.reward
        elif input_string[:4] == "Rmax":
            input_string = input_string[4:]
            operator_direction = OperatorDirection.max
            operator_type = OperatorType.reward
        elif input_string[:1] == "R":
            input_string = input_string[1:]
            operator_direction = OperatorDirection.unspecified
            operator_type = OperatorType.reward
        elif input_string[:4] == "Tmin":
            input_string = input_string[4:]
            operator_direction = OperatorDirection.min
            operator_type = OperatorType.time
        elif input_string[:4] == "Tmax":
            input_string = input_string[4:]
            operator_direction = OperatorDirection.max
            operator_type = OperatorType.time
        elif input_string[:1] == "T":
            input_string = input_string[1:]
            operator_direction = OperatorDirection.unspecified
            operator_type = OperatorType.time
        else:
            ValueError("Expect property {} to start with P/Pmin/Pmax/R/Rmin/Rmax/T/Tmin/Tmax".format(input_string))

        reward_name = None
        if operator_type == OperatorType.reward:
            if input_string[0:5] == "[exp]":
                logger.debug("Drop reward expectation")
                input_string = input_string[5:]

            if input_string[0] == "{":
                reward_name = input_string[2:].split('}', 1)[0][:-1]
                input_string = input_string[4+len(reward_name):]
                logger.debug("Found reward name: {}".format(reward_name))

            if input_string[0:3] == "min":
                operator_direction = OperatorDirection.min
                input_string = input_string[3:]
            elif input_string[0:3] == "max":
                operator_direction = OperatorDirection.max
                input_string = input_string[3:]
        operator_bound = OperatorBound.from_string(input_string.split(" ", 1)[0])


        input_string = input_string.split(" ",1)[1].strip()



        return cls(operator_type, operator_direction, reward_name, operator_bound, input_string)

    def __str__(self):
        return str(self.operator) + ("{\"" + self.reward_name + "\"}" if self.reward_name else "") + str(self.operator_direction) + str(self.bound) + " " + self.pathformula


