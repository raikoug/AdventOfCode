
pub fn next_coords(point: (usize,usize), direction: &char) -> (usize,usize){
    let mut new_point: (usize, usize) = point.clone();
    if *direction == '^' {
        new_point.0 -= 1;
    }
    else if *direction ==  '>' {
        new_point.1 += 1;
    }
    else if *direction ==  'v' {
        new_point.0 += 1;
    }
    else if *direction ==  '<' {
        new_point.1 -= 1;
    }
    new_point
}

pub fn next_direction(direction: &char) -> char {
    if *direction == '^' {
        '>'
    }
    else if *direction ==  '>' {
        'v'
    }
    else if *direction ==  'v' {
        '<'
    }
    else if *direction ==  '<' {
        '^'
    }
    else{
        '.'
    }
}

pub fn check_coords(grid: &Vec<Vec<char>>, point: &(usize, usize)) -> bool {
    let (x, y) = point;
    if *x < grid.len() && *y < grid[0].len(){
        true
    } else {
        false
    }
}


pub fn _part_1(_input: &str) {
    let lines = _input.lines();
    let mut old_posititon: (usize, usize) = (0, 0);
    let mut visited : Vec<(usize, usize)> = Vec::new();
    let grid: Vec<Vec<char>> = lines.enumerate().map(|something: (usize, &str)|{
        let row : usize = something.0;
        something.1.chars().enumerate().map(|another_something| {
            let col: usize = another_something.0;
            let ch: char = another_something.1;
            if ch == '^' {
                old_posititon = (row,col);
                '.'
            }
            else {
                ch
            }

          }).collect()
        }).collect();
    
    visited.push(old_posititon);
    let mut direction : char = '^';
    let mut next_position: (usize,usize) = next_coords(old_posititon, &direction);

    
    while check_coords(&grid, &next_position){
        // coord are ok and it's safe to get the grid tyle:
        let tyle: char = grid[next_position.0][next_position.1];
        if tyle == '#' {
            // canmt step in wall, change direction and calculate again from old position!
            direction = next_direction(&direction);
            next_position = next_coords(old_posititon, &direction);
        }
        else{
            if !visited.contains(&next_position){
                visited.push(next_position);
            }
            old_posititon = next_position;
            next_position = next_coords(next_position, &direction);
        }
    }
    println!("Day 6, Parte 1: {}", visited.len());
}

pub fn check_is_loop(grid: Vec<Vec<char>>) -> bool{
    let mut old_posititon: (usize, usize) = (0, 0);
    let mut visited : Vec<(usize, usize)> = Vec::new();
    let mut movements: Vec<(usize,usize,char)> = Vec::new();
    visited.push(old_posititon);
    let mut direction : char = '^';
    let movement: (usize,usize,char) = (old_posititon.0,old_posititon.1,direction);
    movements.push(movement);
    let mut next_position: (usize,usize) = next_coords(old_posititon, &direction);

    
    while check_coords(&grid, &next_position){
        // coord are ok and it's safe to get the grid tyle:
        let tyle: char = grid[next_position.0][next_position.1];
        if tyle == '#' {
            // canmt step in wall, change direction and calculate again from old position!
            direction = next_direction(&direction);
            next_position = next_coords(old_posititon, &direction);
        }
        else{
            if !visited.contains(&next_position){
                visited.push(next_position);
            }
            let movement: (usize, usize, char) = (next_position.0,next_position.1,direction);
            if !movements.contains(&movement){
                movements.push(movement);
            }
            else{
                // this is a loop!!!
                return true
            }
            old_posititon = next_position;
            next_position = next_coords(next_position, &direction);
        }
    }

    false
    
}

pub fn _part_2(_input: &str) {
    let lines = _input.lines();
    let mut old_posititon: (usize, usize) = (0, 0);
    let mut visited : Vec<(usize, usize)> = Vec::new();
    let grid: Vec<Vec<char>> = lines.enumerate().map(|something: (usize, &str)|{
        let row : usize = something.0;
        something.1.chars().enumerate().map(|another_something| {
            let col: usize = another_something.0;
            let ch: char = another_something.1;
            if ch == '^' {
                old_posititon = (row,col);
                '.'
            }
            else {
                ch
            }

          }).collect()
        }).collect();
    
    let result: bool = check_is_loop(grid);
    println!("{result}");

    // visited.push(old_posititon);
    // let mut direction : char = '^';
    // let mut next_position: (usize,usize) = next_coords(old_posititon, &direction);

    
    // while check_coords(&grid, &next_position){
    //     // coord are ok and it's safe to get the grid tyle:
    //     let tyle: char = grid[next_position.0][next_position.1];
    //     if tyle == '#' {
    //         // canmt step in wall, change direction and calculate again from old position!
    //         direction = next_direction(&direction);
    //         next_position = next_coords(old_posititon, &direction);
    //     }
    //     else{
    //         if !visited.contains(&next_position){
    //             visited.push(next_position);
    //         }
            
    //         old_posititon = next_position;
    //         next_position = next_coords(next_position, &direction);
    //     }
    // }
    // println!("{}")
    // println!("Day 6, Parte 1: {}", visited.len());

}

pub fn start(input: &str){
    let _test_input: &str = "....#.....\n.........#\n..........\n..#.......\n.......#..\n..........\n.#..^.....\n........#.\n#.........\n......#...";
    let _test_input_loop: &str = "....#.....\n.........#\n..........\n..#.......\n.......#..\n..........\n.#.#^.....\n........#.\n#.........\n......#...";
    _part_1(input);
    _part_2(_test_input_loop);
}