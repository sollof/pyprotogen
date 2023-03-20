from pathlib import Path


GRPC_GEN_PATH = "gen"

CURRENT_DIR_PATH = Path(__file__).parent.absolute()
TEMPLATES_DIR_PATH = CURRENT_DIR_PATH / Path("templates")
DEPENDENCIES_DIR_PATH = CURRENT_DIR_PATH / Path("dependencies")
