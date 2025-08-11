import difflib
import glob
import os
import sys


def run_tests(solve, tests_dir, multiple_tests):
    input_files = sorted(glob.glob(os.path.join(tests_dir, "input*.txt")))
    if not input_files:
        print(f"No input*.txt files found in {tests_dir}")
        return

    for infile in input_files:
        testname = os.path.splitext(os.path.basename(infile))[0].replace("input", "")
        expected_file = os.path.join(tests_dir, f"expected{testname}.txt")
        output_file = os.path.join(tests_dir, f"output{testname}.txt")

        with open(infile, "r") as fin, open(output_file, "w") as fout:
            orig_stdin, orig_stdout = sys.stdin, sys.stdout
            sys.stdin, sys.stdout = fin, fout
            t = 1
            if multiple_tests:
                t = int(input())
            for _ in range(t):
                solve()
            sys.stdin, sys.stdout = orig_stdin, orig_stdout

        with open(output_file, "r") as f:
            output = f.read().strip()

        if os.path.exists(expected_file):
            with open(expected_file, "r") as f:
                expected = f.read().strip()

            if output == expected:
                print(f"[PASS] {os.path.basename(infile)}")
            else:
                print(f"[FAIL] {os.path.basename(infile)}")
                diff = difflib.unified_diff(
                    expected.splitlines(),
                    output.splitlines(),
                    fromfile=f"expected{testname}.txt",
                    tofile=f"output{testname}.txt",
                    lineterm="",
                )
                for line in diff:
                    print(line)
        else:
            print(
                f"[NO EXPECTED] {os.path.basename(infile)} → output written to {os.path.basename(output_file)}"
            )


def main(solve, file_path, multiple_tests):
    filename = os.path.basename(file_path)
    problem_id = filename.replace("codeforces_", "").replace(".py", "")
    tests_dir = os.path.join(os.path.dirname(file_path), "tests", problem_id)
    run_tests(solve, tests_dir, multiple_tests)
