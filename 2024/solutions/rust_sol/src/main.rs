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
        0 =>  days::day_00::start(&input),
        1 =>  days::day_01::start(&input),
        2 =>  days::day_02::start(&input),
        3 =>  days::day_03::start(&input),
        4 =>  days::day_04::start(&input),
        5 =>  days::day_05::start(&input),
        //6 =>  days::day_06::start(&input),
        7 =>  days::day_07::start(&input),
        //8 =>  days::day_08::start(&input),
        //9 =>  days::day_09::start(&input),
        10 => days::day_10::start(&input),
        11 => days::day_11::start(&input),
        //12 => days::day_12::start(&input),
        // Aggiungi altri giorni e parti qui
        _ => println!("Soluzione non implementata per questo giorno e parte"),
    }
}