import os
import logging
from unittest import TestCase
from service import app
from service.models import db, init_db, Account
from service.routes import talisman

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:password@localhost:5432/testdb"
)

class TestAccountService(TestCase):
    """Account Service Routes Test Cases"""

    @classmethod
    def setUpClass(cls):
        """Run once before all test instances"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)
        talisman.force_https = False

    @classmethod
    def tearDownClass(cls):
        """Run once after all test instances"""
        db.session.close()

    def setUp(self):
        """Runs before every individual test method"""
        db.drop_all()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        """Runs after every individual test method"""
        db.session.remove()

    def _create_accounts(self, count):
        """Helper to seed accounts into the database"""
        accounts = []
        for i in range(count):
            account = Account(
                name=f"User {i}",
                email=f"user{i}@example.com",
                address=f"{i} Main St",
                phone=f"555-000{i}"
            )
            account.create()
            accounts.append(account)
        return accounts

    def test_index(self):
        """It should get the root index page successfully"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_health(self):
        """It should return health status OK"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "OK")

    def test_create_account(self):
        """It should Create a new Account"""
        data = {"name": "Alice", "email": "alice@gmail.com", "address": "123 Lane", "phone": "555-1234"}
        response = self.client.post("/accounts", json=data, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["name"], "Alice")

    def test_get_account(self):
        """It should Read a single Account by ID"""
        account = self._create_accounts(1)[0]
        response = self.client.get(f"/accounts/{account.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], account.name)

    def test_get_account_not_found(self):
        """It should return 404 for missing account IDs"""
        response = self.client.get("/accounts/99999")
        self.assertEqual(response.status_code, 404)

    def test_list_accounts(self):
        """It should List all available Accounts"""
        self._create_accounts(3)
        response = self.client.get("/accounts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 3)

    def test_update_account(self):
        """It should Update an existing Account payload"""
        account = self._create_accounts(1)[0]
        updated_data = {"name": "Alice Updated", "email": "alice@gmail.com", "address": "456 Blvd", "phone": "555-1234"}
        response = self.client.put(f"/accounts/{account.id}", json=updated_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Alice Updated")

    def test_update_account_not_found(self):
        """It should return 404 when updating non-existent accounts"""
        response = self.client.put("/accounts/99999", json={"name": "No One"}, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_delete_account(self):
        """It should Delete an Account from storage"""
        account = self._create_accounts(1)[0]
        response = self.client.delete(f"/accounts/{account.id}")
        self.assertEqual(response.status_code, 204)
        # Verify deletion returns 404
        response = self.client.get(f"/accounts/{account.id}")
        self.assertEqual(response.status_code, 404)
