import ast
import builtins

from .supported_functions import SUPPORTED_FUNCTIONS


class Transformer(ast.NodeTransformer):
    def __init__(self, df_var_name):
        self.df_name = df_var_name
        self.builtins = set(dir(builtins))
        self.impl_functions = set(SUPPORTED_FUNCTIONS.keys())

    def visit_Name(self, node):
        if node.id in self.builtins or node.id in self.impl_functions:
            return node
        new_node = ast.Subscript(
            value=ast.Name(id=self.df_name, ctx=ast.Load()),
            slice=ast.Index(value=ast.Constant(node.id)),
            ctx=node.ctx
        )
        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


class Preprocessor:
    def __init__(self, df_var_name):
        self.df_var_name = df_var_name

    def preprocess(self, code):
        tree = ast.parse(code, mode='eval')
        transformer = Transformer(self.df_var_name)
        tree = transformer.visit(tree)
        return tree


class Executor:
    def __init__(self, df_var_name):
        self.df_var_name = df_var_name

    def execute(self, tree, df):
        code = compile(tree, filename='<ast>', mode='eval')
        return eval(code, {self.df_var_name: df}, SUPPORTED_FUNCTIONS)
