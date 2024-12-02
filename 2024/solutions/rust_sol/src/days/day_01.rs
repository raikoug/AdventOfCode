
pub fn part_1(input: &str) {
    let mut column1: Vec<u32> = vec![];
    let mut column2: Vec<u32> = vec![];
    input.lines().for_each(|line| {
        // split line, first parama to append on column1 and second param to append on column2
        let mut split = line.split("   ");
        column1.push(split.next().unwrap().parse().unwrap());
        column2.push(split.next().unwrap().parse().unwrap());

    });
    // sort both column ascending
    column1.sort();
    column2.sort();
    
    // read both columns comparing each element at same index
    let mut i = 0;
    let mut distances: u32 = 0;
    while i < column1.len() {
        // increment distances by the absolute value of column1[i] - column2[i]
        distances += (column1[i] as i32 - column2[i] as i32).abs() as u32;
        i += 1;
    }

    println!("Day 01, Parte 1: {distances}");
}

pub fn part_2(input: &str) {
    let mut column1: Vec<u32> = vec![];
    let mut column2: Vec<u32> = vec![];
    input.lines().for_each(|line| {
        // split line, first parama to append on column1 and second param to append on column2
        let mut split = line.split("   ");
        column1.push(split.next().unwrap().parse().unwrap());
        column2.push(split.next().unwrap().parse().unwrap());

    });

    let mut i = 0;
    let mut distances: u32 = 0;
    while i < column1.len() {
        // increment distances by the absolute value of column1[i] - column2[i]
        let mut j = 0;
        while j < column1.len() {
            if column1[i] == column2[j] {
                distances += column1[i];
            }
            j += 1;
        }
        i += 1;
    }

    println!("Day 01, Parte 2: {distances}");

}

pub fn start(input: &str){
    part_1(input);
    part_2(input);
}