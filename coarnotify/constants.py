class ConstantList:
    @classmethod
    def all_constants(cls):
        att_names = cls.__dict__
        att_names = (i for i in att_names if not (i.startswith('__') and i.endswith('__')))
        return (getattr(cls, n) for n in att_names)

