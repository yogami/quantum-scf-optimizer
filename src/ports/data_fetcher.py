from abc import ABC, abstractmethod

class DataFetcherPort(ABC):
    @abstractmethod
    def get_topology_nodes(self):
        """Fetches grid topology nodes."""
        pass
