class ServiceRegistry:  # Singleton approach
    def __init__(self):
        self._services = {}
        self._dependency_factories = {}

    def register(self, service_type):
        self._services[service_type] = service_type()

        def _get():
            return self._services[service_type]

        self._dependency_factories[service_type] = _get

    def get(self, service_type):
        return self._dependency_factories[service_type]


service_registry = ServiceRegistry()
