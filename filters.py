import operator


class FilterNotSupported(Exception):
    """Exception raised for unsupported filter criteria."""
    pass


class GeneralFilter:
    """A general filter class to apply a comparison to an attribute of an approach."""

    def __init__(self, comparator, ref_value):
        """Initialize the filter with a comparator function and a reference value."""
        self.comparator = comparator
        self.ref_value = ref_value

    def __call__(self, approach):
        """Apply the filter to an approach."""
        attribute = self.extract_attribute(approach)
        return self.comparator(attribute, self.ref_value)

    @classmethod
    def extract_attribute(cls, approach):
        """Raise an exception as this method is intended to be overridden by subclasses."""
        raise FilterNotSupported(f"{cls.__name__} does not support extracting an attribute.")

    def __str__(self):
        """Return a string representation of the filter."""
        comparator_name = self.comparator.__name__
        return f"{self.__class__.__name__}(comparator=operator.{comparator_name}, ref_value={self.ref_value})"


# Subclasses for each filter type follow, overriding the extract_attribute method.

class DateFilter(GeneralFilter):
    """Filter based on the date of close approach."""

    @classmethod
    def extract_attribute(cls, approach):
        """Extract the date from the CloseApproach object."""
        return approach.time.date()


class DistanceFilter(GeneralFilter):
    """Filter based on the distance of close approach."""

    @classmethod
    def extract_attribute(cls, approach):
        """Extract the distance from the CloseApproach object."""
        return approach.distance


class VelocityFilter(GeneralFilter):
    """Filter based on the velocity of close approach."""

    @classmethod
    def extract_attribute(cls, approach):
        """Extract the velocity from the CloseApproach object."""
        return approach.velocity


class DiameterFilter(GeneralFilter):
    """Filter based on the diameter of the NEO."""

    @classmethod
    def extract_attribute(cls, approach):
        """Extract the diameter from the NEO of the CloseApproach object."""
        return approach.neo.diameter


class HazardFilter(GeneralFilter):
    """Filter based on whether the NEO is potentially hazardous."""

    @classmethod
    def extract_attribute(cls, approach):
        """Extract the hazardous flag from the NEO of the CloseApproach object."""
        return approach.neo.hazardous


def create_filters(
    date=None, start_date=None, end_date=None,
    distance_min=None, distance_max=None,
    velocity_min=None, velocity_max=None,
    diameter_min=None, diameter_max=None,
    hazardous=None
):
    """Create a list of filter objects based on provided criteria."""
    filter_list = []

    # Mapping of filter names to their respective classes, operators, and values.
    criteria = {
        'date': (DateFilter, operator.eq, date),
        'start_date': (DateFilter, operator.ge, start_date),
        'end_date': (DateFilter, operator.le, end_date),
        'distance_min': (DistanceFilter, operator.ge, distance_min),
        'distance_max': (DistanceFilter, operator.le, distance_max),
        'velocity_min': (VelocityFilter, operator.ge, velocity_min),
        'velocity_max': (VelocityFilter, operator.le, velocity_max),
        'diameter_min': (DiameterFilter, operator.ge, diameter_min),
        'diameter_max': (DiameterFilter, operator.le, diameter_max),
        'hazardous': (HazardFilter, operator.eq, hazardous),
    }

    for key, (FilterClass, op, value) in criteria.items():
        if value is not None:
            filter_list.append(FilterClass(op, value))

    return filter_list


def limit(iterator, max_elements=None):
    """Limit the number of elements in an iterator to max_elements."""
    if max_elements is None or max_elements == 0:
        return iterator
    else:
        return (item for idx, item in enumerate(iterator) if idx < max_elements)
