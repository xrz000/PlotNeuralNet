import os
import jinja2
from plotnn.tikzeng import Block


DEFAULT_TEMPLATE = os.path.join(os.path.dirname(__file__), "templates", "default.tex")


def flatten(s):
    results = []
    for item in s:
        if isinstance(item, list) or isinstance(item, tuple):
            results.extend(flatten(item))
        elif isinstance(item, Block):
            results.extend(flatten(item.layers))
        else:
            results.append(item)
    return results


def generate(archs, save_path, template_path=DEFAULT_TEMPLATE):
    if os.path.exists(save_path):
        raise ValueError("Target file exists")
    template_dir, template_name = os.path.split(template_path)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    figs = []
    for arch in archs:
        arch = flatten(arch)
        figs.append([layer.to_tex() for layer in arch])
    variables = {
        "import_path": os.path.join(os.path.dirname(__file__), "layers"),
        "figs": figs,
    }
    results = template.render(**variables)
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(results)
