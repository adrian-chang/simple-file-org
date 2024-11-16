import tempfile

from pathlib import Path
from simple_file_org.main import all
from datetime import datetime

def test_all():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir_source:
        with tempfile.TemporaryDirectory() as temp_dir_target:
            temp_path_source = Path(temp_dir_source)
            temp_path_target = Path(temp_dir_target)
            
            # Create a test file in the temporary directory
            test_file = temp_path_source / "test.txt"
            test_file.write_text("test content")
            
            # Call the main function with the temp directory
            all(temp_path_source, temp_path_target)
            
            # Add assertions here based on what main() is expected to do
            now = datetime.now()
            expected_destination = Path(temp_path_target, now.strftime("%Y"), now.strftime("%B")[0:3], f"{now.month}-{now.day}")
            assert expected_destination.exists()
            assert (expected_destination / "test.txt").exists()
