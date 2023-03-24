import re
from importlib import resources
from pathlib import Path

from grpc_tools import protoc
from pyprotogen import settings
import shutil


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
    proto_include = resources.path('grpc_tools', '_proto')
    include = ['-I{}'.format(proto_include)]
    protoc.main(args + include)

    for file in grpc_gen_path.iterdir():
        with open(file, "r") as sources:
            lines = sources.readlines()
        with open(file, "w") as sources:
            for line in lines:
                if re.search(r'^import .*_pb2 as', line) is not None:
                    line = 'from . ' + line
                sources.write(line)
