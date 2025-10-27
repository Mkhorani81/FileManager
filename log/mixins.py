from .base_mixins import BaseDownloadLoggingMixin
from .models import DownloadLog


class DownloadLoggingMixin(BaseDownloadLoggingMixin):
    def handle_log(self):
        DownloadLog(**self.log).save()