"""
Test cases for Account Service

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
"""
import os
import logging
from unittest import TestCase
from service import app
from service.models import db, Account, init_db
from service.common import status
from tests.factories import AccountFactory

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///test.db")


class TestAccountService(TestCase):
    """Account Service Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        pass

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        with app.app_context():
            db.session.query(Account).delete()
            db.session.commit()

    def tearDown(self):
        """Runs after each test"""
        with app.app_context():
            db.session.remove()

    def _create_accounts(self, count):
        """Factory method to create accounts in bulk"""
        accounts = []
        with app.app_context():
            for _ in range(count):
                account = AccountFactory()
                db.session.add(account)
                db.session.commit()
                # Refresh to get the ID and avoid detached session
                db.session.refresh(account)
                accounts.append(account)
        return accounts

    def test_index(self):
        """It should return the index page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "Customer Account REST API Service")

    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "OK")

    def test_create_account(self):
        """It should Create a new Account"""
        account = AccountFactory()
        response = self.client.post(
            "/accounts",
            json=account.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        new_account = response.get_json()
        self.assertEqual(new_account["name"], account.name)
        self.assertEqual(new_account["email"], account.email)

    def test_create_account_bad_content_type(self):
        """It should not Create an Account with the wrong content type"""
        account = AccountFactory()
        response = self.client.post(
            "/accounts",
            json=account.serialize(),
            content_type="text/plain",
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_list_accounts(self):
        """It should List all Accounts"""
        self._create_accounts(5)
        response = self.client.get("/accounts")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_read_account(self):
        """It should Read an Account"""
        self._create_accounts(1)
        with app.app_context():
            account = Account.query.first()
            response = self.client.get(f"/accounts/{account.id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], account.name)

    def test_read_account_not_found(self):
        """It should not Read an Account that is not found"""
        response = self.client.get("/accounts/0")
        self.assertEqual(response.status_code, 404)

    def test_update_account(self):
        """It should Update an existing Account"""
        self._create_accounts(1)
        with app.app_context():
            account = Account.query.first()
            account_id = account.id
            response = self.client.put(
                f"/accounts/{account_id}",
                json={
                    "name": "Updated Name",
                    "email": account.email,
                    "address": account.address,
                    "phone_number": account.phone_number,
                },
                content_type="application/json",
            )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "Updated Name")

    def test_update_account_not_found(self):
        """It should not Update an Account that is not found"""
        response = self.client.put(
            "/accounts/0", json={}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_account(self):
        """It should Delete an Account"""
        self._create_accounts(1)
        with app.app_context():
            account = Account.query.first()
            account_id = account.id
            response = self.client.delete(f"/accounts/{account_id}")
        self.assertEqual(response.status_code, 204)

    def test_security_headers(self):
        """It should return security headers"""
        response = self.client.get("/", environ_overrides={"HTTPS": "on"})
        self.assertEqual(response.status_code, 200)
        headers = {
            "X-Frame-Options": "SAMEORIGIN",
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "default-src 'self'; object-src 'none'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }
        for key, value in headers.items():
            self.assertEqual(response.headers.get(key), value)

    def test_cors_policies(self):
        """It should return CORS header"""
        response = self.client.get("/", environ_overrides={"HTTPS": "on"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "*")
