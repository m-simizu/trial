ifeq ($(OS),Windows_NT)
RUSTC ?= rustc +stable-x86_64-pc-windows-gnu
EXE = .exe
else
RUSTC ?= rustc
EXE =
endif

CC ?= gcc
UNITY_SRC = third_party/unity/src
RUST_OBJ = gcd.o
TEST_EXE = unity_test_gcd$(EXE)

.PHONY: all test clean

all: $(TEST_EXE)

$(RUST_OBJ): gcd.rs
	$(RUSTC) --emit=obj --crate-type=lib -C opt-level=2 -C panic=abort gcd.rs -o $(RUST_OBJ)

$(TEST_EXE): unity_test_gcd.c gcd.h $(RUST_OBJ) $(UNITY_SRC)/unity.c $(UNITY_SRC)/unity.h $(UNITY_SRC)/unity_internals.h
	$(CC) unity_test_gcd.c $(UNITY_SRC)/unity.c $(RUST_OBJ) -I. -I$(UNITY_SRC) -o $(TEST_EXE)

test: all
	./$(TEST_EXE)

clean:
	rm -f $(RUST_OBJ) $(TEST_EXE)
