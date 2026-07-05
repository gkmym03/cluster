# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
import sys


project_dir = Path.cwd()
python_base = Path(sys.base_prefix)

datas = []
hiddenimports = [
    "tkinter",
    "_tkinter",
]

def collect_data_tree(source_dir: Path, target_root: str):
    collected = []
    if not source_dir.exists():
        return collected

    for path in source_dir.rglob("*"):
        if path.is_file():
            relative_parent = path.relative_to(source_dir).parent
            target_dir = Path(target_root) / relative_parent
            collected.append((str(path), str(target_dir)))
    return collected


tcl_dir = python_base / "tcl" / "tcl8.6"
tk_dir = python_base / "tcl" / "tk8.6"
datas += collect_data_tree(tcl_dir, "_tcl_data")
datas += collect_data_tree(tk_dir, "_tk_data")


a = Analysis(
    ["kmeans_gui.py"],
    pathex=[str(project_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=["pyi_rth_kmeans_tk.py"],
    excludes=[
        "IPython",
        "PIL",
        "bs4",
        "lxml",
        "matplotlib",
        "numba",
        "pandas",
        "pyarrow",
        "pytest",
        "scipy",
        "sqlalchemy",
        "tables",
        "xlrd",
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="KMeansClusterGUI",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
