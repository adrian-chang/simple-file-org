import typer
import logging
import pytz

from typing_extensions import Annotated
from pathlib import Path
from datetime import datetime, timedelta

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
    for subdir in folder.rglob('*'):
        # Check if it is a directory and is empty
        if subdir.is_dir() and not any(subdir.iterdir()):
            subdir.rmdir()
            logger.info(f"Deleted empty directory: {subdir}")
        else:
            logger.debug(f"Directory {subdir} is not empty or {subdir} is not a directory")


def move_files(folder: Path, read_target: Path = None):
    """
    Moves files in the root folder to their respective directories.

    Args:
        folder (Path): The root folder to search for files.

    Returns:
        None
    """
    if read_target is None:
        read_target = folder
    for file_path in read_target.rglob('*'):
        if file_path.is_file():
            logger.info(f"Found file: {file_path}")
            creation_time_str = (datetime.fromtimestamp(file_path.stat().st_ctime, tz=pytz.UTC)
                .astimezone(pytz.timezone('America/Los_Angeles'))
                .strftime('%Y-%m-%d %H:%M:%S'))
            logger.info(f"Creation time: {creation_time_str}")

            modified_time = (datetime.fromtimestamp(file_path.stat().st_mtime, tz=pytz.UTC)
                .astimezone(pytz.timezone('America/Los_Angeles')))
            logger.info(f"Modified time: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}")

            target_directory = Path(folder, modified_time.strftime("%B")[0:3], f"{modified_time.month}-{modified_time.day}")
            destination_path = target_directory / file_path.name
            logger.info(f"Moving file {file_path} to {destination_path}")
            try:
                if destination_path.exists():
                    logger.info(f"File {destination_path} already exists")
                else:
                    file_path.rename(destination_path)
            except Exception as e:
                logger.error(f"Error moving file: {e}")


@app.command()
def all(
    start: datetime,
    folder: Path = typer.Argument(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=True,
    ),
):
    """
    Organizes files in the specified folder by year and date.

    Args:
        start (datetime): The starting date for organizing the files.
        folder (Path): The folder path where the files will be organized.

    Returns:
        None
    """
    start = start.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    logger.info(f"Organizing files in {folder} by year")
    logger.info(f"Starting from date {start}")
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    while start <= today:
        target_directory = Path(folder, str(start.year), start.strftime("%B")[0:3], f"{start.month}-{start.day}")
        if target_directory.exists():
            logger.info(f"Directory {target_directory} already exists")
        else:
            logger.info(f"Creating directory {target_directory}")
            target_directory.mkdir(parents=True, exist_ok=True)
        start = start + timedelta(days=1)

    move_files(folder)
    clean_folders(folder)
    

@app.command()
def year(
    start: datetime,
    folder: Path = typer.Argument(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=True,
    ),
):
    """
    Organizes files in the specified folder by year.

    Args:
        start (datetime): The starting date for organizing files.
        folder (Path): The folder path to organize the files in.

    Returns:
        None
    """
    start = start.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    logger.info(f"Organizing files in {folder} by year")
    logger.info(f"Starting from date {start}")
    next_year = start.year + 1

    while start.year < next_year:
        target_directory = Path(folder, str(start.year), start.strftime("%B")[0:3], f"{start.month}-{start.day}")
        if target_directory.exists():
            logger.info(f"Directory {target_directory} already exists")
        else:
            logger.info(f"Creating directory {target_directory}")
            target_directory.mkdir(parents=True, exist_ok=True)
        start = start + timedelta(days=1)

    start = start - timedelta(days=1)
    folder = folder / str(start.year)
    move_files(folder)  
    clean_folders(folder)


@app.command()
def month(
    start: datetime,
    folder: Path = typer.Argument(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=True,
    ),
):
    """
    Organizes files in a folder for a specific month.

    Args:
        start (datetime): The starting date for organizing the files.
        folder (Path): The path to the folder containing the files to be organized.

    Returns:
        None
    """
    start = start.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    logger.info(f"Organizing files in {folder} by month")
    logger.info(f"Starting from date {start}")
    next_month = start.month + 1

    while start.month < next_month:
        target_directory = Path(folder, start.strftime("%B")[0:3], f"{start.month}-{start.day}")
        if target_directory.exists():
            logger.info(f"Directory {target_directory} already exists")
        else:
            logger.info(f"Creating directory {target_directory}")
            target_directory.mkdir(parents=True, exist_ok=True)
        start = start + timedelta(days=1)

    start = start - timedelta(days=1)
    move_files(folder, folder / start.strftime("%B")[0:3])
    clean_folders(folder / start.strftime("%B")[0:3])

if __name__ == "__main__":
    app()
