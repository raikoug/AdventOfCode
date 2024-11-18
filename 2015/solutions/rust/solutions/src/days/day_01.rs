pub fn part_1(input: &str) {
    println!("Esecuzione Day 04, Parte 1");
    let mut res : i32 = 0;
    input.split("").for_each(|x| {
        if x == "(" {
            res += 1;
        } else if x == ")" {
            res -= 1;
        }

    });
    println!("{res}");
}

pub fn part_2(input: &str) {
    println!("Esecuzione Day 04, Parte 2");
    let mut res : i32 = 0;
    for (i, x) in input.split("").into_iter().enumerate(){
        if x == "(" {
            res += 1;
        } else if x == ")" {
            res -= 1;
        }
        if res == -1 {
            println!("{i}");
            break;
        }
    };

}
