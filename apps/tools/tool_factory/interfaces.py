from abc import ABC, abstractmethod


class Tool(ABC):
    """
    Tool interface.

    Methods
    -------
    load_image_model()
        Abstract method to load the image model.
    process()
        Abstract method to process the image.
    """

    @abstractmethod
    def load_image_model(self):
        """
        Abstract method to load the image model.
        """

        pass

    @abstractmethod
    def process(self):
        """
        Abstract method to process the image.
        """

        pass
