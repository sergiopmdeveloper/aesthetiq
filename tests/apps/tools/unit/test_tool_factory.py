import pytest

from apps.tools.factories.tool_factory import ToolFactory
from apps.tools.services.tool.modules.bg_remover import BackgroundRemover


def test_tool_factory_service_not_found():
    """
    GIVEN an invalid tool service type
    WHEN create_service function is called
    THEN a ValueError is raised
    """

    # Arrange
    tool_factory = ToolFactory()

    # Act
    with pytest.raises(ValueError) as e:
        tool_factory.create_service("invalid_tool")

    # Assert
    assert str(e.value) == "Invalid tool: invalid_tool"


def test_tool_factory_service_found():
    """
    GIVEN a valid tool service type
    WHEN create_service function is called
    THEN the initialized tool service is returned
    """

    # Arrange
    tool_factory = ToolFactory()

    # Act
    result = tool_factory.create_service("background_remover")

    # Assert
    assert isinstance(result, BackgroundRemover)
