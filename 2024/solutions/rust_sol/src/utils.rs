use std::fs;
use std::path::Path;

pub fn read_input(day: u8) -> String {
    let filename = format!("/home/raikoug/SyncThing/SharedCodeTest/adventOfCode/2024/inputs/day_{:02}/input_1.txt", day);
    println!("{filename}");
    fs::read_to_string(Path::new(&filename)).expect("Errore nella lettura del file di input")
}
