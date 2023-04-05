from dataclasses import dataclass, field
from typing import Generator

from _anvil_designer.common_structures import *
from ... import Media


@dataclass
class DriveItem:
    id: String = field(default_factory=String)  # ID of the DriveItem

    def delete(self):
        """Delete the DriveItem (this cannot be undone)"""
        pass

    def move(self, dest_folder):
        """Move the DriveItem from one folder to another"""
        pass

    def trash(self):
        """Move the DriveItem to the trash folder"""
        pass


@dataclass
class File(DriveItem, Media):
    def get_bytes(self):
        """Get the contents of an object representing a Google Drive file. Native Google files such as Docs,
        Slides and Sheets must first be exported to an appropriate file type. All other file types support get_bytes(
        )."""
        pass

    def set_bytes(self, content):
        """Set the contents of an object representing a Google Drive file."""
        pass

    def set_media(self, media):
        """Upload new contents to an existing File. Media must be a Media object."""
        pass


@dataclass
class Folder(DriveItem):
    files: list = field(default_factory=list)
    folders: list = field(default_factory=list)

    def create_file(self, title, content_bytes=None, content_type='text/plain'):
        """Create a new file within the Folder."""
        pass

    def create_folder(self, title):
        """Create a new folder within the Folder."""
        pass

    def get(self, title: str) -> File:
        """Get the File item by title. The title argument should be a string."""
        pass

    def get_by_id(self, id) -> File:
        """Get the File item by ID. The ID argument should be a string."""
        pass

    def list_files(self) -> Generator[File]:
        """List the files (not folders) in the Folder."""
        pass

    def list_folders(self) -> Generator[File]:
        """List the folders (not files) in the Folder."""


def get_user_files() -> Folder:
    """Return the top-level folder containing all the files in the Users drive. anvil.google.drive.login() must be
    called first."""
    pass


def login(extra_scopes=None):
    """Prompt the user to log in to their Google account and ask permission to access their Google Drive files."""
    pass
