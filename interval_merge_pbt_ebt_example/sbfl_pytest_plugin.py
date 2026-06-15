"""SBFL測定用に、pytestのテスト単位の合否をJSONへ保存する。"""

import json
from pathlib import Path


TEST_RESULTS: dict[str, dict[str, str]] = {}


def pytest_addoption(parser):
    parser.addoption(
        "--sbfl-results-file",
        action="store",
        default=None,
        help="テスト単位の合否を書き出すJSONファイル",
    )


def pytest_runtest_logreport(report):
    """setup/call/teardownの結果から、各pytestテストの最終状態を記録する。"""
    nodeid = report.nodeid

    if report.when == "setup" and report.failed:
        TEST_RESULTS[nodeid] = {"nodeid": nodeid, "status": "failed"}
        return

    if report.when == "setup" and report.skipped:
        TEST_RESULTS[nodeid] = {"nodeid": nodeid, "status": "skipped"}
        return

    if report.when == "call":
        if hasattr(report, "wasxfail"):
            status = "xfailed" if report.skipped else "xpassed"
        elif report.passed:
            status = "passed"
        elif report.failed:
            status = "failed"
        else:
            status = "skipped"

        TEST_RESULTS[nodeid] = {"nodeid": nodeid, "status": status}
        return

    if report.when == "teardown" and report.failed:
        TEST_RESULTS[nodeid] = {"nodeid": nodeid, "status": "failed"}


def pytest_sessionfinish(session, exitstatus):
    """テストセッション終了時に結果をJSONへ保存する。"""
    output = session.config.getoption("--sbfl-results-file")
    if output is None:
        return

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "pytest_exit_status": exitstatus,
        "tests": sorted(TEST_RESULTS.values(), key=lambda result: result["nodeid"]),
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
