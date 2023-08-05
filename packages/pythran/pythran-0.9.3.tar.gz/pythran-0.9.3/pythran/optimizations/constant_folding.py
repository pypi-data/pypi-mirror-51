""" ConstantFolding performs some kind of partial evaluation.  """
from __future__ import print_function

from pythran.analyses import ConstantExpressions, ASTMatcher
from pythran.passmanager import Transformation
from pythran.tables import MODULES
from pythran.conversion import to_ast, ConversionError, ToNotEval, mangle
from pythran.analyses.ast_matcher import DamnTooLongPattern
from pythran.syntax import PythranSyntaxError

import gast as ast
from copy import deepcopy


class ConstantFolding(Transformation):

    """
    Replace constant expression by their evaluation.

    >>> import gast as ast
    >>> from pythran import passmanager, backend
    >>> node = ast.parse("def foo(): return 1+3")
    >>> pm = passmanager.PassManager("test")
    >>> _, node = pm.apply(ConstantFolding, node)
    >>> print(pm.dump(backend.Python, node))
    def foo():
        return 4
    """

    def __init__(self):
        Transformation.__init__(self, ConstantExpressions)

    def prepare(self, node):
        assert isinstance(node, ast.Module)
        self.env = {
            '__builtin__': __import__('__builtin__'),
        }

        for module_name in MODULES:
            # __dispatch__ is the only fake top-level module
            if module_name != '__dispatch__':
                import_name = module_name

                alias_module_name = mangle(module_name)
                self.env[alias_module_name] = __import__(import_name)

                # handle functions conflicting with c++ keywords
                for fun in MODULES[module_name]:
                    if fun in ("__theitemgetter__", "pythran"):
                        # these ones do not exist in Python
                        continue

        # we need to parse the whole code to be able to apply user-defined pure
        # function but import are resolved before so we remove them to avoid
        # ImportError (for operator_ for example)
        dummy_module = ast.Module([s for s in node.body
                                   if not isinstance(s, ast.Import)])
        eval(compile(ast.gast_to_ast(dummy_module),
                     '<constant_folding>', 'exec'),
             self.env)

        super(ConstantFolding, self).prepare(node)

    def skip(self, node):
        return node

    visit_Num = visit_Name = skip

    visit_List = visit_Set = Transformation.generic_visit
    visit_Dict = visit_Tuple = Transformation.generic_visit

    def visit_Index(self, node):
        value = self.visit(node.value)
        if value is not node.value:
            return ast.Index(value)
        else:
            return node

    def generic_visit(self, node):
        if isinstance(node, ast.expr) and node in self.constant_expressions:
            fake_node = ast.Expression(node)
            code = compile(ast.gast_to_ast(fake_node),
                           '<constant folding>', 'eval')
            try:
                value = eval(code, self.env)
                new_node = to_ast(value)
                try:
                    if not ASTMatcher(node).search(new_node):
                        self.update = True
                        return new_node
                except DamnTooLongPattern as e:
                    print("W: ", e, " Assume no update happened.")
                return Transformation.generic_visit(self, node)
            except ConversionError as e:
                print('error in constant folding: ', e)
                raise
            except ToNotEval:
                return Transformation.generic_visit(self, node)
            except AttributeError as e:
                # FIXME union_ function is not handle by constant folding
                if "union" in e.args[0]:
                    return Transformation.generic_visit(self, node)
                elif "pythran" in e.args[0]:
                    # FIXME: Can be fix giving a Python implementation for
                    # these functions.
                    return Transformation.generic_visit(self, node)
                raise
            except NameError as e:
                # FIXME dispatched function are not processed by constant
                # folding
                if "__dispatch__" in e.args[0]:
                    return Transformation.generic_visit(self, node)
                raise
            except Exception as e:
                raise PythranSyntaxError(str(e), node)
        else:
            return Transformation.generic_visit(self, node)


class PartialConstantFolding(Transformation):

    """
    Replace partially constant expression by their evaluation.

    >>> import gast as ast
    >>> from pythran import passmanager, backend

    >>> node = ast.parse("def foo(n): return [n] * 2")
    >>> pm = passmanager.PassManager("test")
    >>> _, node = pm.apply(PartialConstantFolding, node)
    >>> print(pm.dump(backend.Python, node))
    def foo(n):
        return [n, n]

    >>> node = ast.parse("def foo(n): return 2 * (n,)")
    >>> _, node = pm.apply(PartialConstantFolding, node)
    >>> print(pm.dump(backend.Python, node))
    def foo(n):
        return (n, n)

    >>> node = ast.parse("def foo(n): return [n] + [n]")
    >>> _, node = pm.apply(PartialConstantFolding, node)
    >>> print(pm.dump(backend.Python, node))
    def foo(n):
        return [n, n]

    >>> node = ast.parse("def foo(n, m): return (n,) + (m, n)")
    >>> _, node = pm.apply(PartialConstantFolding, node)
    >>> print(pm.dump(backend.Python, node))
    def foo(n, m):
        return (n, m, n)
    """

    def __init__(self):
        Transformation.__init__(self, ConstantExpressions)

    def fold_mult_left(self, node):
        if not isinstance(node.left, (ast.List, ast.Tuple)):
            return False
        if not isinstance(node.right, ast.Num):
            return False
        return isinstance(node.op, ast.Mult)

    def fold_mult_right(self, node):
        if not isinstance(node.right, (ast.List, ast.Tuple)):
            return False
        if not isinstance(node.left, ast.Num):
            return False
        return isinstance(node.op, ast.Mult)

    def fold_add(self, node, ty):
        if not isinstance(node.left, ty):
            return False
        if not isinstance(node.right, ty):
            return False
        return isinstance(node.op, ast.Add)

    def visit_BinOp(self, node):
        if node in self.constant_expressions:
            return node

        node = self.generic_visit(node)
        if self.fold_mult_left(node):
            self.update = True
            node.left.elts = [deepcopy(elt)
                              for _ in range(node.right.n)
                              for elt in node.left.elts]
            return node.left

        if self.fold_mult_right(node):
            self.update = True
            node.left, node.right = node.right, node.left
            return self.visit(node)

        for ty in (ast.List, ast.Tuple):
            if self.fold_add(node, ty):
                self.update = True
                node.left.elts += node.right.elts
                return node.left

        return node

    def visit_Subscript(self, node):
        """
        >>> import gast as ast
        >>> from pythran import passmanager, backend
        >>> pm = passmanager.PassManager("test")

        >>> node = ast.parse("def foo(a): a[1:][3]")
        >>> _, node = pm.apply(PartialConstantFolding, node)
        >>> _, node = pm.apply(ConstantFolding, node)
        >>> print(pm.dump(backend.Python, node))
        def foo(a):
            a[4]

        >>> node = ast.parse("def foo(a): a[::2][3]")
        >>> _, node = pm.apply(PartialConstantFolding, node)
        >>> _, node = pm.apply(ConstantFolding, node)
        >>> print(pm.dump(backend.Python, node))
        def foo(a):
            a[6]

        >>> node = ast.parse("def foo(a): a[-4:][5]")
        >>> _, node = pm.apply(PartialConstantFolding, node)
        >>> _, node = pm.apply(ConstantFolding, node)
        >>> print(pm.dump(backend.Python, node))
        def foo(a):
            a[1]
        """
        self.generic_visit(node)
        if not isinstance(node.value, ast.Subscript):
            return node
        if not isinstance(node.value.slice, ast.Slice):
            return node
        if not isinstance(node.slice, ast.Index):
            return node

        if not isinstance(node.slice.value, ast.Num):
            return node

        slice_ = node.value.slice
        index = node.slice
        node = node.value

        node.slice = index
        lower = slice_.lower or ast.Num(0)
        step = slice_.step or ast.Num(1)
        node.slice.value = ast.BinOp(lower,
                                     ast.Add(),
                                     ast.BinOp(index.value,
                                               ast.Mult(),
                                               step))
        self.update = True
        return node
