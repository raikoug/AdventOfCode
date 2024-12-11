use std::collections::HashMap;


pub fn _part_1(input: &str) {
    // Helper functions

    // Check if a number has an even number of digits
    fn stone_have_even_digits(x: i64) -> bool {
        let s = x.to_string();
        s.len() % 2 == 0
    }

    // Split a number with even number of digits into two halves
    fn split_string_by_half(stone: i64) -> Vec<i64> {
        let s = stone.to_string();
        let l = s.len();
        let h = l / 2;
        let left = &s[..h];
        let right = &s[h..];
        // Convert halves back to integers; leading zeros will naturally be dropped by parsing
        let left_num = left.parse::<i64>().unwrap();
        let right_num = right.parse::<i64>().unwrap();
        vec![left_num, right_num]
    }

    // Transform a single stone according to the given rules
    fn parse_stone(stone: i64) -> Vec<i64> {
        if stone == 0 {
            vec![1]
        } else if stone_have_even_digits(stone) {
            split_string_by_half(stone)
        } else {
            vec![stone * 2024]
        }
    }

    // Parse the input string into a vector of stones
    let mut stones: Vec<i64> = input
        .split_whitespace()
        .filter_map(|s| s.parse::<i64>().ok())
        .collect();

    // We need to blink 75 times
    let part_2_blinks = 75;

    for _ in 0..part_2_blinks {
        let mut new_stones = Vec::new();
        for stone in &stones {
            let transformed = parse_stone(*stone);
            new_stones.extend(transformed);
        }
        stones = new_stones;
    }

    println!("Day N, Parte 2: {}", stones.len());
}


fn split_string_by_half(stone: u32) -> Vec<u32> {
    let s = stone.to_string();
    let h = s.len() / 2;
    let left = s[..h].parse::<u32>().unwrap();
    let right = s[h..].parse::<u32>().unwrap();
    vec![left, right]
}

fn stone_have_even_digits(stone: u32) -> bool {
    stone.to_string().len() % 2 == 0
}

fn parse_stone(stone: u32, cache: &mut HashMap<u32, Vec<u32>>) -> Vec<u32> {
    if let Some(result) = cache.get(&stone) {
        return result.clone();
    }
    let result = if stone == 0 {
        vec![1]
    } else if stone_have_even_digits(stone) {
        split_string_by_half(stone)
    } else {
        match stone.checked_mul(2024) {
            Some(new_stone) => vec![new_stone],
            None => vec![stone], // Handle overflow by keeping the original stone
        }
    };
    cache.insert(stone, result.clone());
    result
}

const PART_2_BLINKS: u32 = 75;

pub fn _part_2(input: &str) {
    let mut stones: Vec<u32> = input.split_whitespace().map(|el| el.parse::<u32>().unwrap()).collect();
    let mut blinks = 0;
    let mut cache = HashMap::new();

    while blinks < PART_2_BLINKS {
        let mut new_stones = Vec::new();
        for &stone in &stones {
            new_stones.extend(parse_stone(stone, &mut cache));
        }
        blinks += 1;
        stones = new_stones;
        println!("Blinks: {: >3}", blinks);
    }

    
    println!("Day N, Parte 2: {:?}", stones.len());

}

pub fn start(input: &str){
    _part_1(input);
    _part_2(input);
}