@echo off
echo PyInstaller を使用して exe ファイルを生成します...
python -m PyInstaller --clean --noconfirm --onefile --windowed --upx-dir C:\upx --exclude-module matplotlib --exclude-module PIL gui_app.py
echo 生成完了。exe ファイルが dist フォルダにあります。
pause
