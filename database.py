class NEODatabase:
    """
    A database of near-Earth objects and their close approaches to Earth.

    This class holds a collection of `NearEarthObject`s and a collection of `CloseApproach`es
    and provides methods to fetch an object by its primary designation or by its name and to
    query the dataset for a collection of `CloseApproach`es that match a collection of user-provided filters.
    """

    def __init__(self, neos, approaches):
        """
        Create a new `NEODatabase`.

        :param neos: A list of `NearEarthObject`s.
        :param approaches: A list of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches
        
        # Indexing by Designation and Name
        self._neo_idx_by_designation = {neo.designation: idx for idx, neo in enumerate(neos)}
        self._neo_idx_by_name = {neo.name: idx for idx, neo in enumerate(neos) if neo.name}

        # Linking Approaches to NEOs
        for approach in self._approaches:
            neo = self.get_neo_by_designation(approach._designation)
            if neo:
                approach.neo = neo
                neo.approaches.append(approach)

    def get_neo_by_designation(self, designation):
        """
        Find and return an NEO by its primary designation.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the given primary designation, or `None`.
        """
        idx = self._neo_idx_by_designation.get(designation, -1)
        return self._neos[idx] if idx >= 0 else None

    def get_neo_by_name(self, name):
        """
        Find and return an NEO by its name.

        :param name: The name of the NEO to search for.
        :return: The `NearEarthObject` with the given name, or `None`.
        """
        idx = self._neo_idx_by_name.get(name, -1)
        return self._neos[idx] if idx >= 0 else None

    def query(self, filters=()):
        """
        Query close approaches to generate those that match a collection of filters.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A generator of `CloseApproach`es that match all of the provided filters.
        """
        for approach in self._approaches:
            if all(f(approach) for f in filters):
                yield approach
