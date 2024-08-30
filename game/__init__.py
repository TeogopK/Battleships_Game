"""
Package manager file
"""

__version__ = "0.0.1"

from .application import Application, main
from .server.multiplayer_server import MultiplayerServer

__all__ = ["Application", "main", "MultiplayerServer"]
