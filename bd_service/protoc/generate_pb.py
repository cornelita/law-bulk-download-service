from grpc_tools import protoc

protoc.main((
    '',
    '--proto_path=./bd_service/protoc/protos',
    '--python_out=.',
    '--grpc_python_out=.',
    './bd_service/protoc/protos/download.proto',
))
