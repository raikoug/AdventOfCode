
extern crate rust;

fn main() {
    // get file content and print it
    let content: Vec<String> = rust::get_file_content(5, false).unwrap();

    rust::day_22::solve(content);

    
}
