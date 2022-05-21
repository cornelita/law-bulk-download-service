from grpc_tools import protoc

protoc.main((
    '',
    '--proto_path=./bd_service/api/protoc/protos',
    '--python_out=.',
    '--grpc_python_out=.',
    './bd_service/api/protoc/protos/download.proto',
))
