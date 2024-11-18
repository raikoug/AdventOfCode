pub fn part_1(input: &str) {
    println!("Esecuzione Day 04, Parte 1");
    let mut total_sqf : i32 = 0;
    input.lines().for_each(|line: &str| {
        let mut m : Vec<i32> = line.split('x').map(|x| x.parse::<i32>().unwrap()).collect();
        m.sort();
        let l: i32 = m[0];
        let w: i32 = m[1];
        let h: i32 = m[2];
        total_sqf += 2 * (l*w + w*h + h*l) + l*w;
        
        //println!("{:?}, {l} {w} {h}", M)
        
        
    });
    println!("{total_sqf}")
}

pub fn part_2(input: &str) {
    println!("Esecuzione Day 04, Parte 2");
    let mut total_rlf : i32 = 0;
    input.lines().for_each(|line: &str| {
        let mut m : Vec<i32> = line.split('x').map(|x| x.parse::<i32>().unwrap()).collect();
        m.sort();
        let l: i32 = m[0];
        let w: i32 = m[1];
        let h: i32 = m[2];
        total_rlf += 2*l+2*w+l*w*h
        
        //println!("{:?}, {l} {w} {h}", M)
        
        
    });
    println!("{total_rlf}")
}
