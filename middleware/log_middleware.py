import logging
from django.utils.timezone import now

logger = logging.getLogger(__name__)

class RequestResponseLoggingMiddleware:
    """
    Middleware для логирования входящих запросов и исходящих ответов.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.log_request(request)

        response = self.get_response(request)

        self.log_response(request, response)

        return response

    def log_request(self, request):
        """Логируем параметры запроса."""
        logger.info(f"Request at {now()}: {request.method} {request.get_full_path()}")
        logger.info(f"Headers: {request.headers}")
        if request.method == "POST" or request.method == "PUT":
            logger.info(f"Body: {request.body.decode('utf-8', 'ignore')}")
        logger.info(f"GET Params: {request.GET}")
        logger.info(f"POST Params: {request.POST}")

    def log_response(self, request, response):
        """Логируем параметры ответа."""
        logger.info(f"Response at {now()}: {response.status_code}")
        logger.info(f"Response Body: {response.content[:100]}...")  

