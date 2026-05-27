use std::os::raw::c_int;

#[no_mangle]
pub extern "C" fn read_or_default(value: *const c_int, default_value: c_int) -> c_int {
    if value.is_null() {
        return default_value;
    }

    unsafe { *value }
}

#[no_mangle]
pub extern "C" fn write_if_not_null(target: *mut c_int, value: c_int) -> c_int {
    if target.is_null() {
        return 0;
    }

    unsafe {
        *target = value;
    }
    1
}

#[cfg(not(null_pointer_no_main))]
fn main() {
    let value = 42;
    let mut target = 0;

    println!(
        "read_or_default(&value, -1): {}",
        read_or_default(&value, -1)
    );
    println!(
        "read_or_default(NULL, -1): {}",
        read_or_default(std::ptr::null(), -1)
    );
    println!(
        "write_if_not_null(&target, 99): {}",
        write_if_not_null(&mut target, 99)
    );
    println!("target: {}", target);
    println!(
        "write_if_not_null(NULL, 99): {}",
        write_if_not_null(std::ptr::null_mut(), 99)
    );
}
