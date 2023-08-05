"""
Either pull in QCEl models or local models
"""

from . import rest_models
from .rest_models import rest_model, ComputeResponse
from .common_models import KeywordSet, Molecule, ObjectId, OptimizationSpecification, ProtoModel, QCSpecification
from .gridoptimization import GridOptimizationInput, GridOptimizationRecord
from .model_builder import build_procedure
from .model_utils import hash_dictionary, json_encoders, prepare_basis
from .records import OptimizationRecord, ResultRecord
from .task_models import PythonComputeSpec, TaskRecord, TaskStatusEnum, ManagerStatusEnum
from .torsiondrive import TorsionDriveInput, TorsionDriveRecord

from ..util import auto_gen_docs_on_demand


for model in (ComputeResponse, KeywordSet, Molecule, OptimizationRecord, QCSpecification,
              GridOptimizationInput, GridOptimizationRecord, ResultRecord,
              PythonComputeSpec, TaskRecord,
              TorsionDriveInput, TorsionDriveRecord):
    auto_gen_docs_on_demand(model)
