from unittest import TestCase
from unittest.mock import MagicMock, patch

import pytest

from src.chats.chat import Chat


class TestChat(TestCase):
    chat: Chat
    assistant_id = "assistant_id"

    mock_client: MagicMock

    def setUp(self):
        self.mock_client = MagicMock()
        self.chat = Chat(self.mock_client, self.assistant_id)

    def test_chat_start(self):
        self.mock_client.threads_create.return_value.id = "thread_id"

        with patch.object(self.chat, "run_thread") as mock_run_thread:
            self.chat.start()

        assert self.chat.thread_id == "thread_id"
        mock_run_thread.assert_called_once()

    def test_chat_start_with_thread(self):
        self.chat.thread_id = "thread_id"

        with patch.object(self.chat, "run_thread") as mock_run_thread:
            self.chat.start()

        assert self.chat.thread_id == "thread_id"
        mock_run_thread.assert_called_once()

    def test_send_user_message(self):
        self.mock_client.messages_create.return_value = None
        self.mock_client.messages_list.return_value.data = [{"content": "Hello"}]
        self.chat.thread_id = "thread_id"
        self.chat.run_thread = MagicMock()
        self.chat.last_message = MagicMock(return_value="Hello")

        result = self.chat.send_user_message("Test message")

        assert result == "Hello"
        self.mock_client.messages_create.assert_called_once_with(
            "thread_id",
            "Test message",
            "user",
        )
        self.chat.run_thread.assert_called_once()
        self.chat.last_message.assert_called_once()

    def test_chat_run_thread(self):
        self.mock_client.runs_create.return_value.id = "run_id"
        self.chat.thread_id = "thread_id"

        with patch.object(self.chat, "_wait_for_run_to_complete") as mock_wait_for_run_to_complete:
            self.chat.run_thread()

        mock_wait_for_run_to_complete.assert_called_once_with("run_id")

    def test_wait_for_run_to_complete_success(self):
        self.mock_client.runs_retrieve.return_value.status = "completed"

        with patch("time.sleep", return_value=None):
            # pylint: disable=protected-access
            self.chat._wait_for_run_to_complete("run_id")

        self.mock_client.runs_retrieve.assert_called_with(
            "run_id",
            self.chat.thread_id,
        )

    def test_wait_for_run_to_complete_failure(self):
        self.mock_client.runs_retrieve.return_value.status = "failed"

        with patch("time.sleep", return_value=None):
            with pytest.raises(RuntimeError, match="Run failed with status: failed"):
                # pylint: disable=protected-access
                self.chat._wait_for_run_to_complete("run_id")

        self.mock_client.runs_retrieve.assert_called_with(
            "run_id",
            self.chat.thread_id,
        )

    def test_wait_for_run_to_complete_timeout(self):
        self.mock_client.runs_retrieve.return_value.status = "running"

        with patch("time.sleep", return_value=None):
            with pytest.raises(RuntimeError, match="Run timed out after 1 seconds"):
                # pylint: disable=protected-access
                self.chat._wait_for_run_to_complete("run_id", timeout_in_seconds=1)

        self.mock_client.runs_retrieve.assert_called_with(
            "run_id",
            self.chat.thread_id,
        )

    def test_last_message(self):
        self.mock_client.messages_list.return_value.data = [
            MagicMock(content=[MagicMock(text=MagicMock(value="Hello"))])
        ]
        self.chat.thread_id = "thread_id"

        result = self.chat.last_message()

        assert result == "Hello"
        self.mock_client.messages_list.assert_called_once_with("thread_id")
