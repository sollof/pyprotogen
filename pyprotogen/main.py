from typing import Optional

import typer

from pyprotogen import packager
from pyprotogen import renderer


app = typer.Typer()


@app.command()
def main(
    input: str = typer.Argument(..., help="input .proto file"),
    output: str = typer.Argument(..., help="client output file path"),
    name: str = typer.Option("Client", help="client class name"),
    package_version: Optional[str] = typer.Option(None, help="package version"),
    package_authors: Optional[str] = typer.Option(None, help="package authors"),
):
    package_name = ''
    if package_version:
        resp = packager.init_package(
            output_path=output,
            client_class_name=name,
            package_version=package_version,
            package_authors=package_authors,
        )
        output = resp.client_output_path
        package_name = resp.package_name

    renderer.gen_pb2_files(input, output)
    renderer.create_client(output, package_name)
    renderer.copy_dependencies(output)


def run() -> None:
    typer.run(main)


if __name__ == '__main__':
    app()
