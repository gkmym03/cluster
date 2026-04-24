import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os
from datetime import datetime


def show_plot_if_available(scaled_data, clusters, centers, k):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        messagebox.showwarning(
            "グラフ省略",
            "matplotlib がないため、2次元散布図の表示を省略しました。"
        )
        return

    plt.scatter(scaled_data[:, 0], scaled_data[:, 1], c=clusters, cmap='viridis')
    plt.scatter(centers[:, 0], centers[:, 1], s=300, c='red', marker='X')
    plt.title(f'K-means Clustering (k={k})')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.show()

def run_clustering(data_path, k):
    try:
        # データの読み込み
        data = pd.read_csv(data_path)
        print("データを読み込みました。")
        print(data.head())

        # A列を除外してクラスタリング
        if 'A' in data.columns:
            print('列Aを除外して分析します。')
            data_for_clustering = data.drop(columns=['A'])
        else:
            data_for_clustering = data

        numeric_data = data_for_clustering.select_dtypes(include=[float, int])

        # データの標準化
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(numeric_data)

        # k-meansクラスタリングの実行
        kmeans = KMeans(n_clusters=k, random_state=42)
        clusters = kmeans.fit_predict(scaled_data)

        # クラスタラベルを1から始まるように調整
        clusters = clusters + 1

        # 結果をデータフレームに追加
        data['Cluster'] = clusters

        # 可視化（2次元の場合のみ）
        if numeric_data.shape[1] == 2:
            show_plot_if_available(scaled_data, clusters, kmeans.cluster_centers_, k)
        else:
            print("可視化は2次元データでのみサポートされています。")

        # クラスタリング結果を集計
        cluster_counts = data.groupby('Cluster').size().rename('Count')
        summary_columns = [col for col in numeric_data.columns if col != 'A']
        cluster_means = data.groupby('Cluster')[summary_columns].mean()
        cluster_summary = pd.concat([cluster_counts, cluster_means], axis=1)

        # 出力ファイル名をデータファイル名に基づいて変更
        base_name = os.path.splitext(os.path.basename(data_path))[0]
        timestamp = datetime.now().strftime("%m%d%H%M")
        summary_output_path = f'{base_name}_{timestamp}_cluster_summary.csv'
        output_path = f'{base_name}_{timestamp}_clustered_data.csv'

        # 保存
        cluster_summary.to_csv(summary_output_path, index=True)
        data.to_csv(output_path, index=False)

        messagebox.showinfo("成功", f"クラスタリングが完了しました。\n集計ファイル: {summary_output_path}\n結果ファイル: {output_path}")
        print(f"各クラスターの件数と平均値を {summary_output_path} に保存しました。")
        print(f"結果を {output_path} に保存しました。")

    except Exception as e:
        messagebox.showerror("エラー", f"エラーが発生しました: {str(e)}")

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

def run():
    data_path = entry_file.get()
    try:
        k = int(entry_k.get())
        if k <= 0:
            raise ValueError("クラスター数は1以上で指定してください。")
        run_clustering(data_path, k)
    except ValueError as e:
        messagebox.showerror("入力エラー", str(e))

# GUI作成
root = tk.Tk()
root.title("K-means Clustering GUI")

tk.Label(root, text="データファイル (CSV):").grid(row=0, column=0, padx=10, pady=10)
entry_file = tk.Entry(root, width=50)
entry_file.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="選択", command=select_file).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="クラスター数:").grid(row=1, column=0, padx=10, pady=10)
entry_k = tk.Entry(root, width=10)
entry_k.grid(row=1, column=1, padx=10, pady=10)

tk.Button(root, text="実行", command=run).grid(row=2, column=0, columnspan=3, pady=20)

root.mainloop()
