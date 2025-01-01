from typing import Generic, TypeVar

from apps.tools.services.tool.interfaces import Tool
from apps.tools.services.tool.modules.bg_remover import BackgroundRemover

T = TypeVar("T", bound=Tool)


class ToolFactory(Generic[T]):
    """
    Tool factory.

    Attributes
    ----------
    _SERVICES : dict[str, Tool]
        The tool services.

    Methods
    -------
    create_service(service_type: str) -> T
        Creates a new tool service.
    """

    _SERVICES: dict[str, Tool] = {
        "background_remover": BackgroundRemover,
    }

    @classmethod
    def create_service(cls, service_type: str) -> T:
        """
        Creates a new tool service.

        Parameters
        ----------
        service_type : str
            The tool service to create.

        Returns
        -------
        T
            The initialized tool service.
        """

        tool_service = cls._SERVICES.get(service_type)

        if not tool_service:
            raise ValueError(f"Invalid tool: {service_type}")

        return tool_service()
