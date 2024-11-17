import typer
import logging
import pytz
import filecmp
import json
import os

from pathlib import Path
from datetime import datetime
from typing_extensions import Annotated

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = typer.Typer()


def clean_folders(folder: Path):
    """
    Deletes empty directories within the given folder.

    Args:
        folder (Path): The root folder to search for empty directories.

    Returns:
        None
    """
    # Check if it is a directory and is empty
    if folder.is_dir():
        for item in folder.iterdir():
            if item.is_dir():
                clean_folders(item)
        if not any(folder.iterdir()):
            folder.rmdir()
            logger.info(f"Deleted empty directory: {folder}")
        else:
            logger.info(f"Directory {folder} is not empty, cannot delete")
    else:
        logger.debug(f"Folder {folder} is not a directory")
    


def get_destination_path(file_path: Path, target: Path) -> Path:
    """
    Gets the destination path for the file based on the creation and modified times.

    Args:
        file_path (Path): The path to the file.
        target (Path): The target directory.

    Returns:
        Path: The destination path for the file.
    """
    creation_time = (datetime.fromtimestamp(file_path.stat().st_ctime, tz=pytz.UTC)
        .astimezone(pytz.timezone('America/Los_Angeles')))
    modified_time = (datetime.fromtimestamp(file_path.stat().st_mtime, tz=pytz.UTC)
        .astimezone(pytz.timezone('America/Los_Angeles')))
    
    logger.info(f"Found file: {file_path}, Creation time: {creation_time.strftime('%Y-%m-%d %H:%M:%S')}, Modified time: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}")

    target_directory = Path(target, creation_time.strftime("%Y"), creation_time.strftime("%B")[0:3], f"{creation_time.month}-{creation_time.day}")
    destination_path = target_directory / file_path.name
    target_directory.mkdir(parents=True, exist_ok=True)

    return destination_path

def all(
    source: Annotated[Path, typer.Argument(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=True,
        help="The source directory where the files will be read from.",
    )],
    target: Annotated[Path, typer.Argument(
        exists=False,
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=True,
        help="The target directory where the files will be moved to.",
    )],
):
    """
    Organizes files in the specified folder by year and date.

    Args:
        source (Path): The folder path where the files will be read from.
        target (Path): The folder path where the files will be moved to.

    Returns:
        None
    """
    logger.info(f"Organizing files in {source} to {target}")
    target.mkdir(parents=True, exist_ok=True)
    with open(target / "errors.jsonl", "w") as f:
        for file_path in source.rglob('*'):
            if file_path.is_file() and file_path.name.startswith('.'):
                logger.info(f"Removing hidden file: {file_path}")
                file_path.unlink()
                continue
            if file_path.is_file():
                destination_path = get_destination_path(file_path, target)
                logger.info(f"Moving file {file_path} to {destination_path}")
                try:
                    if destination_path.exists():
                        logger.info(f"File {destination_path} already exists, overriding if equal")
                        if filecmp.cmp(file_path, destination_path, shallow=False):
                            logger.info(f"File {destination_path} is equal, sending to trash")
                            target_trash_directory = target / 'trash'
                            target_trash_directory.mkdir(parents=True, exist_ok=True)
                            trash_path = target_trash_directory / file_path.name
                            if not trash_path.exists():
                                file_path.rename(trash_path)
                                logger.info(f"File moved to trash at {trash_path}")
                            elif filecmp.cmp(file_path, trash_path, shallow=False):
                                logger.info(f"File {trash_path} already exists in trash and is equal, will delete")
                                file_path.unlink()
                            else:
                                logger.info(f"File is not equal to {trash_path}, not doing anything, need manual intervention")
                                f.write(json.dumps({
                                    "source": str(file_path),
                                    "destination": str(trash_path),
                                    "reason": "already exists in trash as different file",
                                }) + "\n")
                        else:
                            logger.info(f"File {file_path} is not equal to {destination_path}, not doing anything, need manual intervention")
                            f.write(json.dumps({
                                "source": str(file_path),
                                "destination": str(destination_path),
                                "reason": "already exists in destination as different file",
                            }) + "\n")
                    else:
                        logger.info(f"File {destination_path} does not exist, moving")
                        file_path.rename(destination_path)
                except Exception as e:
                    logger.error(f"Error moving file: {e}")
        f.flush()
        os.fsync(f.fileno()) 
    clean_folders(source)

def main() -> None:
    """
    Main function to run the application.
    """
    typer.run(all)

if __name__ == "__main__":
    main()