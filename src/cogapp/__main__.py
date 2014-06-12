"""Make Cog runnable directly from the module."""
import sys

from gernet.src.cogapp.cogapp import Cog


sys.exit(Cog().main(sys.argv))
