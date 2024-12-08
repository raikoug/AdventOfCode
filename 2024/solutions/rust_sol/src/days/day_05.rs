
pub fn is_valid_update(update: Vec<u32>, rules: Vec<Vec<u32>>) -> bool{
    let mut result: bool = true;
    for rule in rules {
        let a: u32 = rule.get(0).unwrap().clone();
        let b: u32 = rule.get(1).unwrap().clone();
        let mut index_a: usize = usize::MAX;
        let mut index_b: usize = usize::MAX;

        for (index, value) in update.iter().enumerate(){
            if *value == a {
                index_a = index;
            } else if *value == b {
                index_b = index;
                break
            }
        }
        
        if index_a > 1000 || index_b > 1000{
            //we dont need this now
            continue
        }
        else if index_b < index_a {
            result = false;
            break
            
        }
    }
    result
}

pub fn _part_1(_input: &str) {
    let mut rules: Vec<Vec<u32>> = Vec::new();
    let mut updates: Vec<Vec<u32>> = Vec::new();
    let mut total: u32 = 0;
    _input.lines().for_each(|line| {
        if line.contains("|") {
            let rule: Vec<u32> = line.split("|").map(|x| x.parse::<u32>().unwrap()).collect();
            rules.push(rule);
        } else if line.contains(",") {
            updates.push(line.split(",").map(|x| x.parse::<u32>().unwrap()).collect());
        }
    });
    updates.iter().for_each(|update|{
        if is_valid_update(update.clone(), rules.clone()){
            println!("{:?}",update);
            total += update.get(update.len() / 2).unwrap();
        }
    });

    println!("Day 5, Parte 1: {total}");
}

pub fn _part_2(_input: &str) {
    println!("Day 5, Parte 2: ");

}

pub fn start(input: &str){
    _part_1(input);
    _part_2(input);
}