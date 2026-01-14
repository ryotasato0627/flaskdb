import pytest
from unittest.mock import Mock, MagicMock
from app.services.note import NoteService
from app.models.note import Note

def test_create_note_service():
    # Arrange
    mock_repo = MagicMock()
    mock_note = MagicMock(id=1, title="Test Note", content="This is a test note.", user_id=1)
    mock_repo.create_note.return_value = mock_note

    service = NoteService(note_repo=mock_repo)

    # Act
    result = service.create_note(title="Test Note", content="This is a test note.", user_id=1)

    # Assert
    assert result == mock_note
    mock_repo.create_note.assert_called_once_with(
        "Test Note",
        "This is a test note.",
        1
    )
