
use std::fs;

pub fn common_function() {
    println!("Hello, world!");
}

pub fn get_file_path(day: u32, test: bool) -> String {
    let day_str = format!("{:02}", day);
    let file_name = if test { "test_input.txt" } else { "input.txt" };
    format!("C:\\Users\\raikoug\\SyncThing\\shared_code_tests\\adventOfCode\\2023\\day_{}\\{}", day_str, file_name)
}

pub fn get_file_content(day: u32, test: bool) -> Result<Vec<String>, std::io::Error> {
    let path = get_file_path(day, test);
    println!("path: {}", path);
    let content = fs::read_to_string(path)?;
    let lines = content.lines().map(|line| line.to_string()).collect();
    Ok(lines)
}