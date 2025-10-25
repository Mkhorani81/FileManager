from django.template.context_processors import request
from django.utils.timezone import now
import ipaddress
import traceback
import logging
import ast

logger = logging.getLogger(__name__)

class BaseDownloadLoggingMixin:
    should_log = '__all__' # for customizing methods should be logged
    sensitive_fields = {}
    CLEANED_SUBSTITUTE = '**********'

    def __init__(self, *args, **kwargs):
        assert isinstance(self.CLEANED_SUBSTITUTE, str), 'CLEANED_SUBSTITUTE must be a string'
        super().__init__(*args, **kwargs)

    def initial(self, request, *args, **kwargs):
        self.log = {'timestamp': now(),}
        return super().initial(request, *args, **kwargs)

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        self.log['errors'] = traceback.format_exc()
        return response

    def finalize_response(self, request, response, *args, **kwargs):
        pass
