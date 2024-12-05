from typing import Callable, Dict, Type

from src.api.services.base import BaseService


class ServiceRegistry:  # Singleton approach
    def __init__(self):
        self._services: Dict[Type[BaseService], BaseService] = {}
        self._dependency_factories: Dict[
            Type[BaseService], Callable[[], BaseService]
        ] = {}

    def register(self, service_type: Type[BaseService]) -> None:
        # Create instance
        self._services[service_type] = service_type()

        # Factory function to return stored instance
        def _get() -> BaseService:
            return self._services[service_type]

        # Store factory function
        self._dependency_factories[service_type] = _get

    def get(self, service_type: Type[BaseService]) -> Callable[[], BaseService]:
        # Return factory function, suitable for dependency injection
        return self._dependency_factories[service_type]


service_registry = ServiceRegistry()
