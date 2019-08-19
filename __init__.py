import sys
import os

gfToolsAPPS = os.path.abspath(os.path.join(os.path.dirname(__file__), "applications"))

if gfToolsAPPS not in sys.path:
    sys.path.append(gfToolsAPPS)
