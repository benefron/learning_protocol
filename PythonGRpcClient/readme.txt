
Change History

Sparrow App V4.10.2

 New functions
 - bool WriteChipID(string chipID);
 - string ReadChipID();
 - bool CloseConfiguration(int id);
 - bool ExportMeasurementData(string fullFilename);
 Changed functions
 - bool SetPixelMode(int pixelNr, int modeId);
 - bool SetPixelModeWell(int wellNR, int modeId);
 - bool SetPixelModeRow(int wellNr, int rowNr, int modeId);
 - bool SetPixelModeColumn(int wellNr, int columnNr, int modeId);
 - bool SetPixelModeRange(int pixelNrFrom, int pixelNrTo, int modeId);




Setup Python environment

1. Python side (client)
   To build client side scripts to automate SparrowApp measurements, there are 
   two alternatives: Visual Studio Code or Visual Studio

    1.  Python
        - install Python 3.10.6
          https://www.python.org/downloads/
        - gRPC is the communication library
          Install gRPC with tools:
          $ python -m pip install grpcio-tools
          Quick Start: https://grpc.io/docs/languages/python/quickstart/
        - pdoc3 is used to create html documentation
          Install pdoc3:
          $ python -m pip install pdoc3

    2.  Visual Studio Code
        - Install Visual Studio Code
        - Install Extensions in VSC:
            - Python extension for Visual Studio Code
            - vscode-proto3
            - python docstrings

        - Python packages
            - pdoc3

    3. Visual Studio 
        - 'Python Development' workload
          Run Visual Studio Installer
          Choose 'Modify'
          Select 'Workloads' tab
          Select 'Python development'
          Unselect Python version
          Click on 'Modify' (bottom right)

2. Files in the  PythonGRpcClient folder
    - _SetupPythonEnvironment.txt   -> this info file
    - contracts.proto               -> definition of the gRPC service
    - contracts_pb2.py              -> generated gRPC code
    - contracts_pb2_grpc.py         -> generated gRPC code
    - SparrowRpcService.py          -> client side API, to be used in client application
    - SparrowRpcService_demo...py   -> demo code

4. Way of work to use this gRPC functionality in a python client script:
    Check out how SparrowRpcService.py is used in one of the demo files ...

5. Way of work to extend gRPC service     

    1. Python side (client): Generate Python interfacing code
        1. The project 'Sandbox->PythonGRpcClient' 
                is used to define the gRPC interface and to generate the code
                
        2. Update proto file in the project 
            Sandbox->PythonGRpcClient -> contracts.proto

        3. Generate the new Python code files for the gRPC client 
            - run in terminal:
              python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. contracts.proto
            - two files are generated: contracts_pb2.py and contracts_pb2_grpc.py

        4. Adjust the code in SparrowRpcService.py, this is the API to be used in client code

        5. Create the new Html documentation with pdoc:
            run in terminal:
            pdoc --html --force .\SparrowRpcService.py
            
    2. C# side (server): 
        1. The project 'Tools->RpcSererviceGenerateProtoFiles'
                is used to define the gRPC interface and to generate the code
           The project 'Imec.Informed.Application'
                uses the generated code to implement the gRPC server

        2. Update proto file in the project 
            Tools -> RpcSererviceGenerateProtoFiles -> contracts.proto

        3. Build the project RpcSererviceGenerateProtoFiles
            New server code will be generated and copied to 
            - Imec.Informed.Application\ScriptingRpc
            - Sandbox\TestRpcService
            
        4. Adjust/Extend code in 
            - IGRpcServiceHandler.cs    -> interface to be applied by the class that implements the server code
            - ScriptingRpcService.cs    -> class that translates the gRPC calls to functions in the IGRpcServiceHandler interface
            - MainWindow.xaml.cs        -> here all the server functions are implemented


