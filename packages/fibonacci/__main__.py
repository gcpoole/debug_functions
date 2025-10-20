"""
Fibonacci Calculator Function

A DigitalOcean Function that calculates Fibonacci numbers.
Publicly accessible via HTTP with query parameter.

Usage:
    GET /fibonacci?n=10
    Returns: {"n": 10, "result": 55, "duration_seconds": 0.001}
"""

import json
import time


def fibonacci(n: int) -> int:
    """Recursive Fibonacci - exponentially CPU intensive."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def main(event, context):
    """
    Main function handler for DO Functions.

    Args:
        event (dict): Contains request data including:
            - http: dict with method, headers, path, queryString, etc.
        context (dict): Function execution context

    Returns:
        dict: Response with statusCode, body, and headers
    """
    # Extract query parameters
    http_data = event.get('http', {})
    query_string = http_data.get('queryString', '')

    # Parse query parameters manually (simple key=value&key=value format)
    params = {}
    if query_string:
        for param in query_string.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                params[key] = value

    # Get 'n' parameter
    n_str = params.get('n')

    if n_str is None:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Missing required parameter "n"',
                'usage': 'GET /fibonacci?n=10',
                'note': 'n should be between 0 and 40 for reasonable performance'
            })
        }

    # Validate and parse n
    try:
        n = int(n_str)
        if n < 0:
            raise ValueError("n must be non-negative")
        if n > 45:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'n too large (max 45)',
                    'reason': 'Values above 45 take too long to compute'
                })
            }
    except ValueError as e:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': f'Invalid parameter "n": {str(e)}',
                'received': n_str
            })
        }

    # Calculate fibonacci with timing
    start_time = time.time()
    result = fibonacci(n)
    duration = time.time() - start_time

    # Return success response
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'n': n,
            'result': result,
            'duration_seconds': round(duration, 4),
            'function': 'fibonacci',
            'note': 'Calculated using recursive algorithm'
        })
    }
