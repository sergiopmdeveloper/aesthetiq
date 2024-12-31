from typing import Generic, TypeVar

from apps.tools.tool_factory.interfaces.tool import Tool
from apps.tools.tool_factory.tools.background_remover import BackgroundRemover

T = TypeVar("T", bound=Tool)


class ToolFactory(Generic[T]):
    """
    Tool factory.
    """

    @staticmethod
    def create_tool(tool: str) -> T:
        """
        Creates a tool.

        Parameters
        ----------
        tool : str
            The tool to create.

        Returns
        -------
        T
            The created tool.
        """

        factories = {
            "background_remover": BackgroundRemover,
        }

        factory = factories.get(tool)

        if not factory:
            raise ValueError(f"Invalid tool type: {tool}")

        return factory()
