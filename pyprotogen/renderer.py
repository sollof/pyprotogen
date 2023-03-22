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

    for proto_file in proto_files:
        protoc.main((
            '',
            f'--proto_path={grpc_gen_path}={proto_dir}',
            '--python_out=./',
            '--mypy_out=./',
            '--grpc_python_out=./',
            str(proto_file),
        ))
