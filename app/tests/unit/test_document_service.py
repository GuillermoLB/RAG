# from unittest.mock import MagicMock, patch

# import pytest
# from sqlalchemy.orm import Session

# from app.dependencies import get_settings
# from app.services.document_service import embeddings, extract_document
# from app.services.extraction_service import LCDocument


# def test_extract_document_success():
#     # Arrange
#     mock_document = LCDocument(page_content="Mocked content")

#     with patch('app.services.document_service.extract_text', return_value=mock_document) as mock_extract_text, \
# patch('app.services.document_service.split_document_and_index_chunks')
# as mock_split_chunks:

#         mock_db = MagicMock(spec=Session)

#         # Act
#         extract_document(mock_db)

#         # Assert
#         settings = get_settings()
#         mock_extract_text.assert_called_once_with(settings.DATA_FILE_PATH)
#         mock_split_chunks.assert_called_once_with(
#             mock_db, mock_document, embeddings)


# def test_extract_document_failure():
#     # Arrange
#     with patch('app.services.document_service.extract_text', side_effect=Exception("Extraction failed")):
#         mock_db = MagicMock()

#         # Act & Assert
#         with pytest.raises(Exception) as exc_info:
#             extract_document(mock_db)
#         assert str(exc_info.value) == "Extraction failed"


# def test_extract_document_empty_input():
#     # Arrange
#     mock_document = MagicMock()
#     mock_document.page_content = ""

#     with patch('app.services.document_service.extract_text', return_value=mock_document) as mock_extract_text, \
# patch('app.services.document_service.split_document_and_index_chunks')
# as mock_split_chunks:

#         mock_db = MagicMock()

#         # Act
#         extract_document(mock_db)

#         # Assert
#         settings = get_settings()
#         mock_extract_text.assert_called_once_with(settings.DATA_FILE_PATH)
#         mock_split_chunks.assert_not_called()
