use regex::Regex;
use lazy_static::lazy_static;

pub fn part2(input: Vec<String>) -> u32 {
    const DIGIT_NAMES: [(&[u8], u32); 9] = [
        (b"one", 1),
        (b"two", 2),
        (b"three", 3),
        (b"four", 4),
        (b"five", 5),
        (b"six", 6),
        (b"seven", 7),
        (b"eight", 8),
        (b"nine", 9),
    ];

    fn find_digit<T>(mut f: impl FnMut(&[u8], u32) -> Option<T>) -> Option<T> {
        DIGIT_NAMES.into_iter().find_map(|(d, n)| f(d, n))
    }

    input
        .iter()
        .map(|line| {
            let line = line.as_bytes();

            let (rest, lhs) = std::iter::successors(Some(line), |line| Some(line.split_first()?.1))
                .find_map(|line| match line.first() {
                    Some(&b @ b'1'..=b'9') => Some((&line[1..], (b - b'0') as u32)),
                    _ => find_digit(|d, n| line.strip_prefix(d).map(|rest| (rest, n))),
                })
                .unwrap();

            let rhs = std::iter::successors(Some(rest), |line| Some(line.split_last()?.1))
                .find_map(|line| match line.last() {
                    Some(&b @ b'1'..=b'9') => Some((b - b'0') as u32),
                    _ => find_digit(|d, n| line.ends_with(d).then(|| n)),
                })
                .unwrap_or(lhs);

            lhs * 10 + rhs
        })
        .sum()
}

fn part_1(input: Vec<String>) -> u32{
    lazy_static! {
        static ref RE: Regex = Regex::new(r"\d").unwrap();
    }
    input
        .iter()
        .map(|line| {
            let ns : Vec<i64> = RE.find_iter(line)
                // try to parse the string matches as i64 (inferred from fn type signature)
                // and filter out the matches that can't be parsed (e.g. if there are too many digits to store in an i64).
                .filter_map(|digits| digits.as_str().parse().ok())
                // collect the results in to a Vec<i64> (inferred from fn type signature)
                .collect();
            let first: char = ns.first().unwrap().to_string().chars().next().unwrap();
            let last: char = ns.last().unwrap().to_string().chars().next().unwrap();
            let merged: u32 = format!("{}{}", first, last).parse().unwrap();
            merged * 1
            }
        )
        .sum()
}


pub fn solve(input: Vec<String>) {
    // PART 1
    println!("part 1: {}", part_1(input.clone()));

    // PART 2
    println!("part 2: {}", part2(input));

}