from pathlib import Path
from typer.testing import CliRunner
from pyprotogen import main
from tempfile import TemporaryDirectory

runner = CliRunner()

PROTO_PATH = "tests/protos"
GEN_DIR = 'genpack'


def test_entrypoint() -> None:
    with TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir).joinpath(GEN_DIR)
        result = runner.invoke(main.app, [PROTO_PATH, str(tmp_path.absolute())])

    assert result.exit_code == 0
