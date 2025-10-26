from django.utils.timezone import now
import ipaddress
import traceback
import logging

logger = logging.getLogger(__name__)


class BaseDownloadLoggingMixin:
    logging_methods = '__all__'  # for customizing methods should be logged
    sensitive_fields = {}
    CLEANED_SUBSTITUTE = '**********'

    def __init__(self, *args, **kwargs):
        assert isinstance(self.CLEANED_SUBSTITUTE, str), 'CLEANED_SUBSTITUTE must be a string'
        super().__init__(*args, **kwargs)

    def initial(self, request, *args, **kwargs):
        self.log = {'timestamp': now(), }
        return super().initial(request, *args, **kwargs)

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        self.log['errors'] = traceback.format_exc()
        return response

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        if self.should_log(request):
            user = self._get_user(request)

            self.log.update({
                'file': self._get_file(),
                'user': self._get_user(),
                'ip_address': self._get_ip_address(),
                'username_persistent': user.username if user else None,
                'short_code': self._get_short_code(),
                'success': 200 <= response.status_code < 300,
                'status_code': response.status_code,
            })

    def handle_log(self):
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

    def should_log(self, request):
        return (
                self.logging_methods == '__all__' or request.method in self.logging_methods
        )


class BaseChangeLoggingMixin:
    logging_methods = '__all__'  # for customizing methods should be logged
    sensitive_fields = {}
    CLEANED_SUBSTITUTE = '**********'

    def __init__(self, *args, **kwargs):
        assert isinstance(self.CLEANED_SUBSTITUTE, str), 'CLEANED_SUBSTITUTE must be a string'
        super().__init__(*args, **kwargs)
