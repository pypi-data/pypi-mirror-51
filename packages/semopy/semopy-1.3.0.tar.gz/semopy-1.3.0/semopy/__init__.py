'''semopy is a Python package that implements numerous SEM-related functonality.'''
from .stats import gather_statistics, calculate_likelihood, calculate_aic,\
                   calculate_bic, calc_aic, calc_bic, calc_likelihood
from .regsem import StructureAnalyzer
from .visualization import visualize
from .optimizer import Optimizer
from .inspector import inspect
from .model_nl import ModelNL
from .model import Model

name = "semopy"
__version__ = "1.3.0"
