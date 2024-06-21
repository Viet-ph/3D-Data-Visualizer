from Windows.mainWindow import RunApp
import os

if __name__ == "__main__":
    os.environ["QSG_RHI_BACKEND"] = "opengl"
    RunApp()

