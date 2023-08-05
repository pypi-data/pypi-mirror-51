"""
``@route()`` use this decorator to define the route, pass path as argument

``response()`` call this function with arguments, the arguments can be JSON type or String.
"""

from .sidanwebframework import Server, response, route, render

name = 'sidanwebframework'

__all__ = [
    'Server', 'response', 'route', 'render'
]