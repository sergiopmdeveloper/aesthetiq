from unittest.mock import Mock

import pytest

from apps.tools.factories.tool_factory import ToolFactory
from apps.tools.services.tool.modules.bg_remover import BackgroundRemover


@pytest.fixture(name="background_remover_mock")
def background_remover_mock_fixture() -> Mock:
    """
    Background remover mock fixture.

    Returns
    -------
    Client
        The background remover mock.
    """

    background_remover = ToolFactory[BackgroundRemover].create_service("background_remover")

    background_remover.load_image_model = Mock()
    background_remover.process = Mock(return_value=b"image")

    return background_remover
