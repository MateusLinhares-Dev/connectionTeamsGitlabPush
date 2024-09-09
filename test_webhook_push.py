"""
TDD - Test Driven development (Desenvolvimento dirigido a tests)
"""
from core.webhook_conector import GitlabPushPayload, GitLabPushEvent, Commit, Repository, CommitAuthor
from fastapi import HTTPException
import unittest


class TestWebhookReturnJsonPush(unittest.TestCase):
    def setUp(self):
        self.payload = GitlabPushPayload(
            object_kind="push",
            event_name="push",
            before="0000000000000000000000000000000000000000",
            after="1111111111111111111111111111111111111111",
            ref="refs/heads/main",
            user_name="test_user",
            commits=[Commit(
                id="a1b2c3d4",
                message="create conector, url=https://gitlab.softexpert.network/on-demand-development/odd-conectores/src/csvinput",
                timestamp="2023-08-30T12:34:56Z",
                url="http://example.com",
                author=CommitAuthor(name="John Doe", email="john@example.com"),
                added=["file1.txt"],
                modified=["file2.txt"],
                removed=[]
            )],
            repository=Repository(
                name="TestRepo",
                url="http://gitlab.example.com",
                description="Test repository",
                homepage="http://example.com",
                git_http_url="http://gitlab.example.com/repo.git",
                git_ssh_url="git@gitlab.example.com:repo.git",
                visibility_level=0
            )
        )
    
    def test_process_push_event_valid(self):
        """Testa se process_push_event identifica corretamente o evento push."""
        event = GitLabPushEvent(self.payload)
        result = event.process_push_event()
        self.assertIn("commit_messages", result)
        self.assertIn("url_doc", result)
        
    def test_not_push_error_exception(self):
        """
        Testa para ver se caso houver outro tipo de object_kind, ele irá retornar o erro programado
        """
        payload = self.payload.model_copy(update={"object_kind":"merge_request"})
        event = GitLabPushEvent(payload)
        with self.assertRaises(HTTPException) as context:
            event.process_push_event()
        
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, 'Evento desconhecido')

    def test_not_conector_create_push(self):
        """
        Este teste valida se não foi inserido um novo conector, com objetivo de validar se caso não tiver nenhum conector sendo cadastrado então é mostrado na tela um exception
        """
        payload = self.payload.model_copy(update={
            "commits":[Commit(
                id="a1b2c3d4",
                message="Update README",
                timestamp="2023-08-30T12:34:56Z",
                url="http://example.com",
                author=CommitAuthor(name="John Doe", email="john@example.com"),
                added=["file1.txt"],
                modified=["file2.txt"],
                removed=[]
            )]
        })

        event = GitLabPushEvent(payload)
        with self.assertRaises(HTTPException) as context:
            event.process_push_event()
        
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, 'Nenhum conector encontrado')

    def test_not_url_push_event(self):
        """
        Testa o cenário em que não recebe a URL no commit
        """
        payload = self.payload.model_copy(update={
            "commits":[Commit(
                id="a1b2c3d4",
                message="create conector",
                timestamp="2023-08-30T12:34:56Z",
                url="http://example.com",
                author=CommitAuthor(name="John Doe", email="john@example.com"),
                added=["file1.txt"],
                modified=["file2.txt"],
                removed=[]
            )]
        })

        event = GitLabPushEvent(payload=payload)
        with self.assertRaises(HTTPException) as context:
            event.process_push_event()

            self.assertEqual(context.exception.status_code, 400)
            self.assertEqual(context.exception.detail, "Está faltando a url da documentação")

if __name__ == '__main__':
    unittest.main(verbosity=2)
