from django.utils.timezone import now
import ipaddress
import traceback
import logging

from file.models import File

logger = logging.getLogger(__name__)


class BaseLoggingMixin:
    """
    This is Base Logging Mixin in which put fields that are used in any logs


    For developing app, create new mixins by inheriting from BaseLoggingMixin and -
    override 'get_extra_log_data' methods for additional fields.

    Base Fields:
        - user
        - ip_address
        - user_name
        - success
        - status code
        - time
        - errors
    """
    logging_methods = '__all__'  # for customizing methods should be logged
    sensitive_fields = {}
    CLEANED_SUBSTITUTE = '**********'

    def __init__(self, *args, **kwargs):
        assert isinstance(self.CLEANED_SUBSTITUTE, str), 'CLEANED_SUBSTITUTE must be a string'
        super().__init__(*args, **kwargs)

    def initial(self, request, *args, **kwargs):
        """
        Filling out time by requesting user
        """
        self.log = {'timestamp': now(), }
        return super().initial(request, *args, **kwargs)

    def handle_exception(self, exc):
        """
        Saving errors in log
        """
        response = super().handle_exception(exc)
        self.log['errors'] = traceback.format_exc()
        return response

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Get base fields and save them in log model
        """

        response = super().finalize_response(request, response, *args, **kwargs)

        if self.should_log(request):
            user = self._get_user(request)

            base_log_data = {
                'user': user,
                'ip_address': self._get_ip_address(request),
                'username_persistent': user.phone_number if user else None,
                'success': 200 <= response.status_code < 300,
                'status_code': response.status_code,
            }

            base_log_data.update(self.get_extra_log_data(request, response))

            self.log.update(base_log_data)

            try:
                self.handle_log()
            except Exception:
                logger.exception('Logging API call raise exception!')

        return response

    def handle_log(self):
        """
        Override handle_log depends on your requirements
        """
        raise NotImplementedError

    def _get_ip_address(self, request):
        # Check and get user's IP, if user uses load balancer or proxy
        ipaddr = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if ipaddr:
            ipaddr = ipaddr.split(',')[0]
        else:
            ipaddr = request.META.get('REMOTE_ADDR', '').split(',')[0]

        possibles = (
            ipaddr.lstrip('[').split(']')[0], ipaddr.split(':')[0]
        )

        for addr in possibles:
            try:
                return str(ipaddress.ip_address(addr))
            except:
                pass
        return ipaddr

    def _get_user(self, request):
        user = request.user
        if user.is_anonymous:
            return None
        return user

    def should_log(self, request):
        """
        Checking that logs should be executed on which methods.
        """
        return (
                self.logging_methods == '__all__' or request.method in self.logging_methods
        )

    def get_extra_log_data(self, request, response):
        """
        Override this method for custom mixins inheriting from BaseLoggingMixin
        """
        return {}


class BaseDownloadLoggingMixin(BaseLoggingMixin):

    def get_extra_log_data(self, request, response):
        return {
            'file': self._get_file(),
            'short_code': self._get_short_code(),
        }

    def _get_short_code(self):
        return self.kwargs.get('short_code')

    def _get_file(self):
        short_code = self._get_short_code()

        from file.models import Link

        if short_code:
            try:
                link = Link.objects.select_related('file').get(short_code=short_code)
                return link.file
            except Link.DoesNotExist:
                return None
        return None