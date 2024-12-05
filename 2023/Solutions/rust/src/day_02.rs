use std::collections::HashMap;


pub fn start(input: Vec<String>, cards: HashMap<&'static str, i32>) {
    let mut part_2_res : u32 = 0;
    let part_1_res: u32 = input
      .iter()
        .map(|line| {
            // each line is in the forma
            // Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
            // take game number and treat the string after : as a new input.

            // part 2 tmp cards
            let mut tmp_card: HashMap<&str, i32> = HashMap::new();
            tmp_card.insert("red", 0);
            tmp_card.insert("green", 0);
            tmp_card.insert("blue", 0);

            
            // split line with character ":"
            let mut line_split = line.split(":");
            // the first element is now "Game X:", get X as u32
            let game_number: u32 = line_split.next().unwrap().split(" ").nth(1).unwrap().parse().unwrap();

            // second element is a list of games separated by ";",. loop through them returning a u32
            // if all the games are valid return 1 else 0.
            let moltipl: u32 = line_split.next().unwrap().split(";")
              .into_iter()
                .map(|game|{
                    // game now is list ho hands separated by ","
                    //     hands must be matched with variable 'cards'
                   
                    let res: u32 = game.split(",").into_iter()
                     .map(|hand|{
                           // if hand has a color with a value higher than cards[color] return 0
                           // else return 1, problem is that some hand starts witha a space
                           // need to clean it
                            let hand = hand.trim();
                            let color = hand.split(" ").nth(1).unwrap();
                            let value = hand.split(" ").nth(0).unwrap().parse::<i32>().unwrap();

                            let current_tmp_value = tmp_card.entry(color).or_insert(0);
                            if value > *current_tmp_value {
                                *current_tmp_value = value;
                            }

                            if value > *cards.get(color).unwrap() {
                                return 0
                            }

                           1

                     }).product();
                    return res;
                    
                }).product();
            
            // for part 2 multiply each card value with each other and then add to part_2_res
            part_2_res += tmp_card.values().product::<i32>() as u32;
            return game_number*moltipl;

        })
        .sum();
    println!("part 1: {}", part_1_res);
    println!("part 2: {}", part_2_res);
}
//pub fn part_2(input: Vec<String>) -> u32 {
//    input.iter()
//    .map(|line| {
//        // each line is in the forma
//        // Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
//        // take game number and treat the string after : as a new input.
//        
//        // split line with character ":"
//        let mut line_split = line.split(":");
//        // the first element is now "Game X:", get X as u32
//        //let game_number: u32 = line_split.next().unwrap().split(" ").nth(1).unwrap().parse().unwrap();
//
//        // second element is a list of games separated by ";",. loop through them making 
//        // starting with red = 0, green = 0, blue = 0, looping through games, get the higher
//        // value for each color.
//        // with this game: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
//        // result whould be red = 4, green = 2, blue = 6
//
//        // init cards value hasmap to 0
//        let mut cards: HashMap<&str, i32> = HashMap::new();
//        cards.insert("red", 0);
//        cards.insert("green", 0);
//        cards.insert("blue", 0);
//
//        
//        line_split.next().unwrap().split(";")
//          .into_iter()
//            .for_each(|game|{
//                // we have now single games with hands separated by ","
//                //     3 blue, 4 red
//                
//                game.split(",").into_iter()
//                 .for_each(|hand|{
//                       // now we have single hands
//                       // '3 blue' or ' 4 redd'
//                       // trim the spaces
//                        let hand = hand.trim();
//                        let color = hand.split(" ").nth(1).unwrap();
//                        let value = hand.split(" ").nth(0).unwrap().parse::<i32>().unwrap();
//                        
//                        let current_value = cards.entry(color).or_insert(0);
//                        //println!("{}-{}", value,color);
//                        if value > *current_value {
//                            *current_value = value;
//                        }
//                 });
//            });
//        println!("{:?}", cards);
//        1
//
//
//    }).sum()
//}


pub fn solve(input: Vec<String>) {

    let mut cards: HashMap<&str, i32> = HashMap::new();
    cards.insert("red", 12);
    cards.insert("green", 13);
    cards.insert("blue", 14);
    
    
    // PART 1
    start(input.clone(), cards);

    // PART 2
    //println!("part 2: {}", part_2(input));

}