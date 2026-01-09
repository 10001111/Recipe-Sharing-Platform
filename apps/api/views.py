from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@permission_classes([AllowAny])  # Public endpoint
def api_root(request):
    """
    API Root endpoint.
    Returns basic API information and available endpoints.
    """
    return Response({
        'message': 'Welcome to Recipe Sharing Platform API',
        'version': '1.0.0',
        'endpoints': {
            'recipes': '/api/recipes/',
            'users': '/api/users/',
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])  # Public endpoint for monitoring
def health_check(request):
    """
    Health check endpoint.
    Useful for monitoring and testing database connection.
    """
    from django.db import connection
    
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return Response({
        'status': 'healthy',
        'database': db_status,
    }, status=status.HTTP_200_OK)
