import pytest
from fastapi import UploadFile
from app.ocr import extract_text_from_image
from unittest.mock import MagicMock
import io

@pytest.mark.asyncio
async def test_extract_text_from_image():
    # Prepare a fake image file (replace 'sample.png' with your test image path)
    with open('app/sample.png', 'rb') as f:
        file_bytes = f.read()

    async def async_read():
        return file_bytes

    mock_upload_file = MagicMock(spec=UploadFile)
    mock_upload_file.read = async_read  # async function

    # Call the OCR function
    text = await extract_text_from_image(mock_upload_file)
    # Assert that some text is returned (adjust as needed for your test image)
    assert isinstance(text, str)
    assert len(text) > 0 