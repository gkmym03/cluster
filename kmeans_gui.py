from pathlib import Path

from tk_env import configure_tk_environment

configure_tk_environment()

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from kmeans_core import (
    SUPPORTED_INPUT_EXTENSIONS,
    format_summary,
    run_kmeans,
    setup_logger,
)


class KMeansApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("K-Means クラスタリング")
        self.root.resizable(False, False)

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar(value=str(Path.cwd()))
        self.cluster_count = tk.StringVar(value="3")
        self.status_text = tk.StringVar(value="入力ファイル、クラスタ数、出力先フォルダを指定してください。")

        self._build_widgets()

    def _build_widgets(self) -> None:
        main = ttk.Frame(self.root, padding=16)
        main.grid(row=0, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(main, text="入力ファイル").grid(row=0, column=0, sticky="w", pady=(0, 6))
        ttk.Entry(main, textvariable=self.input_path, width=52).grid(row=1, column=0, padx=(0, 8))
        ttk.Button(main, text="参照", command=self.select_input_file).grid(row=1, column=1)

        ttk.Label(main, text="クラスタ数").grid(row=2, column=0, sticky="w", pady=(12, 6))
        ttk.Entry(main, textvariable=self.cluster_count, width=12).grid(row=3, column=0, sticky="w")

        ttk.Label(main, text="出力先フォルダ").grid(row=4, column=0, sticky="w", pady=(12, 6))
        ttk.Entry(main, textvariable=self.output_path, width=52).grid(row=5, column=0, padx=(0, 8))
        ttk.Button(main, text="参照", command=self.select_output_folder).grid(row=5, column=1)

        ttk.Button(main, text="実行", command=self.execute, width=18).grid(row=6, column=0, sticky="w", pady=(18, 8))
        ttk.Label(main, textvariable=self.status_text, wraplength=420, foreground="#444444").grid(
            row=7, column=0, columnspan=2, sticky="w"
        )

    def select_input_file(self) -> None:
        filetypes = [("対応ファイル", "*.csv *.xlsx"), ("すべてのファイル", "*.*")]
        path = filedialog.askopenfilename(title="入力ファイルを選択", filetypes=filetypes)
        if not path:
            return
        self.input_path.set(path)

        self.output_path.set(str(Path(path).parent))
        self.status_text.set("入力ファイルを選択しました。実行ボタンで処理を開始できます。")

    def select_output_folder(self) -> None:
        path = filedialog.askdirectory(
            title="出力先フォルダを選択",
            initialdir=self.output_path.get() if self.output_path.get() else str(Path.cwd()),
            mustexist=True,
        )
        if path:
            self.output_path.set(path)

    def build_output_file_path(self, input_file: str, output_folder: str) -> str:
        input_path = Path(input_file)
        output_dir = Path(output_folder)
        return str(output_dir / f"{input_path.stem}_result{input_path.suffix.lower()}")

    def validate_inputs(self) -> tuple[str, int, str]:
        input_file = self.input_path.get().strip()
        output_folder = self.output_path.get().strip()
        cluster_text = self.cluster_count.get().strip()

        if not input_file:
            raise ValueError("入力ファイルを選択してください。")
        if Path(input_file).suffix.lower() not in SUPPORTED_INPUT_EXTENSIONS:
            raise ValueError("入力ファイルは .csv / .xlsx のいずれかを指定してください。")
        if not Path(input_file).exists():
            raise ValueError("入力ファイルが見つかりません。")

        if not cluster_text:
            raise ValueError("クラスタ数を入力してください。")
        try:
            n_clusters = int(cluster_text)
        except ValueError as error:
            raise ValueError("クラスタ数は整数で入力してください。") from error

        if not output_folder:
            raise ValueError("出力先フォルダを指定してください。")
        if not Path(output_folder).exists():
            raise ValueError("出力先フォルダが見つかりません。")
        if not Path(output_folder).is_dir():
            raise ValueError("出力先にはフォルダを指定してください。")

        return input_file, n_clusters, output_folder

    def execute(self) -> None:
        try:
            input_file, n_clusters, output_folder = self.validate_inputs()
        except ValueError as error:
            messagebox.showerror("入力エラー", str(error))
            self.status_text.set(str(error))
            return

        self.status_text.set("クラスタリングを実行しています...")
        self.root.update_idletasks()

        try:
            output_file = self.build_output_file_path(input_file, output_folder)
            _, summary = run_kmeans(input_file, n_clusters, output_file)
        except Exception as error:
            messagebox.showerror("実行エラー", str(error))
            self.status_text.set(f"エラー: {error}")
            return

        summary_text = format_summary(summary)
        messagebox.showinfo("処理完了", summary_text)
        self.status_text.set("処理が完了しました。")


def main() -> None:
    setup_logger(log_to_stdout=False)
    root = tk.Tk()
    ttk.Style(root).theme_use("clam")
    KMeansApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
