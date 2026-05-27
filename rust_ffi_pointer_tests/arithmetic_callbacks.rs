type ArithmeticCallback = extern "C" fn(i32, i32) -> i32;

#[no_mangle]
pub extern "C" fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[no_mangle]
pub extern "C" fn subtract(a: i32, b: i32) -> i32 {
    a - b
}

#[no_mangle]
pub extern "C" fn multiply(a: i32, b: i32) -> i32 {
    a * b
}

#[no_mangle]
pub extern "C" fn divide(a: i32, b: i32) -> i32 {
    if b == 0 {
        return 0;
    }
    if a == i32::MIN && b == -1 {
        return i32::MIN;
    }

    a / b
}

#[no_mangle]
pub extern "C" fn calculate(x: i32, y: i32, callback: ArithmeticCallback) -> i32 {
    callback(x, y)
}

#[cfg(not(arithmetic_callbacks_no_main))]
fn main() {
    let a = 10;
    let b = 5;

    println!("add: {}", calculate(a, b, add));
    println!("subtract: {}", calculate(a, b, subtract));
    println!("multiply: {}", calculate(a, b, multiply));
    println!("divide: {}", calculate(a, b, divide));
}
