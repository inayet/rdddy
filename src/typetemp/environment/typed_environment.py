from jinja2 import Environment, FileSystemLoader

from typetemp.extension.faker_extension import FakerExtension
from typetemp.extension.inflection_extension import InflectionExtension


class TypedEnvironment(Environment):
    def __init__(self, **kwargs):
        super(TypedEnvironment, self).__init__(trim_blocks=True, lstrip_blocks=True, **kwargs)

        self.add_extension(FakerExtension)
        self.add_extension(InflectionExtension)
        self.add_extension("jinja2_time.TimeExtension")
        self.add_extension("jinja2.ext.i18n")
        self.add_extension("jinja2.ext.debug")
        self.add_extension("jinja2.ext.do")
        self.add_extension("jinja2.ext.loopcontrols")


# Initializing environment instances

file_loader = FileSystemLoader("./templates")

environment = TypedEnvironment(loader=file_loader)

async_environment = TypedEnvironment(enable_async=True, loader=file_loader)
