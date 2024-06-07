import os
import re
import shutil

from pathlib import Path

from grpc_tools import protoc
from jinja2 import Environment, FileSystemLoader

from pyprotogen import settings


def create_client(output_path: str, package_name: str) -> None:
    output_dir = Path(output_path)
    env = Environment(
        loader=FileSystemLoader(settings.TEMPLATES_DIR_PATH),
        extensions=['jinja2.ext.loopcontrols'],
    )
    template = env.get_template('client-py.j2')

    client_path = output_dir.joinpath('client.py')

    with open(client_path, 'w') as client_file:
        client_file.write(template.render(package_name=package_name))


def copy_dependencies(output_path: str) -> None:
    shutil.copytree(
        settings.DEPENDENCIES_DIR_PATH, Path(output_path).absolute(), dirs_exist_ok=True
    )


def gen_pb2_files(proto_path: str, output_path: str) -> None:
    grpc_gen_path = Path(output_path).joinpath(settings.GRPC_GEN_PATH)
    grpc_gen_path.mkdir(parents=True, exist_ok=True)

    proto_files = []
    path = Path(proto_path)
    if path.is_file():
        proto_dir = path.parent
        proto_files.append(str(path))
    else:
        proto_dir = path if path.is_dir() else path.parent
        for f in proto_dir.iterdir():
            if f.name.endswith('.proto'):
                proto_files.append(str(f))
    args = [
        '',
        f'--proto_path={proto_dir}',
        f'--python_out={grpc_gen_path}',
        f'--mypy_out={grpc_gen_path}',
        f'--grpc_python_out={grpc_gen_path}',
        *proto_files,
    ]
    proto_include = protoc.pkg_resources.resource_filename('grpc_tools', '_proto')
    include = ['-I{}'.format(proto_include)]
    protoc.main(args + include)

    for file in grpc_gen_path.rglob('*.py'):
        name, extension = os.path.splitext(file.name)
        if '.' in name:
            new_name = f'{name.replace(".", "/")}{extension}'
            os.rename(file, f'{file.parent}/{new_name}')

    for file in grpc_gen_path.rglob('*.py'):
        with open(file, "r") as sources:
            lines = sources.readlines()
        with open(file, "w") as sources:
            for line in lines:
                if re.search(r'^import .*_pb2 as', line) is not None:
                    line = 'from . ' + line
                if re.search(
                    r'^from .* import .*_pb2 as', line
                ) is not None and not line.startswith('from google.protobuf'):
                    line = 'from . import' + line.split('import')[1]
                sources.write(line)
