import os
import sys


# Append tool path in sys.path
toolPath = os.path.dirname(os.path.abspath(__file__))
if toolPath not in sys.path:
    sys.path.append(toolPath)
