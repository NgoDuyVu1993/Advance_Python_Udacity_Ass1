"""Provide filters for querying close approaches and limit the generated results.

The `create_filters` function produces a collection of objects that is used by
the `query` method to generate a stream of `CloseApproach` objects that match
all of the desired criteria. The arguments to `create_filters` are provided by
the main module and originate from the user's command-line options.

This function can be thought to return a collection of instances of subclasses
of `AttributeFilter` - a 1-argument callable (on a `CloseApproach`) constructed
from a comparator (from the `operator` module), a reference value, and a class
method `get` that subclasses can override to fetch an attribute of interest from
the supplied `CloseApproach`.

The `limit` function simply limits the maximum number of values produced by an
iterator.

You'll edit this file in Tasks 3a and 3c.
"""
import operator

class FilterNotSupported(Exception):
    """Exception raised when an attempt is made to use an unsupported filter criterion."""
    pass

class GeneralFilter:
    """Base class for filtering attributes of CloseApproach objects.

    This class is designed to be subclassed for specific attributes to filter.
    """

    def __init__(self, comparator, ref_value):
        """Initialize the filter with a comparator function and a reference value.

        Args:
            comparator: A function from the operator module that compares two values.
            ref_value: The reference value to compare against.
        """
        self.comparator = comparator
        self.ref_value = ref_value

    def __call__(self, approach):
        """Make the filter class instances callable.

        Args:
            approach: The CloseApproach object to filter.

        Returns:
            The result of applying the comparator to the attribute and the reference value.
        """
        attribute = self.extract_attribute(approach)
        return self.comparator(attribute, self.ref_value)

    @classmethod
    def extract_attribute(cls, approach):
        """Extract the attribute from the CloseApproach object.

        This method should be overridden by subclasses to extract the specific attribute.

        Args:
            approach: The CloseApproach object to extract the attribute from.

        Raises:
            FilterNotSupported: If the subclass does not implement this method.
        """
        raise FilterNotSupported(f"{cls.__name__} does not support extracting an attribute.")

    def __str__(self):
        """String representation of the filter.

        Returns:
            A string that represents the filter, including its class name, comparator, and reference value.
        """
        return f"{self.__class__.__name__}(comparator=operator.{self.comparator.__name__}, ref_value={self.ref_value})"

# Subclasses for each filter type follow. Each subclass overrides the extract_attribute method
# to return the relevant attribute from the CloseApproach object.

class DateFilter(GeneralFilter):
    @classmethod
    def extract_attribute(cls, approach):
        """Extract the date from the CloseApproach object."""
        return approach.time.date()

class DistanceFilter(GeneralFilter):
    @classmethod
    def extract_attribute(cls, approach):
        """Extract the distance from the CloseApproach object."""
        return approach.distance

class VelocityFilter(GeneralFilter):
    @classmethod
    def extract_attribute(cls, approach):
        """Extract the velocity from the CloseApproach object."""
        return approach.velocity

class DiameterFilter(GeneralFilter):
    @classmethod
    def extract_attribute(cls, approach):
        """Extract the diameter from the NEO of the CloseApproach object."""
        return approach.neo.diameter

class HazardFilter(GeneralFilter):
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
    """Create a list of filter objects based on the provided criteria.

    Args:
        date: Exact date to match.
        start_date: Minimum date to match.
        end_date: Maximum date to match.
        distance_min: Minimum distance to match.
        distance_max: Maximum distance to match.
        velocity_min: Minimum velocity to match.
        velocity_max: Maximum velocity to match.
        diameter_min: Minimum diameter to match.
        diameter_max: Maximum diameter to match.
        hazardous: Whether to match on the hazardous attribute.

    Returns:
        A list of initialized filter objects that can be used to filter CloseApproach objects.
    """
    filter_list = []

    # Dictionary mapping the filter names to their respective classes, operators, and values.
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

    # Iterate over the criteria dictionary and create filter objects for each non-None criterion.
    for key, (FilterClass, op, value) in criteria.items():
        if value is not None:
            filter_list.append(FilterClass(op, value))

    return filter_list

def limit(iterator, max_elements=None):
    """Limit the number of items produced by an iterator.

    Args:
        iterator: The iterator to limit.
        max_elements: The maximum number of elements to produce.

    Returns:
        An iterator that produces at most `max_elements` items.
    """
    if max_elements is None or max_elements == 0:
        return iterator
    else:
        # Otherwise, we return an iterator that stops after max_elements items.
        return (item for idx, item in enumerate(iterator) if idx < max_elements)

