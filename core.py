import inspect
import copy


def try_copy(data):
    # some inner structure use dict.
    if isinstance(data, dict):
        ret = {}
        for i in data:
            new_copy = try_copy(data[i])
            if new_copy:
                ret[i] = new_copy
        return ret
    else:
        try:
            # copy data
            return copy.deepcopy(data)
        except Exception as e:
            # if the data can't be copied
            pass
    # just return data.
    return data


def convert_stack_to_dict(stack):
    keys = ['frame', 'file_name','line_number','function_name','codes','index']
    ret = {}
    for i,value in enumerate(stack):
        ret[keys[i]] = value
    return ret


class MyException(Exception):
    def __init__(self, msg):
        super(MyException, self).__init__(msg)
        stack = inspect.stack()[1]
        frame = convert_stack_to_dict(stack)['frame']
        self.local_vars = try_copy(frame.f_locals)


    def __str__(self):
        return str(self.local_vars)


def catch_local_vars(code, env=None, stop=-1):
    if env is None:
        env = {}

    if stop >= 0:
        lines = code.split('\n')
        while stop > 0:
            if len(lines[stop].strip()) == 0:
                stop -= 1
            elif lines[stop][-1] == ':':
                stop -= 1
            else:
                break
        lines[stop] = lines[stop] + ';raise MyException("xx")'
        code ='\n'.join(lines)
        env['MyException'] = MyException

    try:
        exec code in env
        local_vars = {}
        err = ''
    except MyException as e:
        local_vars = e.local_vars
        err = 'catch local vars'
    except Exception as e:
        local_vars = {}
        err = str(e)

    return env, local_vars, err
