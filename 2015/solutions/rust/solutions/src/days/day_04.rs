
use md5;
use rayon::prelude::*;
use std::time::Instant;

pub fn part_1(input: &str) {
    let initial_string = input;
    let target_prefix = "00000";

    let start_time = Instant::now();

    // Utilizziamo find_first per trovare il primo valore che soddisfa la condizione
    if let Some(i) = (0u64..u64::MAX)
        .into_par_iter()
        .find_first(|&i| {
            let input = format!("{}{}", initial_string, i);
            let hash = format!("{:x}", md5::compute(&input));
            hash.starts_with(target_prefix)
        })
    {
        let input = format!("{}{}", initial_string, i);
        let hash = format!("{:x}", md5::compute(&input));
        println!("Trovato! i = {}", i);
        println!("Hash: {}", hash);
        println!("Tempo trascorso: {:?}", start_time.elapsed());
    } else {
        println!("Nessun valore trovato che soddisfa la condizione.");
    }
}

pub fn part_2(input: &str) {
    let initial_string = input;
    let target_prefix = "000000";

    let start_time = Instant::now();

    // Utilizziamo find_first per trovare il primo valore che soddisfa la condizione
    if let Some(i) = (0u64..u64::MAX)
        .into_par_iter()
        .find_first(|&i| {
            let input = format!("{}{}", initial_string, i);
            let hash = format!("{:x}", md5::compute(&input));
            hash.starts_with(target_prefix)
        })
    {
        let input = format!("{}{}", initial_string, i);
        let hash = format!("{:x}", md5::compute(&input));
        println!("Trovato! i = {}", i);
        println!("Hash: {}", hash);
        println!("Tempo trascorso: {:?}", start_time.elapsed());
    } else {
        println!("Nessun valore trovato che soddisfa la condizione.");
    }
}
