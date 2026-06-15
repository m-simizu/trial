"""EBT/PBTを個別実行し、行単位のSBFL表を作成する。"""

import argparse
import csv
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys

from coverage import Coverage, CoverageData


PROJECT_ROOT = Path(__file__).resolve().parent
SUT_PATH = PROJECT_ROOT / "interval_merger.py"
SUITES = {
    "ebt": PROJECT_ROOT / "tests" / "test_interval_merge_ebt.py",
    "pbt": PROJECT_ROOT / "tests" / "test_interval_merge_pbt.py",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="EBT/PBT別にef, nf, ep, npと疑惑値を計算します。"
    )
    parser.add_argument(
        "--label",
        default="mutant",
        help="結果フォルダ名に使うミュータント名。例: merge_touching_false",
    )
    parser.add_argument(
        "--formula",
        choices=("ochiai", "tarantula", "jaccard"),
        default="ochiai",
        help="疑惑値の計算式。既定値はochiaiです。",
    )
    return parser.parse_args()


def safe_label(label: str) -> str:
    """フォルダ名に使えない文字をアンダースコアへ変換する。"""
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", label).strip("._")
    return cleaned or "mutant"


def suspiciousness(ef: int, nf: int, ep: int, np: int, formula: str) -> float:
    """指定されたSBFL式で疑惑値を返す。"""
    if formula == "ochiai":
        denominator = math.sqrt((ef + nf) * (ef + ep))
        return ef / denominator if denominator else 0.0

    if formula == "tarantula":
        failed_rate = ef / (ef + nf) if ef + nf else 0.0
        passed_rate = ep / (ep + np) if ep + np else 0.0
        denominator = failed_rate + passed_rate
        return failed_rate / denominator if denominator else 0.0

    denominator = ef + ep + nf
    return ef / denominator if denominator else 0.0


def run_pytest_suite(suite: str, test_path: Path, output_dir: Path) -> tuple[Path, Path]:
    """1つのテスト種別を実行し、coverage DBと合否JSONを作る。"""
    coverage_file = output_dir / f".coverage.{suite}"
    result_file = output_dir / f"{suite}_test_results.json"
    log_file = output_dir / f"{suite}_pytest_output.txt"

    coverage_file.unlink(missing_ok=True)
    result_file.unlink(missing_ok=True)

    command = [
        sys.executable,
        "-m",
        "pytest",
        str(test_path),
        "-o",
        "addopts=-p no:cacheprovider",
        "--tb=short",
        "--cov=interval_merger",
        "--cov-branch",
        "--cov-context=test",
        "--cov-report=",
        "-p",
        "sbfl_pytest_plugin",
        f"--sbfl-results-file={result_file}",
    ]

    environment = os.environ.copy()
    environment["COVERAGE_FILE"] = str(coverage_file)
    environment["PYTHONIOENCODING"] = "utf-8"

    completed = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )

    output = completed.stdout + completed.stderr
    log_file.write_text(output, encoding="utf-8")
    print(f"\n===== {suite.upper()} =====")
    print(output)

    if completed.returncode not in (0, 1):
        raise RuntimeError(
            f"{suite}のpytest実行に失敗しました。詳細: {log_file}"
        )

    if not coverage_file.exists() or not result_file.exists():
        raise RuntimeError(f"{suite}の測定ファイルを作成できませんでした。")

    return coverage_file, result_file


def find_measured_sut(data: CoverageData) -> str:
    """coverage DB内からSUTの絶対パスを探す。"""
    expected = SUT_PATH.resolve()
    for filename in data.measured_files():
        if Path(filename).resolve() == expected:
            return filename
    raise RuntimeError(f"coverage DB内に{SUT_PATH.name}が見つかりません。")


def load_executable_lines(coverage_file: Path) -> list[int]:
    """SUTに存在する実行可能行を取得する。"""
    coverage = Coverage(data_file=str(coverage_file), branch=True)
    coverage.load()
    _, statements, _, _, _ = coverage.analysis2(str(SUT_PATH))
    return sorted(statements)


def load_test_results(result_file: Path) -> dict[str, str]:
    """passed/failedのpytestテストだけをSBFL対象として返す。"""
    payload = json.loads(result_file.read_text(encoding="utf-8"))
    return {
        item["nodeid"]: item["status"]
        for item in payload["tests"]
        if item["status"] in {"passed", "failed"}
    }


def load_line_contexts(coverage_file: Path) -> dict[int, set[str]]:
    """各行を実行したpytestテストIDの集合を取得する。"""
    data = CoverageData(basename=str(coverage_file))
    data.read()
    measured_sut = find_measured_sut(data)
    raw_contexts = data.contexts_by_lineno(measured_sut)

    line_contexts: dict[int, set[str]] = {}
    for line, contexts in raw_contexts.items():
        nodeids = {
            context.removesuffix("|run")
            for context in contexts
            if context.endswith("|run")
        }
        line_contexts[line] = nodeids
    return line_contexts


def calculate_rows(
    coverage_file: Path,
    result_file: Path,
    formula: str,
) -> tuple[list[dict[str, object]], dict[str, int]]:
    """SUTの実行可能行ごとにef, nf, ep, npと疑惑値を計算する。"""
    test_results = load_test_results(result_file)
    failed_tests = {nodeid for nodeid, status in test_results.items() if status == "failed"}
    passed_tests = {nodeid for nodeid, status in test_results.items() if status == "passed"}
    line_contexts = load_line_contexts(coverage_file)
    executable_lines = load_executable_lines(coverage_file)
    source_lines = SUT_PATH.read_text(encoding="utf-8").splitlines()

    rows: list[dict[str, object]] = []
    for line in executable_lines:
        executed = line_contexts.get(line, set())
        ef = len(executed & failed_tests)
        ep = len(executed & passed_tests)
        nf = len(failed_tests) - ef
        np = len(passed_tests) - ep
        score = suspiciousness(ef, nf, ep, np, formula)
        rows.append(
            {
                "line": line,
                "code": source_lines[line - 1].strip(),
                "ef": ef,
                "nf": nf,
                "ep": ep,
                "np": np,
                "suspiciousness": score,
            }
        )

    ranked = sorted(rows, key=lambda row: (-float(row["suspiciousness"]), int(row["line"])))
    previous_score: float | None = None
    current_rank = 0
    for position, row in enumerate(ranked, start=1):
        score = float(row["suspiciousness"])
        if previous_score is None or not math.isclose(score, previous_score):
            current_rank = position
            previous_score = score
        row["rank"] = current_rank

    return rows, {
        "passed": len(passed_tests),
        "failed": len(failed_tests),
        "total": len(test_results),
    }


def write_csv(path: Path, rows: list[dict[str, object]], ranked: bool = False) -> None:
    """行番号順または疑惑値順のCSVを保存する。"""
    output_rows = rows
    if ranked:
        output_rows = sorted(
            rows,
            key=lambda row: (int(row["rank"]), int(row["line"])),
        )

    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=("rank", "line", "code", "ef", "nf", "ep", "np", "suspiciousness"),
        )
        writer.writeheader()
        for row in output_rows:
            serialized = dict(row)
            serialized["suspiciousness"] = f'{float(row["suspiciousness"]):.6f}'
            writer.writerow(serialized)


def write_markdown(
    path: Path,
    suite: str,
    rows: list[dict[str, object]],
    counts: dict[str, int],
    formula: str,
) -> None:
    """確認しやすい疑惑値順Markdown表を保存する。"""
    ranked = sorted(rows, key=lambda row: (int(row["rank"]), int(row["line"])))
    lines = [
        f"# {suite.upper()} SBFL結果",
        "",
        f"- 計算式: `{formula}`",
        f'- 成功テスト: {counts["passed"]}',
        f'- 失敗テスト: {counts["failed"]}',
        "",
        "|順位|行|コード|ef|nf|ep|np|疑惑値|",
        "|---:|---:|---|---:|---:|---:|---:|---:|",
    ]
    for row in ranked:
        code = str(row["code"]).replace("|", "\\|")
        lines.append(
            f'|{row["rank"]}|{row["line"]}|`{code}`|{row["ef"]}|{row["nf"]}|'
            f'{row["ep"]}|{row["np"]}|{float(row["suspiciousness"]):.6f}|'
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_comparison(path: Path, suite_rows: dict[str, list[dict[str, object]]]) -> None:
    """EBT/PBTの値を同じ行で比較できるCSVを保存する。"""
    indexed = {
        suite: {int(row["line"]): row for row in rows}
        for suite, rows in suite_rows.items()
    }
    all_lines = sorted(set(indexed["ebt"]) | set(indexed["pbt"]))

    with path.open("w", newline="", encoding="utf-8-sig") as file:
        fieldnames = [
            "line",
            "code",
            "ebt_ef",
            "ebt_nf",
            "ebt_ep",
            "ebt_np",
            "ebt_suspiciousness",
            "pbt_ef",
            "pbt_nf",
            "pbt_ep",
            "pbt_np",
            "pbt_suspiciousness",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for line in all_lines:
            ebt = indexed["ebt"][line]
            pbt = indexed["pbt"][line]
            writer.writerow(
                {
                    "line": line,
                    "code": ebt["code"],
                    "ebt_ef": ebt["ef"],
                    "ebt_nf": ebt["nf"],
                    "ebt_ep": ebt["ep"],
                    "ebt_np": ebt["np"],
                    "ebt_suspiciousness": f'{float(ebt["suspiciousness"]):.6f}',
                    "pbt_ef": pbt["ef"],
                    "pbt_nf": pbt["nf"],
                    "pbt_ep": pbt["ep"],
                    "pbt_np": pbt["np"],
                    "pbt_suspiciousness": f'{float(pbt["suspiciousness"]):.6f}',
                }
            )


def main() -> int:
    args = parse_args()
    label = safe_label(args.label)
    output_dir = PROJECT_ROOT / "sbfl_results" / label
    output_dir.mkdir(parents=True, exist_ok=True)

    suite_rows: dict[str, list[dict[str, object]]] = {}
    summary: dict[str, object] = {
        "label": args.label,
        "formula": args.formula,
        "sut": str(SUT_PATH),
        "suites": {},
    }

    for suite, test_path in SUITES.items():
        coverage_file, result_file = run_pytest_suite(suite, test_path, output_dir)
        rows, counts = calculate_rows(coverage_file, result_file, args.formula)
        suite_rows[suite] = rows
        summary["suites"][suite] = counts

        write_csv(output_dir / f"{suite}_line_sbfl.csv", rows)
        write_csv(output_dir / f"{suite}_ranked_sbfl.csv", rows, ranked=True)
        write_markdown(
            output_dir / f"{suite}_sbfl.md",
            suite,
            rows,
            counts,
            args.formula,
        )

    write_comparison(output_dir / "ebt_pbt_comparison.csv", suite_rows)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\nSBFL結果を出力しました: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
