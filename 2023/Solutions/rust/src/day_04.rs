use std::collections::HashMap;



pub fn start(input: Vec<String>) {
    // PART 1 & 2
    
    // for part 2 init a hasmap that will contain data like this:
    // {1 : int, 2: int, 3: int, 4: int, 5: int, 6: int, 7: int, 8: int, 9: int... }
    let mut part_2_cards: HashMap<u32, u32> = HashMap::new();
    let mut part_2_res: u32 = 0;

    let part_1_res : u32 = input
    .iter().map(|row| {
        // each contins 3 parts part1:part2|part3
        // 1. card number 'Card X'
        // 2 .the winning numbers 'a b c d .. '
        // 3. the game number 'a b c d e ... '

        let mut row_split = row.split(":");
        // first part of this now is 'Card 1', 'Card 2' ... 'Card 10'
        //  get 1, 2 3..
        let card_number: u32 = row_split.next().unwrap().split(" ").nth(1).unwrap().parse().unwrap();
        // if card number is not in the part_2_cards hashmap, insert it with value 1
        let number_of_cards: u32 = *part_2_cards.entry(card_number).or_insert(1);
        
        
        // second part is the winning numbers|game numbers
        let mut game_numbers = row_split.next().unwrap().split("|");
        // winning numbers
        let winning_numbers: Vec<u32> = game_numbers.next().unwrap().trim()
            .split_whitespace().map(|n| {
                n.parse().unwrap()
        }).collect();
        // game numbers
        let result: u32 = game_numbers.next().unwrap().trim()
            .split_whitespace().map(|n| {
                let value: u32 = n.parse().unwrap();
                if winning_numbers.contains(&value) {
                    1
                } else {
                    0
                }

        }).sum();
        // for part 2, if result i 4, add 1 to the card numbers card_number+1, +2, +3, +4]
        // if result is 3, add 1 to card_number+1, +2, +3
        for i in 1..=result {
            let card_number = card_number + i;
            let tmp_num = part_2_cards.entry(card_number).or_insert(1);
            *tmp_num += 1;
            // TODO check if this works
        }


        // for part 2 multiply number_of_cards with result
        part_2_res += number_of_cards * result;
        print!("card_number: {}, result: {}, ", card_number, result);
        let card_value : u32 = if result > 0 {2_u32.pow(result - 1)} else {0};	
        println!("card_value: {}", card_value);
        card_value
    }).sum();


    println!("part 1: {}", part_1_res);
    println!("part 2: {}", part_2_res);
}


pub fn solve(input: Vec<String>) {

    start(input.clone());

    // PART 2
    //println!("part 2: {}", part_2(input));

}