from elements import Transition, ConnectorType

plantuml_code = [
    "START -> Advertising",
    "Connecting --> Advertising",
    "Connecting -left-> Advertising : $RTx_ConnectReq",
    "Connecting -up-> Advertising : $RTx_ConnectReq\n$RTx_ConnectedInd",
    "Connecting -----> Advertising : $RTx_ConnectReq\n$RTx_ConnectedInd"
]

for code in plantuml_code:
    transition = Transition.from_plantuml_code(code)
    print(transition.get_plantuml_code())


