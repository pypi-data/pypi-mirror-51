""" NormalizeCompare turns complex compare into function calls. """

from pythran.analyses import ImportedIds
from pythran.passmanager import Transformation
from pythran.utils import path_to_attr

import gast as ast


def is_trivially_copied(node):
    try:
        ast.literal_eval(node)
        return True
    except ValueError:
        pass
    if isinstance(node, (ast.Name, ast.Attribute)):
        return True
    return False


class NormalizeCompare(Transformation):
    '''
    Turns multiple compare into a function with proper temporaries.

    >>> import gast as ast
    >>> from pythran import passmanager, backend
    >>> node = ast.parse("def foo(a): return 0 < a + 1 < 3")
    >>> pm = passmanager.PassManager("test")
    >>> _, node = pm.apply(NormalizeCompare, node)
    >>> print(pm.dump(backend.Python, node))
    def foo(a):
        return foo_compare0(a)
    def foo_compare0(a):
        $1 = (a + 1)
        if (0 < $1):
            pass
        else:
            return __builtin__.False
        if ($1 < 3):
            pass
        else:
            return __builtin__.False
        return __builtin__.True
    '''

    def visit_Module(self, node):
        self.compare_functions = list()
        self.generic_visit(node)
        node.body.extend(self.compare_functions)
        self.update |= bool(self.compare_functions)
        return node

    def visit_FunctionDef(self, node):
        self.prefix = node.name
        self.generic_visit(node)
        return node

    def visit_Compare(self, node):
        node = self.generic_visit(node)
        if len(node.ops) > 1:
            # in case we have more than one compare operator
            # we generate an auxiliary function
            # that lazily evaluates the needed parameters
            imported_ids = self.gather(ImportedIds, node)
            imported_ids = sorted(imported_ids)
            binded_args = [ast.Name(i, ast.Load(), None) for i in imported_ids]

            # name of the new function
            forged_name = "{0}_compare{1}".format(self.prefix,
                                                  len(self.compare_functions))

            # call site
            call = ast.Call(
                ast.Name(forged_name, ast.Load(), None),
                binded_args,
                [])

            # new function
            arg_names = [ast.Name(i, ast.Param(), None) for i in imported_ids]
            args = ast.arguments(arg_names, None, [], [], None, [])

            body = []  # iteratively fill the body (yeah, feel your body!)

            if is_trivially_copied(node.left):
                prev_holder = node.left
            else:
                body.append(ast.Assign([ast.Name('$0', ast.Store(), None)],
                                       node.left))
                prev_holder = ast.Name('$0', ast.Load(), None)

            for i, exp in enumerate(node.comparators):
                if is_trivially_copied(exp):
                    holder = exp
                else:
                    body.append(ast.Assign([ast.Name('${}'.format(i+1),
                                                     ast.Store(), None)],
                                           exp))
                    holder = ast.Name('${}'.format(i+1), ast.Load(), None)
                cond = ast.Compare(prev_holder,
                                   [node.ops[i]],
                                   [holder])
                body.append(ast.If(cond,
                                   [ast.Pass()],
                                   [ast.Return(path_to_attr(('__builtin__', 'False')))]))
                prev_holder = holder

            body.append(ast.Return(path_to_attr(('__builtin__', 'True'))))

            forged_fdef = ast.FunctionDef(forged_name, args, body, [], None)
            self.compare_functions.append(forged_fdef)

            return call
        else:
            return node
