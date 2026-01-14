import pytest
from unittest.mock import Mock, MagicMock
from src.services.note import NoteService
from src.models.note import Note
from src.repository.note import NoteRepository


class TestNoteService:
    """NoteServiceのテストクラス"""
    
    @pytest.fixture
    def mock_note_repo(self):
        """モックのNoteRepositoryを作成"""
        return Mock(spec=NoteRepository)
    
    @pytest.fixture
    def note_service(self, mock_note_repo):
        """テスト対象のNoteServiceインスタンスを作成"""
        return NoteService(mock_note_repo)
    
    @pytest.fixture
    def sample_note(self):
        """テスト用のNoteオブジェクトを作成"""
        note = Mock(spec=Note)
        note.id = 1
        note.user_id = 100
        note.title = "テストタイトル"
        note.content = "テストコンテンツ"
        return note
    

    class TestGetAllNotes:
        """get_all_notesメソッドのテスト"""
        
        def test_get_all_notes_success(self, note_service, mock_note_repo):
            """全てのノートを正常に取得できること"""
            # Arrange
            expected_notes = [Mock(spec=Note), Mock(spec=Note)]
            mock_note_repo.get_all_notes.return_value = expected_notes
            
            # Act
            result = note_service.get_all_notes()
            
            # Assert
            assert result == expected_notes
            mock_note_repo.get_all_notes.assert_called_once()
        
        def test_get_all_notes_empty(self, note_service, mock_note_repo):
            """ノートが0件の場合"""
            # Arrange
            mock_note_repo.get_all_notes.return_value = []
            
            # Act
            result = note_service.get_all_notes()
            
            # Assert
            assert result == []
            mock_note_repo.get_all_notes.assert_called_once()
    

    class TestGetNoteById:
        """get_note_by_idメソッドのテスト"""
        
        def test_get_note_by_id_success(self, note_service, mock_note_repo, sample_note):
            """IDでノートを正常に取得できること"""
            # Arrange
            note_id = 1
            mock_note_repo.get_note_by_id.return_value = sample_note
            
            # Act
            result = note_service.get_note_by_id(note_id)
            
            # Assert
            assert result == sample_note
            mock_note_repo.get_note_by_id.assert_called_once_with(note_id)
        
        def test_get_note_by_id_not_found(self, note_service, mock_note_repo):
            """存在しないIDの場合"""
            # Arrange
            note_id = 999
            mock_note_repo.get_note_by_id.return_value = None
            
            # Act
            result = note_service.get_note_by_id(note_id)
            
            # Assert
            assert result is None
            mock_note_repo.get_note_by_id.assert_called_once_with(note_id)
    

    class TestCreateNote:
        """create_noteメソッドのテスト"""
        
        def test_create_note_success(self, note_service, mock_note_repo, sample_note):
            """ノートを正常に作成できること"""
            # Arrange
            user_id = 100
            title = "新しいノート"
            content = "ノートの内容"
            mock_note_repo.create_note.return_value = sample_note
            
            # Act
            result = note_service.create_note(user_id, title, content)
            
            # Assert
            assert result == sample_note
            mock_note_repo.create_note.assert_called_once_with(title, content, user_id)
        
        def test_create_note_without_title(self, note_service):
            """タイトルがない場合にエラーが発生すること"""
            # Arrange
            user_id = 100
            title = ""
            content = "ノートの内容"
            
            # Act & Assert
            with pytest.raises(ValueError, match="titleとcontentは必須です"):
                note_service.create_note(user_id, title, content)
        
        def test_create_note_without_content(self, note_service):
            """コンテンツがない場合にエラーが発生すること"""
            # Arrange
            user_id = 100
            title = "タイトル"
            content = ""
            
            # Act & Assert
            with pytest.raises(ValueError, match="titleとcontentは必須です"):
                note_service.create_note(user_id, title, content)
        
        def test_create_note_with_none_values(self, note_service):
            """Noneが渡された場合にエラーが発生すること"""
            # Arrange
            user_id = 100
            
            # Act & Assert
            with pytest.raises(ValueError, match="titleとcontentは必須です"):
                note_service.create_note(user_id, None, None)
    

    class TestUpdateNote:
        """update_noteメソッドのテスト"""
        
        def test_update_note_success(self, note_service, mock_note_repo, sample_note):
            """ノートを正常に更新できること"""
            # Arrange
            user_id = 100
            note_id = 1
            title = "更新後のタイトル"
            content = "更新後のコンテンツ"
            
            mock_note_repo.get_note_by_id.return_value = sample_note
            mock_note_repo.update_note.return_value = sample_note
            
            # Act
            result = note_service.update_note(user_id, note_id, title, content)
            
            # Assert
            assert result == sample_note
            mock_note_repo.get_note_by_id.assert_called_once_with(note_id)
            mock_note_repo.update_note.assert_called_once_with(note_id, title, content)
        
        def test_update_note_without_permission(self, note_service, mock_note_repo, sample_note):
            """権限がない場合にエラーが発生すること"""
            # Arrange
            user_id = 999  # 異なるユーザーID
            note_id = 1
            title = "更新後のタイトル"
            content = "更新後のコンテンツ"
            
            sample_note.user_id = 100  # ノートの所有者は別のユーザー
            mock_note_repo.get_note_by_id.return_value = sample_note
            
            # Act & Assert
            with pytest.raises(PermissionError, match="権限がありません"):
                note_service.update_note(user_id, note_id, title, content)
        
        def test_update_note_without_title(self, note_service):
            """タイトルがない場合にエラーが発生すること"""
            # Arrange
            user_id = 100
            note_id = 1
            
            # Act & Assert
            with pytest.raises(ValueError, match="titleとcontentは必須です"):
                note_service.update_note(user_id, note_id, "", "content")
        
        def test_update_note_without_content(self, note_service):
            """コンテンツがない場合にエラーが発生すること"""
            # Arrange
            user_id = 100
            note_id = 1
            
            # Act & Assert
            with pytest.raises(ValueError, match="titleとcontentは必須です"):
                note_service.update_note(user_id, note_id, "title", "")
    

    class TestDeleteNote:
        """delete_noteメソッドのテスト"""
        
        def test_delete_note_success(self, note_service, mock_note_repo, sample_note):
            """ノートを正常に削除できること"""
            # Arrange
            note_id = 1
            user_id = 100
            
            mock_note_repo.get_note_by_id.return_value = sample_note
            mock_note_repo.delete_note.return_value = True
            
            # Act
            result = note_service.delete_note(note_id, user_id)
            
            # Assert
            assert result is True
            mock_note_repo.get_note_by_id.assert_called_once_with(note_id)
            mock_note_repo.delete_note.assert_called_once_with(note_id, user_id)
        
        def test_delete_note_without_permission(self, note_service, mock_note_repo, sample_note):
            """権限がない場合にエラーが発生すること"""
            # Arrange
            note_id = 1
            user_id = 999  # 異なるユーザーID
            
            sample_note.user_id = 100  # ノートの所有者は別のユーザー
            mock_note_repo.get_note_by_id.return_value = sample_note
            
            # Act & Assert
            with pytest.raises(PermissionError, match="権限がありません"):
                note_service.delete_note(note_id, user_id)
            
            # リポジトリのdelete_noteは呼ばれないことを確認
            mock_note_repo.delete_note.assert_not_called()
    

    class TestCheckPermission:
        """check_permissionメソッドのテスト"""
        
        def test_check_permission_success(self, sample_note):
            """権限がある場合は正常に終了すること"""
            # Arrange
            user_id = 100
            sample_note.user_id = 100
            
            # Act & Assert (例外が発生しないことを確認)
            NoteService.check_permission(sample_note, user_id)
        
        def test_check_permission_failure(self, sample_note):
            """権限がない場合にエラーが発生すること"""
            # Arrange
            user_id = 999
            sample_note.user_id = 100
            
            # Act & Assert
            with pytest.raises(PermissionError, match="権限がありません"):
                NoteService.check_permission(sample_note, user_id)