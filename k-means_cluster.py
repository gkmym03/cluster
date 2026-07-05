import argparse
import sys

from kmeans_core import format_summary, run_kmeans, setup_logger


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="先頭列を ID、2 列目以降を特徴量として KMeans クラスタリングを実行します。"
    )
    parser.add_argument("input_file", help="入力ファイル (.csv/.xlsx)")
    parser.add_argument("n_clusters", type=int, help="クラスタ数")
    parser.add_argument("--output", default="kmeans_result.csv", help="出力ファイル (.csv/.xlsx)")
    return parser.parse_args()


def main() -> int:
    setup_logger(log_to_stdout=True)
    args = parse_args()
    try:
        result, summary = run_kmeans(args.input_file, args.n_clusters, args.output)
    except Exception as error:
        print(str(error), file=sys.stderr)
        return 1

    print(result.head())
    print("")
    print(format_summary(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
