from mporm.dsn import DSN
from mporm.fields import Field
from mporm.oper import Operator


# You can't import `mporm.schema` in this file!!

__dsn__ = "__dsn__"
__prefix__ = "__prefix__"


class Expr:
    def __init__(self, model, **kwargs):
        self.params: dict = kwargs
        self.reflect:  dict = model.__dict__
        self.md_name:   str = model.__name__.lower()
        self.dsn:       DSN = self.reflect.get(__dsn__)
        self.tb_prefix: str = self.reflect.get(__prefix__)
        self.tb_name:   str = self.md_name if not self.tb_prefix else f"{self.tb_prefix.lower()}_{self.md_name}"

        self.fields: [tuple] = [(k, v.__dict__) for k, v in self.reflect.items() if isinstance(v, Field)]

        self.fields.append(("created_at", model.created_at.__dict__))
        self.fields.append(("updated_at", model.updated_at.__dict__))
        self.fields.append(("id", model.id.__dict__))

        self.operator = Operator(self)
