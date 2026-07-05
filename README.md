# K-Means Cluster Tool

先頭列を ID、2 列目以降を特徴量として KMeans クラスタリングを実行する Windows 向けツールです。CLI と GUI の両方に対応しています。

## 必要な依存関係

- numpy
- openpyxl
- pyinstaller

インストール例:

```powershell
python -m pip install numpy openpyxl pyinstaller
```

## 使い方

### CLI

```powershell
python k-means_cluster.py input.xlsx 3 --output result.xlsx
```

### GUI

```powershell
python kmeans_gui.py
```

または `run_gui.bat` をダブルクリックしてください。

GUI では出力ファイルではなく出力先フォルダを指定します。保存されるファイル名は `（入力ファイル名）_result` がベースになり、末尾に `月日時分` が自動付与されます。

## exe の作成

`build_exe.bat` を実行すると、`PyInstaller --onefile --windowed` で GUI アプリをビルドします。

生成物:

- `dist\KMeansClusterGUI.exe`

ビルド前に `build`、`dist`、`.pyinstaller` は自動で削除されます。

## 配布時の注意

- 対象 OS は Windows を前提にしています。
- 初回起動時は `--onefile` の展開で少し時間がかかることがあります。
- Windows Defender などのセキュリティソフトが exe を確認する場合があります。
- アイコン差し替え、インストーラー化、コード署名は未対応です。

## 配布用ファイル

- `dist\KMeansClusterGUI.exe`
- `DISTRIBUTION_MESSAGE.md`
- `USER_MANUAL.md`

配布時は上記 3 点を一緒に渡すと案内しやすくなります。

## 現在の仕様

- 入力対応形式は `.csv` / `.xlsx` のみです。
- 出力対応形式は `.csv` / `.xlsx` のみです。
- GUI では出力ファイル名を直接指定せず、出力先フォルダを指定します。
- 保存名は `（入力ファイル名）_result_月日時分` 形式で自動生成されます。
