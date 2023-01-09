class C_Function:
    def __init__(self, name: str, arg_types: list, return_type: any = None) -> None:
        self.name = name
        self.arg_types = arg_types
        self.return_type = return_type