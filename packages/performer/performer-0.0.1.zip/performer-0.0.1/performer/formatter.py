from performer import color

class Formatter(object):
    _output_format = lambda t, s: '[ ' + str(t).ljust(22) + ' ] : ' + str(s)

    @classmethod
    def func_name(cls, name):
        return cls._output_format(color.green('Function name'), name)

    @classmethod
    def return_value(cls, value):
        return cls._output_format(color.red('Return value'), value)

    @classmethod
    def loop_count(cls, count):
        return cls._output_format(color.yellow('Loop count'), count)

    @classmethod
    def average(cls, sec):
        return cls._output_format(color.blue('Average sec'), str(sec) + ' / s')

    @classmethod
    def total(cls, sec):
        return cls._output_format(color.magenta('Total sec'), str(sec) + ' / s')