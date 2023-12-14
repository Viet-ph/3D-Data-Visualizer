from cx_Freeze import setup, Executable

# ADD FILES
files = ['icon.ico','themes/', 'PlotImages/', 'configurations/']

# TARGET
target = Executable(
    script="main.py",
    base="Win32GUI",
    icon="GESLogo.ico"
)

# SETUP CX FREEZE
setup(
    name = "DataVisualizer",
    version = "1.0.0",
    description = "GES Data Visualizer",
    author = "GES",
    options = {'build_exe' : {'packages':['numpy', 'pandas'], 'include_files' : files}},
    executables = [target]      
)
