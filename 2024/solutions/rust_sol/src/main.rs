mod utils;
mod days;

use std::io;

fn main() {
    println!("Inserisci il giorno (es. 4 per il day_04):");
    let mut day_input = String::new();
    io::stdin().read_line(&mut day_input).expect("Errore nella lettura dell'input");
    let day: u8 = day_input.trim().parse().expect("Inserisci un numero valido!");

    let input = utils::read_input(day);
    
    match day {
        1 => days::day_01::start(&input),
        //(2, 1) => days::day_02::part_1(&input),
        //(2, 2) => days::day_02::part_2(&input),
        //(3, 1) => days::day_03::part_1(&input),
        //(3, 2) => days::day_03::part_2(&input),
        //(4, 1) => days::day_04::part_1(&input),
        //(4, 2) => days::day_04::part_2(&input),
        //(6, 1) => days::day_06::part_1(&input),
        //(6, 2) => days::day_06::part_2(&input),
        // Aggiungi altri giorni e parti qui
        _ => println!("Soluzione non implementata per questo giorno e parte"),
    }
}