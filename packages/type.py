def type_handler(content):
        print(type(content))
        if isinstance(content, dict):
            return "application/json"
        else:
            return "text/html"