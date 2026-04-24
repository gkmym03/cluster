from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_exe_options = {
    "packages": ["os"],
    "excludes": [],
    "include_files": [],
    "upx": True
}

base = "gui"

executables = [
    Executable("gui_app.py", base=base, target_name="KMeansGUI.exe")
]

setup(
    name="KMeans Clustering GUI",
    version="1.0",
    description="GUI for K-means clustering",
    options={"build_exe": build_exe_options},
    executables=executables
)