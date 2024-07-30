from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from time import perf_counter
from collections import defaultdict
from typing import Callable

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int, window_seconds: int, max_ips: int = 10000):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.max_ips = max_ips
        self.ip_request_counts = defaultdict(list)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host
        current_time = perf_counter()

        # Clean up old timestamps for this IP
        if client_ip in self.ip_request_counts:
            self.ip_request_counts[client_ip] = [
                timestamp for timestamp in self.ip_request_counts[client_ip]
                if current_time - timestamp < self.window_seconds
            ]

        if len(self.ip_request_counts[client_ip]) >= self.max_requests:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please try again later."}
            )

        self.ip_request_counts[client_ip].append(current_time)

        if len(self.ip_request_counts) > self.max_ips:
            # Remove the oldest IP
            oldest_ip = min(self.ip_request_counts, key=lambda ip: min(self.ip_request_counts[ip]))
            del self.ip_request_counts[oldest_ip]

        response = await call_next(request)
        return response
