
pub fn check_numbers(numbers: Vec<i32>) -> bool {
    let mut ascending: bool = true;
    for i in 0..numbers.len()-1 {
        if numbers[i] >= numbers[i+1] {
            ascending = false;
            break;
        }
        else{
            if numbers[i+1] - numbers[i] > 3 {
                ascending = false;
                break;
            }
        }
    }

    let mut descending: bool = true;
    for i in 0..numbers.len()-1 {
        if numbers[i] <= numbers[i+1] {
            descending = false;
            break;
        }
        else{
            if numbers[i] - numbers[i+1] > 3 {
                descending = false;
                break;
            }
        }
    }
    if ascending || descending{
        return true
    }
    false
}

pub fn _part_1(_input: &str) {
    let mut result: i32 = 0;

    _input.lines().for_each(|line| {
        let numbers: Vec<i32> = line.split_whitespace().map(|x| x.parse::<i32>().unwrap()).collect();
        if check_numbers(numbers){
            result += 1;
        }
    });

    println!("Day 02, Parte 1: {result}");
}

pub fn _part_2(_input: &str) {
    let mut result: i32 = 0;

    _input.lines().for_each(|line| {
        let numbers: Vec<i32> = line.split_whitespace().map(|x| x.parse::<i32>().unwrap()).collect();
        let mut line_ok: bool = false;
        for i in 0..numbers.len() {
            let mut new_numbers: Vec<i32> = numbers.clone();
            new_numbers.remove(i);
            if check_numbers(new_numbers){
                line_ok = true;
                break;
            }
        }
        if line_ok{
            result += 1;
        }
    });

    println!("Day 02, Parte 2: {result}");

}

pub fn start(input: &str){
    let _test_input: &str = "7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9";

    _part_1(input);
    _part_2(input);
}