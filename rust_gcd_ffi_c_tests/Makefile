ifeq ($(OS),Windows_NT)
RUSTC ?= rustc +stable-x86_64-pc-windows-gnu
else
RUSTC ?= rustc
endif
CC ?= gcc

ifeq ($(OS),Windows_NT)
RUST_OBJ = gcd.o
EXE = .exe
else
RUST_OBJ = gcd.o
EXE =
endif

TESTS = c_test_gcd_common_factor c_test_gcd_coprime c_test_gcd_argument_order

.PHONY: all test clean

all: $(RUST_OBJ) $(addsuffix $(EXE),$(TESTS))

$(RUST_OBJ): gcd.rs
	$(RUSTC) --emit=obj --crate-type=lib -C opt-level=2 -C panic=abort gcd.rs -o $(RUST_OBJ)

%$(EXE): %.c gcd.h $(RUST_OBJ)
	$(CC) $< $(RUST_OBJ) -o $@

test: all
	./c_test_gcd_common_factor$(EXE)
	./c_test_gcd_coprime$(EXE)
	./c_test_gcd_argument_order$(EXE)

clean:
	rm -f $(RUST_OBJ) $(addsuffix $(EXE),$(TESTS))
