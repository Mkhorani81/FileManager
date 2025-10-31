from datetime import timedelta

from django.test import TestCase
from unittest.mock import patch
from django.utils import timezone
from model_bakery import baker

from file.models import File, Link


class TestFileModel(TestCase):
    """
    This is the test for the file model.
    In this test case, methods which exist in file model should be tested
    in difference situation which they have.
    """

    def test_is_expired_when_expires_at_in_the_past(self):
        file = baker.make(File, expires_at=timezone.now() - timedelta(hours=1), status=File.Status.ACTIVE)
        self.assertTrue(file.is_expired())

    def test_is_expired_when_status_expired(self):
        file = baker.make(File, expires_at=None, status=File.Status.EXPIRED)
        self.assertTrue(file.is_expired())

    def test_is_not_expired_when_expires_at_in_the_future(self):
        file = baker.make(File, expires_at=timezone.now() + timedelta(hours=1), status=File.Status.ACTIVE)
        self.assertFalse(file.is_expired())

    def test_is_not_expired_when_no_expires_at_and_active(self):
        file = baker.make(File, expires_at=None, status=File.Status.ACTIVE)
        self.assertFalse(file.is_expired())

    def test_increment_download_count(self):
        file = baker.make(File, download_count=5)
        file.increment_download_count()
        self.assertEqual(file.download_count, 6)

    @patch('file.models.File.is_expired', return_value=False)
    def test_can_download_when_max_downloads_is_None(self, mock_is_expired):
        file = baker.make(File, max_downloads=None, status=File.Status.ACTIVE)
        self.assertTrue(file.can_download())

    @patch('file.models.File.is_expired', return_value=False)
    def test_can_download_when_download_count_lt_max_downloads(self, mock_is_expired):
        file = baker.make(File, download_count=5, max_downloads=6, status=File.Status.ACTIVE)
        self.assertTrue(file.can_download())

    @patch('file.models.File.is_expired', return_value=False)
    def test_can_not_download_when_status_expired(self, mock_is_expired):
        file = baker.make(File, status=File.Status.EXPIRED, max_downloads=None)
        self.assertFalse(file.can_download())

    @patch('file.models.File.is_expired', return_value=False)
    def test_can_not_download_when_status_deleted(self, mock_is_expired):
        file = baker.make(File, status=File.Status.DELETED, max_downloads=None)
        self.assertFalse(file.can_download())

    @patch('file.models.File.is_expired', return_value=True)
    def test_can_now_download_when_is_expired(self, mock_is_expired):
        file = baker.make(File, status=File.Status.ACTIVE, max_downloads=None)
        self.assertFalse(file.can_download())

    @patch('file.models.File.is_expired', return_value=False)
    def test_can_not_download_when_download_count_gt_max_downloads(self, mock_is_expired):
        file = baker.make(File, status=File.Status.ACTIVE, max_downloads=6, download_count=7)
        self.assertFalse(file.can_download())

    def test_active_to_expired_is_allowed(self):
        file = baker.make(File, status=File.Status.ACTIVE)
        file.change_status(File.Status.EXPIRED)
        file.refresh_from_db()
        self.assertEqual(file.status, File.Status.EXPIRED)

    def test_active_to_deleted_is_allowed(self):
        file = baker.make(File, status=File.Status.ACTIVE)
        file.change_status(File.Status.DELETED)
        file.refresh_from_db()
        self.assertEqual(file.status, File.Status.DELETED)

    def test_expired_to_deleted_is_allowed(self):
        file = baker.make(File, status=File.Status.EXPIRED)
        file.change_status(File.Status.DELETED)
        file.refresh_from_db()
        self.assertEqual(file.status, File.Status.DELETED)

    def test_expired_to_active_is_not_allowed(self):
        file = baker.make(File, status=File.Status.EXPIRED)
        with self.assertRaises(ValueError):
            file.change_status(File.Status.ACTIVE)

    def test_deleted_to_active_is_not_allowed(self):
        file = baker.make(File, status=File.Status.DELETED)
        with self.assertRaises(ValueError):
            file.change_status(File.Status.ACTIVE)

    def test_deleted_to_expired_is_not_allowed(self):
        file = baker.make(File, status=File.Status.DELETED)
        with self.assertRaises(ValueError):
            file.change_status(File.Status.EXPIRED)

    def test_same_status_does_nothing(self):
        file = baker.make(File, status=File.Status.ACTIVE)
        file.change_status(File.Status.ACTIVE)
        file.refresh_from_db()
        self.assertEqual(file.status, File.Status.ACTIVE)
