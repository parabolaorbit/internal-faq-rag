class CustomToolExecutor:
    def __init__(self, tool_registry):
        self.tool_registry = tool_registry
    
    def execute_tool(self, tool_name: str, *args, **kwargs):
        if tool_name in self.tool_registry:
            tool_function = self.tool_registry[tool_name]
            return tool_function(*args, **kwargs)
        else:
            raise ValueError(f"Tool '{tool_name}' not found in the registry.")