from .generator import Generator, PortType, PortDirection, BlockEdgeType, \
    always, CombinationalCodeBlock, SequentialCodeBlock

from .passes import Attribute, verilog
from .util import clog2, reduce_add, reduce_and, reduce_mul, reduce_or,\
    concat, zext, mux, ternary, signed, const, comment

from .ports import PortBundle

# directly import from the underlying C++ binding
from _kratos.util import is_valid_verilog
from _kratos.exception import VarException, StmtException
from _kratos.passes import IRVisitor as IRVisitor
from _kratos import PackedStruct, Port, Var, AssignmentType
from .stmts import IfStmt, SwitchStmt, if_, switch_

# FSMs
from _kratos import FSM, FSMState

posedge = BlockEdgeType.Posedge
negedge = BlockEdgeType.Negedge

__all__ = ["Generator", "PortType", "PortDirection", "BlockEdgeType", "always",
           "verilog", "signed", "const", "is_valid_verilog", "VarException",
           "StmtException", "IRVisitor", "FSM", "FSMState"]

__all__ += ["CombinationalCodeBlock", "SequentialCodeBlock", "SwitchStmt",
            "PackedStruct", "Port", "Var", "IfStmt", "AssignmentType",
            "if_", "switch_", "Attribute", "PortBundle"]

# utils
__all__ += ["clog2", "reduce_add", "reduce_and", "reduce_mul", "reduce_or",
            "concat", "zext", "comment"]

# type aliasing
__all__ += ["BlockEdgeType", "posedge", "negedge", "mux", "ternary"]
