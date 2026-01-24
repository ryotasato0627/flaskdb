import pytest
from unittest.mock import MagicMock, patch
from app.services.auth import AuthService
from tests.dummy.dummy_user import DummyUser

class TestAuthService:
    def test_login_success(self):
        username = "testuser"
        email = "test@example.com"
        password = "securepassword"

        dummy_user = DummyUser(
            id = 1,
            username = username,
            email = email,
            password = password
        )

        with patch("app.services.auth.UserRepository") as mock_repo, \
            patch("app.services.auth.check_password_hash") as mock_check, \
            patch("app.services.auth.TokenUtils.generate_token") as mock_token, \
            patch("app.services.auth.logger") as mock_logger:

            mock_repo.return_value.get_user_by_mail.return_value = dummy_user
            mock_check.return_value = True
            mock_token.return_value = "dummy_token"

            result = AuthService.login(email, password)

            assert result == {"access_token": "dummy_token"}
            mock_token.assert_called_once_with(dummy_user.id)
            mock_logger.info.assert_called_once()

    def test_login_user_not_found(self):
        with patch("app.services.auth.UserRepository") as mock_repo:
            mock_repo.return_value.get_user_by_mail.return_value = None

            with pytest.raises(ValueError) as excinfo:
                AuthService.login("test@example.com", "wrongpassword")

            assert str(excinfo.value) == "ユーザーが登録されていません"

    def test_login_invalid_password(self):
        username = "testuser"
        email = "test@example.com"
        password = "securepassword"

        dummy_user = DummyUser(
            id=1,
            username=username,
            email=email,
            password=password
        )

        with patch("app.services.auth.UserRepository") as mock_repo, \
             patch("app.services.auth.check_password_hash") as mock_check:

            mock_repo.return_value.get_user_by_mail.return_value = dummy_user
            mock_check.return_value = False

            with pytest.raises(ValueError) as excinfo:
                AuthService.login(email, "wrongpassword")

            assert str(excinfo.value) == "パスワードが違います"