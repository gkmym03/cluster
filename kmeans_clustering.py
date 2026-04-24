import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import argparse
from datetime import datetime
import os

# コマンドライン引数のパーサーを作成
parser = argparse.ArgumentParser(description='K-means clustering script')
parser.add_argument('--data', type=str, default='data.csv', help='Path to the CSV data file (default: data.csv)')
parser.add_argument('n_clusters', type=int, help='Number of clusters')
args = parser.parse_args()

# データの読み込み（CSVファイルから）
data_path = args.data
try:
    data = pd.read_csv(data_path)
    print("データを読み込みました。")
    print(data.head())
except FileNotFoundError:
    print(f"ファイル {data_path} が見つかりません。ファイルパスを確認してください。")
    exit(1)

# 数値データのみを使用（カテゴリカルデータがある場合は前処理が必要）
# A列を除外してクラスタリング
if 'A' in data.columns:
    print('列Aを除外して分析します。')
    data_for_clustering = data.drop(columns=['A'])
else:
    data_for_clustering = data

numeric_data = data_for_clustering.select_dtypes(include=[float, int])

# データの標準化（k-meansはスケールに敏感）
scaler = StandardScaler()
scaled_data = scaler.fit_transform(numeric_data)

# クラスター数の指定
k = args.n_clusters

# k-meansクラスタリングの実行
kmeans = KMeans(n_clusters=k, random_state=42)
clusters = kmeans.fit_predict(scaled_data)

# クラスタラベルを1から始まるように調整
clusters = clusters + 1

# 結果をデータフレームに追加
data['Cluster'] = clusters

# 結果の出力
print("クラスタリング結果:")
print(data.head())

# 可視化（2次元の場合のみ。多次元の場合はPCAなどで次元削減が必要）
if numeric_data.shape[1] == 2:
    plt.scatter(scaled_data[:, 0], scaled_data[:, 1], c=clusters, cmap='viridis')
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='red', marker='X')
    plt.title(f'K-means Clustering (k={k})')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.show()
else:
    print("可視化は2次元データでのみサポートされています。")

# クラスタリング結果を集計
cluster_counts = data.groupby('Cluster').size().rename('Count')
# A列は出力対象外にする（分析のみに利用）
summary_columns = [col for col in numeric_data.columns if col != 'A']
cluster_means = data.groupby('Cluster')[summary_columns].mean()
cluster_summary = pd.concat([cluster_counts, cluster_means], axis=1)

# クラスタリングの集計結果を別ファイルに保存
base_name = os.path.splitext(os.path.basename(data_path))[0]
timestamp = datetime.now().strftime("%m%d%H%M")
summary_output_path = f'{base_name}_{timestamp}_cluster_summary.csv'
cluster_summary.to_csv(summary_output_path, index=True)
print(f"各クラスターの件数と平均値を {summary_output_path} に保存しました。")

# クラスタリング結果をCSVに保存
output_path = f'{base_name}_{timestamp}_clustered_data.csv'
data.to_csv(output_path, index=False)
print(f"結果を {output_path} に保存しました。")
