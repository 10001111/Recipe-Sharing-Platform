"""
Custom Middleware for Security Enhancements

This middleware adds security headers and rate limiting to API requests.
"""

from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings
import time


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security headers to all responses
    
    Includes:
    - Content Security Policy (CSP)
    - X-Content-Type-Options
    - X-Frame-Options
    - X-XSS-Protection
    - Referrer-Policy
    """
    
    def process_response(self, request, response):
        # Content Security Policy
        if hasattr(settings, 'SECURE_CONTENT_SECURITY_POLICY') and settings.SECURE_CONTENT_SECURITY_POLICY:
            csp_parts = []
            for directive, sources in settings.SECURE_CONTENT_SECURITY_POLICY.items():
                sources_str = ' '.join(sources)
                csp_parts.append(f"{directive} {sources_str}")
            response['Content-Security-Policy'] = '; '.join(csp_parts)
        
        # X-Content-Type-Options: Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # X-Frame-Options: Prevent clickjacking
        if hasattr(settings, 'X_FRAME_OPTIONS'):
            response['X-Frame-Options'] = settings.X_FRAME_OPTIONS
        else:
            response['X-Frame-Options'] = 'DENY'
        
        # X-XSS-Protection: Enable browser XSS filter
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer-Policy: Control referrer information
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions-Policy: Control browser features
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response


class RateLimitMiddleware(MiddlewareMixin):
    """
    Rate limiting middleware for API endpoints
    
    Limits requests per IP address to prevent abuse.
    Uses Django cache for storing rate limit data.
    """
    
    def process_request(self, request):
        # Only apply rate limiting to API endpoints
        if not request.path.startswith('/api/'):
            return None
        
        # Skip rate limiting for certain endpoints (health check, etc.)
        skip_paths = ['/api/health/', '/api/schema/', '/api/docs/', '/api/redoc/']
        if any(request.path.startswith(path) for path in skip_paths):
            return None
        
        # Get client IP address
        client_ip = self.get_client_ip(request)
        
        # Rate limit configuration
        # Default: 100 requests per hour per IP
        rate_limit_requests = getattr(settings, 'RATE_LIMIT_REQUESTS', 100)
        rate_limit_window = getattr(settings, 'RATE_LIMIT_WINDOW', 3600)  # 1 hour in seconds
        
        # Check rate limit
        cache_key = f'rate_limit:{client_ip}'
        current_count = cache.get(cache_key, 0)
        
        if current_count >= rate_limit_requests:
            # Rate limit exceeded
            return JsonResponse(
                {
                    'error': 'Rate limit exceeded',
                    'message': f'Too many requests. Limit: {rate_limit_requests} requests per {rate_limit_window // 60} minutes.',
                    'retry_after': rate_limit_window,
                },
                status=429  # Too Many Requests
            )
        
        # Increment counter
        cache.set(cache_key, current_count + 1, rate_limit_window)
        
        # Add rate limit headers to response
        request._rate_limit_remaining = rate_limit_requests - current_count - 1
        request._rate_limit_reset = int(time.time()) + rate_limit_window
        
        return None
    
    def process_response(self, request, response):
        # Add rate limit headers to response
        if hasattr(request, '_rate_limit_remaining'):
            response['X-RateLimit-Remaining'] = str(request._rate_limit_remaining)
            response['X-RateLimit-Reset'] = str(request._rate_limit_reset)
            response['X-RateLimit-Limit'] = str(getattr(settings, 'RATE_LIMIT_REQUESTS', 100))
        
        return response
    
    def get_client_ip(self, request):
        """
        Get client IP address from request
        
        Handles proxies and load balancers correctly.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        return ip

