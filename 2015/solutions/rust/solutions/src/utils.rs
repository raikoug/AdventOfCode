use std::fs;
use std::path::Path;

pub fn read_input(day: u8) -> String {
    let filename = format!("src/inputs/day_{:02}.txt", day);
    fs::read_to_string(Path::new(&filename)).expect("Errore nella lettura del file di input")
}
