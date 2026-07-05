@echo off
setlocal

cd /d "%~dp0"

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"
set "PYINSTALLER_CONFIG_DIR=%CD%\.pyinstaller"
set "UPX_EXE=C:\upx\upx.exe"

echo [INFO] Using Python: %PYTHON_EXE%
if exist "%UPX_EXE%" (
    echo [INFO] Using UPX: %UPX_EXE%
) else (
    echo [INFO] UPX not found. Building without UPX compression.
)

tasklist /FI "IMAGENAME eq KMeansClusterGUI.exe" | find /I "KMeansClusterGUI.exe" >NUL
if not errorlevel 1 (
    echo [ERROR] KMeansClusterGUI.exe is currently running. Please close the app and run build_exe.bat again.
    exit /b 1
)

for %%D in (build dist .pyinstaller) do (
    if exist "%%D" (
        echo [INFO] Removing %%D
        rmdir /s /q "%%D"
    )
)

echo [INFO] Installing build dependencies
call "%PYTHON_EXE%" -m pip install numpy openpyxl pyinstaller
if errorlevel 1 goto :error

echo [INFO] Building exe
if exist "%UPX_EXE%" (
  call "%PYTHON_EXE%" -m PyInstaller ^
    --noconfirm ^
    --clean ^
    --upx-dir "C:\upx" ^
    "KMeansClusterGUI.spec"
) else (
  call "%PYTHON_EXE%" -m PyInstaller ^
    --noconfirm ^
    --clean ^
    "KMeansClusterGUI.spec"
)
if errorlevel 1 goto :error

echo [INFO] Build completed
echo [INFO] Output: dist\KMeansClusterGUI.exe
goto :end

:error
echo [ERROR] Build failed.
exit /b 1

:end
endlocal
