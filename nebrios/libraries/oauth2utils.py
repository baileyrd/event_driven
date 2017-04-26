import re
import unidecode


def slugify(text):
    text = unidecode.unidecode(text).lower()
    return re.sub(r'\W+', '-', text)


def get_request_value(request, key, default=None):
    value = default
    if request.FORM:
        try:
            value = getattr(request.FORM, key)
            if value is None:
                value = default
        except:
            pass
    else:
        try:
            value = request.BODY.get(key, default)
        except:
            pass
    return value


def get_process(PROCESS=None, PROCESS_ID=None):
        if PROCESS is not None:
            return PROCESS
        elif PROCESS_ID is not None:
            return Process.objects.get(PROCESS_ID=PROCESS_ID)


class NebriOSModel(object):

    kind = None

    def __init__(self, PROCESS=None, PROCESS_ID=None, **kwargs):
        if self.__class__.kind is None:
            raise Exception('Model kind is None')
        self.__dict__['PROCESS'] = get_process(PROCESS=PROCESS, PROCESS_ID=PROCESS_ID)
        self.__setitem__('kind', self.__class__.kind)
        for key, value in kwargs.iteritems():
            self.__setitem__(key, value)

    def __setattr__(self, key, value):
        return self.__dict__['PROCESS'].__setattr__(key, value)

    def __getattr__(self, item):
        return self.__dict__['PROCESS'].__getattr__(item)

    def __setitem__(self, key, value):
        return self.__dict__['PROCESS'].__setitem__(key, value)

    def __getitem__(self, item):
        return self.__dict__['PROCESS'].__getitem__(item)

    def __set_reference__(self, model_instance, field_name):
        return self.__setitem__(field_name, model_instance.PROCESS_ID)

    def __get_reference__(self, model_class, field_name):
        return model_class(PROCESS_ID=self.__getitem__(field_name))

    def save(self):
        return self.__dict__['PROCESS'].save()

    @classmethod
    def get(cls, **kwargs):
        kwargs['kind'] = cls.kind
        p = Process.objects.get(**kwargs)
        return cls(PROCESS=p)

    @classmethod
    def filter(cls, **kwargs):
        kwargs['kind'] = cls.kind
        q = Process.objects.get(**kwargs)
        return [cls(PROCESS=p) for p in q]