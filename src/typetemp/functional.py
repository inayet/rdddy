import os
from pathlib import Path

from typetemp.environment.typed_environment import environment, to_kwarg
from typetemp.environment.typed_native_environment import native_environment

_env = environment
_native_env = native_environment


def render(tmpl_str_or_path: str | Path, to: str = "", **kwargs) -> str:
    """Render a template from a string or a file with the given keyword arguments."""
    # Check if tmpl_str_or_path is a path to a file
    if os.path.exists(tmpl_str_or_path) and Path(tmpl_str_or_path).is_file():
        with open(tmpl_str_or_path) as file:
            template_content = file.read()
    else:
        template_content = str(tmpl_str_or_path)

    template = _env.from_string(template_content)

    rendered = template.render(**kwargs)

    if to:
        to_ = _env.from_string(to)
        rendered_to = to_.render(**kwargs)

        with open(rendered_to, "w") as file:
            file.write(rendered)

    return rendered


def render_native(tmpl_str_or_path: str | Path, **kwargs) -> str:
    """Render a template from a string or a file with the given keyword arguments."""
    # Check if tmpl_str_or_path is a path to a file
    if os.path.exists(tmpl_str_or_path) and Path(tmpl_str_or_path).is_file():
        with open(tmpl_str_or_path) as file:
            template_content = file.read()
    else:
        template_content = str(tmpl_str_or_path)

    template = _native_env.from_string(template_content)

    return template.render(**kwargs)
