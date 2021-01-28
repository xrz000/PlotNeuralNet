import os
import jinja2


DEFAULT_TEMPLATE = os.path.join(os.path.dirname(__file__), "templates", "default.tex")


def generate(arch, save_path, template_path=DEFAULT_TEMPLATE):
    if os.path.exists(save_path):
        raise ValueError("Target file exists")
    template_dir, template_name = os.path.split(template_path)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    variables = {
        "import_path": os.path.join(os.path.dirname(__file__), "layers"),
        "arch": arch,
    }
    results = template.render(**variables)
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(results)
    # print(results)
