from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO) with its properties and associated close approaches."""

    def __init__(self, **info):
        """Create a new `NearEarthObject` with the given info."""
        self.designation = info.get('designation', '')
        self.name = info.get('name', None)
        try:
            self.diameter = float(info.get('diameter')) if info.get('diameter') else float('nan')
        except ValueError:
            self.diameter = float('nan')
        self.hazardous = bool(info.get('hazardous', False))
        self.approaches = []

    @property
    def fullname(self):
        """Return the full name of the NEO, which is its designation and name."""
        return f"{self.designation} ({self.name})" if self.name else self.designation

    def __str__(self):
        """Return a human-readable string representation of the NEO."""
        return (f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km and "
                f"{'is' if self.hazardous else 'is not'} hazardous.")

    def __repr__(self):
        """Return a computer-readable string representation of the NEO."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")

    def serialize(self):
        """Serialize the NEO data into a dictionary for CSV or JSON serialization."""
        return {
            'designation': self.designation,
            'name': self.name if self.name else '',
            'diameter_km': self.diameter if self.diameter is not float('nan') else 'nan',
            'potentially_hazardous': self.hazardous
        }


class CloseApproach:
    """A close approach to Earth by an NEO."""

    def __init__(self, **info):
        """Create a new `CloseApproach` with the given info."""
        self._designation = info.get('designation', '')
        datetime_str = info.get('datetime')
        self.time = cd_to_datetime(datetime_str) if datetime_str else None
        self.distance = float(info.get('distance', 0.0))
        self.velocity = float(info.get('velocity', 0.0))
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of the approach time."""
        return datetime_to_str(self.time)

    def __str__(self):
        """Return a human-readable string representation of the CloseApproach."""
        return (f"At {self.time_str}, {self._designation} approaches Earth at a distance of "
               
