from pathlib import Path


ASSETS_FOLDER_PATH = f"{Path(__file__).parent.parent.absolute()}/assets"
DEFAULT_IMAGE = ASSETS_FOLDER_PATH + "/default.png"


class Image:
    """
    Stores the information of an image such as a name and file location.

    :param image_name: Optional[str]
        The image name.
    :param file_location: Optional[str]
        The absolute or relative file location.
    """
    def __init__(self, image_name=None, file_location=None):
        self.image_name = image_name or "DEFAULT"
        self.file_location = file_location or DEFAULT_IMAGE
