import pytest
from unittest.mock import MagicMock
from app.services.note import NoteService
from tests.dummy.dummy_note import DummyNote

class TestNoteService:
    @pytest.fixture
    def mock_note_repo(self):
        return MagicMock()

    @pytest.fixture
    def note_service(self, mock_note_repo):
        return NoteService(note_repo=mock_note_repo)
    
    @pytest.fixture
    def sample_note(self):
        return DummyNote()
    
    class TestGetAllNotes:
        def test_get_all_notes_success(self, note_service, mock_note_repo):
            # Arrange
            expected_notes = [DummyNote(1, "タイトル1", "コンテンツ1", 100), DummyNote(2, "タイトル2", "コンテンツ2", 101)]
            mock_note_repo.get_all_notes.return_value = expected_notes

            # Act
            result = note_service.get_all_notes()

            # Assert
            assert result == expected_notes
            mock_note_repo.get_all_notes.assert_called_once()

    class TestGetNoteById:
        def test_get_note_by_id_success(self, note_service, mock_note_repo, sample_note):
            # Arrange
            note_id = 1
            expended_note = DummyNote(id=note_id, title="タイトル1", content="コンテンツ1", user_id=100)
            mock_note_repo.get_note_by_id.return_value = expended_note

            # Act
            result = note_service.get_note_by_id(note_id)

            # Assert
            assert result == expended_note
            mock_note_repo.get_note_by_id.assert_called_once_with(note_id)

    class TestCreateNote:
        def test_create_note_success(self, note_service, mock_note_repo):
            # Arrange
            user_id = 100
            title = "テストタイトル"
            content = "テストコンテント"
            created_note = DummyNote(
                id = 1,
                title = title,
                content = content,
                user_id = user_id
            )

            mock_note_repo.create_note.return_value = created_note

            # Act
            result = note_service.create_note(user_id, title, content)

            # Assert
            assert result == created_note
            mock_note_repo.create_note.assert_called_once_with(title, content, user_id)

        @pytest.mark.parametrize(
            "title, content",
            [
                ("", "content"),
                ("title", ""),
                (None, "content"),
                ("title", None),
            ]
        )
        def test_create_note_value_error(self, note_service, title, content):
            # Arrange
            user_id = 100

            # Act & Assert
            with pytest.raises(ValueError):
                note_service.create_note(user_id, title, content)
            
    class TestUpdateNote:
        def test_update_note_success(self, note_service, mock_note_repo, sample_note):
            # Arrange
            note_id = 1
            user_id = 100
            updated_title = "update title"
            updated_content = "update content"
            exisiting_note = DummyNote(
                id = note_id,
                title = "test title",
                content = "test content",
                user_id = user_id
            )

            updated_note = DummyNote(
                id = note_id,
                title = updated_title,
                content = updated_content,
                user_id = user_id
            )


            mock_note_repo.get_note_by_id.return_value = exisiting_note
            mock_note_repo.update_note.return_value = updated_note

            # Act
            result = note_service.update_note(user_id, note_id, updated_title, updated_content)

            # Assert
            assert result == updated_note
            mock_note_repo.update_note.assert_called_once_with(note_id, updated_title, updated_content)

        def test_update_note_permission_error(self, note_service, mock_note_repo):
            # Arrange
            note_id = 1
            user_id = 100

            other_user_note = DummyNote(
                id = note_id,
                title="test title",
                content="test content",
                user_id = 999
            )

            mock_note_repo.get_note_by_id.return_value = other_user_note

            # Act & Assert
            with pytest.raises(PermissionError):
                note_service.update_note(user_id, note_id, "test title", "test content")
            
            mock_note_repo.get_note_by_id.assert_called_once_with(note_id)
            mock_note_repo.update_note.assert_not_called()

        def test_update_note_value_error(self, note_service, mock_note_repo):
            # Arrange
            user_id = 100
            note_id = 1

            # Act & Assert
            with pytest.raises(ValueError):
                note_service.update_note(user_id, note_id, "", "content")
    
    class TestDeleteNote:
        def test_delete_note_success(self, note_service, mock_note_repo):
            # Arrange
            note_id = 1
            user_id = 100
            exisiting_note = DummyNote(
                id = note_id,
                title = "test title",
                content = "test content",
                user_id = user_id
            )

            mock_note_repo.get_note_by_id.return_value = exisiting_note

            # Act
            result = note_service.delete_note(note_id, user_id)

            # Assert
            assert result is True
            mock_note_repo.get_note_by_id.assert_called_once_with(note_id)
            mock_note_repo.delete_note.assert_called_once_with(note_id, user_id)

        def test_delete_note_permission_error(self, note_service, mock_note_repo):
            # Arrange
            note_id = 1
            user_id = 100

            other_user_note = DummyNote(
                id = note_id,
                title="test title",
                content="test content",
                user_id = 999
            )

            mock_note_repo.get_note_by_id.return_value = other_user_note

            # Act & Assert
            with pytest.raises(PermissionError):
                note_service.delete_note(note_id, user_id)
            
            mock_note_repo.get_note_by_id.assert_called_once_with(note_id)
            mock_note_repo.delete_note.assert_not_called()