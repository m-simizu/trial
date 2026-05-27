# Rust gcd FFI tests with Unity

This folder is separate from the original assert-based C tests. It contains a Unity-based C test runner for the same Rust `gcd` implementation.

## Files

- `gcd.rs`: Rust implementation exported with `pub extern "C" fn`.
- `gcd.h`: C header declaring the Rust function for the C test.
- `unity_test_gcd.c`: Unity test cases.
- `run_unity_gcd_tests.ps1`: PowerShell build-and-test script.
- `Makefile`: Alternative `make test` entry point.
- `third_party/unity/src/`: Unity test framework source files.

## Run

```powershell
.\run_unity_gcd_tests.ps1
```

The script builds `gcd.rs` into `gcd.o`, compiles `unity_test_gcd.c` together with Unity's `unity.c`, links them into `unity_test_gcd.exe`, and runs that executable.

Expected output ends with a Unity summary similar to:

```text
3 Tests 0 Failures 0 Ignored
OK
```

## Why Unity

GoogleTest is probably the best-known name in the wider C/C++ testing world, but it is a C++ framework. For a pure C test framework, Unity is a widely used and lightweight choice, written in ANSI C and commonly used for C and embedded C projects.
