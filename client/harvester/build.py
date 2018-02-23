import cx_Freeze

cx_Freeze.setup(
    name="harvester",
    version="1.0",
    description="monitors system resources and sends this information to a database",
    executables=[cx_Freeze.Executable("harvester.py")],
)