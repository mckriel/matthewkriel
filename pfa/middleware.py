import time
import logging
import json
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('pfa')

class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware to log all requests and responses to the PFA app."""
    
    def process_request(self, request):
        """Set request start time and log incoming request."""
        # Only log requests to the PFA app
        if not request.path.startswith('/pfa'):
            return None
            
        request.start_time = time.time()
        
        # Extract request details
        user = request.user.username if request.user.is_authenticated else 'anonymous'
        method = request.method
        path = request.path
        query = dict(request.GET.items())
        
        # Log request
        logger.info(
            f"REQUEST: {method} {path} from user={user} "
            f"ip={request.META.get('REMOTE_ADDR')} query={json.dumps(query)}"
        )
        return None
        
    def process_response(self, request, response):
        """Log the response and timing."""
        # Only log requests to the PFA app
        if not request.path.startswith('/pfa'):
            return response
            
        # Calculate request duration
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            duration_ms = int(duration * 1000)
            
            # Only log status code and duration for PFA app responses
            logger.info(
                f"RESPONSE: {request.method} {request.path} "
                f"status={response.status_code} time={duration_ms}ms"
            )
            
        return response

class DatabaseQueryLoggingMiddleware(MiddlewareMixin):
    """Middleware to log database queries for PFA app."""
    
    def process_request(self, request):
        """Enable query logging for PFA requests."""
        # Only log queries for the PFA app
        if not request.path.startswith('/pfa'):
            return None
        
        from django.db import connection
        connection.queries_log = []
        connection.force_debug_cursor = True
        
        return None
        
    def process_response(self, request, response):
        """Log database queries."""
        # Only log queries for the PFA app
        if not request.path.startswith('/pfa'):
            return response
            
        from django.db import connection
        
        if hasattr(connection, 'queries_log') and connection.queries_log:
            total_time = 0
            for query in connection.queries_log:
                total_time += float(query.get('time', 0))
                
            # Only log summary of queries for PFA app
            logger.debug(
                f"DB: {request.method} {request.path} - "
                f"{len(connection.queries_log)} queries in {total_time:.2f}ms"
            )
            
            # Log individual queries at trace level
            for i, query in enumerate(connection.queries_log):
                logger.debug(f"DB QUERY #{i+1}: {query.get('sql')} [{query.get('time')}ms]")
                
        # Clean up
        connection.force_debug_cursor = False
            
        return response