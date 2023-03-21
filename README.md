# pyprotogen

Lib for generation *_pb2.py from *.proto with helper methods

## Installation
```shell
pip install pyprotogen
```

## Usage
### Generation
  ```shell
  pyprotogen path/to/input/hello.proto path/to/output/
  ```
### Generate as python-package
  ```shell
  pyprotogen path/to/input/hello.proto path/to/package/output --package-version=0.0.1 --package-authors="Rick, Morty" --name="Package"
  ```
- `--name` — optional;
- `--package-version` — required;
- `--package-authors` — optional;
- `path/to/package/output` — path to the directory where package will be saved.
### Usage
- As client
  ```python
  from package.client import get_channel
  from package.gen.hello_pb2_grpc import HelloStub

  channel = get_channel(host="your.host")
  stub = HelloStub(channel)
  ```
- As server
    ```python
  from package.server import get_server
  from package.gen.hello_pb2_grpc import add_HelloServicer_to_server
  from package.gen.hello_pb2_grpc import HelloServicer

  class Hello(HelloServicer):
      pass

  server = get_server()
  add_HelloServicer_to_server(Hello(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()
  ```

## Development
- Activate environment
  ```shell
  rm -rf .venv || true
  python3 -m venv .venv
  source .venv/bin/activate
  make requirements
  ```
- Make changes
- Execute `make test`
