use regex::Regex;

pub fn _part_1(_input: &str) {
    let mul_pattern : Regex = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)").unwrap();
    let mut total: i32 = 0;

    mul_pattern.captures_iter(_input).for_each(|f: regex::Captures<'_>|{
        let a : i32 = f.get(1).unwrap().as_str().parse().unwrap();
        let b : i32 = f.get(2).unwrap().as_str().parse().unwrap();
        total += a*b;
    });

    //mul_pattern.find_iter(_input).for_each(|f| {
    //    println!("{:?}", f);
    //});
    println!("Day 03, Parte 1: {total}");
}

pub fn _part_2(_input: &str) {
    // Combina tutti i pattern in un singolo regex con gruppi nominati
    let combined_pattern = Regex::new(
        r"(?P<mul>mul\((\d{1,3}),(\d{1,3})\))|(?P<do>do\(\))|(?P<dont>don'?t\(\))"
    ).unwrap();

    let mut total: i32 = 0;
    let mut mul_enabled = true; // Le istruzioni mul() sono abilitate all'inizio

    // Itera su tutte le corrispondenze nell'input
    for cap in combined_pattern.captures_iter(_input) {
        if cap.name("do").is_some() {
            // Abilita le istruzioni mul()
            mul_enabled = true;
        } else if cap.name("dont").is_some() {
            // Disabilita le istruzioni mul()
            mul_enabled = false;
        } else if cap.name("mul").is_some() {
            // Se le istruzioni mul() sono abilitate, esegui la moltiplicazione
            if mul_enabled {
                let a: i32 = cap.get(2).unwrap().as_str().parse().unwrap();
                let b: i32 = cap.get(3).unwrap().as_str().parse().unwrap();
                total += a * b;
            }
        }
    }

    println!("Day 03, Parte 2: {total}");
}

pub fn start(input: &str){
    _part_1(input);
    _part_2(input);
}