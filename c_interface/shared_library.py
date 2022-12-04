import ctypes
from c_interface.c_function import C_Function


class SharedLibrary:

    def __init__(self, path: str, functions: 'list[C_Function]'):
        self.lib = ctypes.cdll.LoadLibrary(path)

        self._map_functions(functions)

    def _map_functions(self, functions: 'list[C_Function]'):
        for func in functions:
            lib_attr = self.lib.__getattr__(func.name)
            lib_attr.argtypes = func.arg_types
            lib_attr.restype = func.return_type

    def _update_arg_types(self, func_name: str, arg_types: list):
        getattr(self.lib, func_name).argtypes = arg_types

    def _update_return_type(self, func_name: str, return_type: any):
        getattr(self.lib, func_name).restype = return_type

    def _run(self, func_name: str, *args):
        return getattr(self.lib, func_name)(*args)
