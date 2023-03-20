from pathlib import Path

from grpc_tools import protoc
from pyprotogen import settings
import shutil


def copy_dependencies(output_path: str) -> None:
    shutil.copytree(settings.DEPENDENCIES_DIR_PATH, Path(output_path).absolute(), dirs_exist_ok=True)


def gen_pb2_files(proto_path: str, output_path: str) -> None:
    grpc_gen_path = Path(output_path).joinpath(settings.GRPC_GEN_PATH)
    grpc_gen_path.mkdir(parents=True, exist_ok=True)

    protoc.main((
        '',
        f'--proto_path={grpc_gen_path}={Path(proto_path).parent}',
        '--python_out=./',
        '--mypy_out=./',
        '--grpc_python_out=./',
        proto_path,
    ))
