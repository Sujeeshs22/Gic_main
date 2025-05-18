import time
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class RateLimitMiddleware(MiddlewareMixin):
    RATE_LIMIT = 5
    WINDOW = 300
    CACHE_PREFIX = "rate_limit"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_ip(request)
        key = f"{self.CACHE_PREFIX}:{ip}"
        current_time = int(time.time())
        request_times = cache.get(key, [])
        request_times = [t for t in request_times if t > current_time - self.WINDOW]

        if len(request_times) >= self.RATE_LIMIT:
            retry_after = self.WINDOW - (current_time - request_times[0])
            return JsonResponse(
                {"error": "Too many requests"},
                status=429,
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(self.RATE_LIMIT),
                    "X-RateLimit-Remaining": "0",
                },
            )
        request_times.append(current_time)
        cache.set(key, request_times, timeout=self.WINDOW)
        response = self.get_response(request)
        response["X-RateLimit-Limit"] = str(self.RATE_LIMIT)
        response["X-RateLimit-Remaining"] = str(self.RATE_LIMIT - len(request_times))
        return response

    def get_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
