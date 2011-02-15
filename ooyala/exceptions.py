
class OoyalaParameterException(Exception):

    def __init__(self, param_name):
        self.parameter = param_name

    def __str__(self):
        return 'Parameter %s is required but is None' % repr(self.parameter)
