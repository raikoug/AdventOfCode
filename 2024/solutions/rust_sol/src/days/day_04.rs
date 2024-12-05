
pub fn _part_1(_input: &str) {
    let input_lines: Vec<&str> = _input.trim().lines().collect();
    let n = input_lines.len();
    let m = input_lines[0].len();
    let word = "XMAS";
    let word_len = word.len();
    let chars: Vec<Vec<char>> = input_lines.iter().map(|l| l.chars().collect()).collect();

    let mut count = 0;

    // Check horizontally and horizontally reversed
    for row in 0..n {
        for col in 0..=m-word_len {
            // Check left to right
            if &chars[row][col..col + word_len] == word.chars().collect::<Vec<char>>() {
                count += 1;
            }
            // Check right to left
            if &chars[row][col..col + word_len] == word.chars().rev().collect::<Vec<char>>() {
                count += 1;
            }
        }
    }

    // Check vertically and vertically reversed
    for col in 0..m {
        for row in 0..=n-word_len {
            // Check top to bottom
            if (0..word_len).all(|i| chars[row + i][col] == word.chars().nth(i).unwrap()) {
                count += 1;
            }
            // Check bottom to top
            if (0..word_len).all(|i| chars[row + i][col] == word.chars().rev().nth(i).unwrap()) {
                count += 1;
            }
        }
    }

    // Check diagonally (top-left to bottom-right and bottom-right to top-left)
    for row in 0..=n-word_len {
        for col in 0..=m-word_len {
            // Check top-left to bottom-right
            if (0..word_len).all(|i| chars[row + i][col + i] == word.chars().nth(i).unwrap()) {
                count += 1;
            }
            // Check bottom-right to top-left
            if (0..word_len).all(|i| chars[row + i][col + i] == word.chars().rev().nth(i).unwrap()) {
                count += 1;
            }
        }
    }

    // Check diagonally (top-right to bottom-left and bottom-left to top-right)
    for row in 0..=n-word_len {
        for col in word_len-1..m {
            // Check top-right to bottom-left
            if (0..word_len).all(|i| chars[row + i][col - i] == word.chars().nth(i).unwrap()) {
                count += 1;
            }
            // Check bottom-left to top-right
            if (0..word_len).all(|i| chars[row + i][col - i] == word.chars().rev().nth(i).unwrap()) {
                count += 1;
            }
        }
    }

    println!("Day 4, Part 1: {}", count);
}
pub fn _part_2(_input: &str) {
    let grid: Vec<&str> = _input.lines().collect();
    let rows = grid.len();
    let cols = grid[0].len();
    
    let mut count = 0;
    
    for row in 0..rows {
        for col in 0..cols {
            if grid[row].as_bytes()[col] == b'A' {
                // Check the 4 pattern with try to avoid index out of range
                if row >= 1 && col >= 1 && row + 1 < rows && col + 1 < cols {
                    let one = grid[row - 1].as_bytes()[col - 1];
                    let two = grid[row - 1].as_bytes()[col + 1];
                    let four = grid[row + 1].as_bytes()[col - 1];
                    let five = grid[row + 1].as_bytes()[col + 1];
                
                    if (one == b'M' && two == b'M' && four == b'S' && five == b'S') ||
                       (one == b'S' && two == b'M' && four == b'S' && five == b'M') ||
                       (one == b'S' && two == b'S' && four == b'M' && five == b'M') ||
                       (one == b'M' && two == b'S' && four == b'M' && five == b'S') {
                        count += 1;
                    }
                }
            }
        }
    }

    println!("Day 04, Parte 2: {}", count);

}

pub fn start(input: &str){
    _part_1(input);
    _part_2(input);
}