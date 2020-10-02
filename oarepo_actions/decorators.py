def action(**kwargs):
    def wrapper(function):
        function.__action = kwargs
        return function
    return wrapper

