import pytest
from unittest.mock import MagicMock, ANY
from app.services.user import UserService
from tests.dummy.dummy_user import DummyUser

class TestUserService:
    @pytest.fixture
    def mock_user_repo(self):
        return MagicMock()

    @pytest.fixture
    def user_service(self, mock_user_repo):
        return UserService(user_repo=mock_user_repo)
    
    @pytest.fixture
    def sample_user(self):
        return DummyUser()
    
    class TestRegister:
        def test_register_success(self, user_service, mock_user_repo):
            # Arrange
            username = "testuser"
            email = "test@example.com"
            password = "securepassword"
            created_user = DummyUser(
                id = 1,
                username = username,
                email = email,
                password = password
            )

            mock_user_repo.get_user_by_mail.return_value = None
            mock_user_repo.register.return_value = created_user

            # Act
            result = user_service.register(username, email, password)

            # Assert
            assert result == created_user
            mock_user_repo.register.assert_called_once_with(username=username, email=email, password=ANY)

            def test_register_existing_email(self, user_service, mock_user_repo, sample_user):
                # Arrange
                username = "testuser"
                email = "test@example.com"
                password = "securepassword"
                mock_user_repo.get_user_by_mail.return_value = DummyUser(
                    id = 1,
                    username = "existinguser",
                    email = email,
                    password = "hashedpassword"
                )

                # Act & Assert
                with pytest.raises(ValueError):
                    user_service.register(username, email, password)

                mock_user_repo.register.assert_not_called()