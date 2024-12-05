use std::collections::HashMap;


pub fn part_1(mappings : (Vec<i64>,HashMap<String, Mapping>)) -> i64 {
    let (seeds, maps) = mappings;
    
    // test the first seed with the first mapping, that is the 'seed' mapping
    seeds.iter().map(|s| {
        // println!("seed: {}", s);
        let mut current_mapping = "seed".to_string();
        let mut result: i64 = *s;

        while current_mapping != "location"{
            let map = maps.get(&current_mapping).unwrap();
            result = map.map_value(result);
            current_mapping = map.destination.clone();

        }
        result
    }).min().unwrap()
    
}
pub fn part_2() -> u32 {
    2
}

pub struct MyRange {
    origin: i64,
    destination: i64,
    span: i64,
}

impl MyRange {
    pub fn new(destination: i64, origin: i64, span: i64) -> MyRange {
        MyRange { destination, origin, span }
    }

    pub fn is_in_range(&self, value: i64) -> bool {
        // check if value is in range
        value >= self.origin as i64 && value <= (self.origin + self.span) as i64
    }

    pub fn to_string(&self) -> String {
        format!("o:{} d:{} s:{}", self.origin, self.destination, self.span)
    }
}

pub struct Mapping {
    origin: String,
    destination: String,
    ranges: Vec<MyRange>,
}

impl Mapping {
    pub fn new(line: &str) -> Mapping {
        let mapping = line.split_whitespace().next().unwrap();
        let parts: Vec<&str> = mapping.split("-").collect();
        let origin = parts[0].to_string();
        let destination = parts[2].to_string();
        Mapping { origin, destination, ranges: Vec::new() }
    }

    pub fn add_range(&mut self, r: &str) {
        let parts: Vec<i64> = r.split_whitespace().map(|s| s.parse().unwrap()).collect();
        self.ranges.push(MyRange::new(parts[0], parts[1], parts[2]));
    }

    pub fn to_string(&self) -> String {
        let mut res = format!("{} to {}\n", self.origin, self.destination);
        for r in &self.ranges {
            res += &format!("\t└─{}\n", r.to_string());
        }
        res
    }

    pub fn map_value(&self, value: i64) -> i64 {
        // checkl all ranges, if value is in range one of these ranges:
        //    the range can be: origin - destination - span
        //       final value will be: destination + (value - origin)
        // if no range match the value, return value
        for r in &self.ranges {
            if r.is_in_range(value) {
                //println!("   {} is in range {}", value, r.to_string());
                return r.destination + (value - r.origin);
            }
        }
        value
    }
}

pub fn part_1_seeds(input: String) -> Vec<i64> {
    // input is a String like: 'seeds: a b c d'
    //   remove 'seeds: ' and split on whitespace
    let numbers: Vec<i64> = input[7..].split_whitespace()
    .map(|s| {
        s.parse().unwrap()
        }).collect();
        numbers
}

pub fn part_2_seeds(input: String) -> Vec<i64>{
    // input is a String like: 'seeds: a b c d'
    //   remove 'seeds: ' and split on whitespace
    
    
    // no

    Vec::new()
}

//pub fn part_2_mapping(input: Vec<String>) -> (Vec<i64>,HashMap<String, Mapping>) {
//    1
//}

pub fn print_mappings(mappings: &HashMap<String, Mapping>) {
    for (k, v) in mappings {
        println!("{}: {}", k, v.to_string());
    }
}

pub fn part_1_mapping(input: Vec<String>) -> (Vec<i64>,HashMap<String, Mapping>) {
    // first line of input are the seeds, send the first line to part_1_seeds
    let seeds: Vec<i64> = part_1_seeds(input.first().unwrap().to_string());
    let mut mappings: HashMap<String, Mapping> = HashMap::new();
    let mut label = String::new();

    for line in input[2..].iter() {
        // if line is empy, pass
        if line.is_empty() {
            continue;
        }
        // if line starts with a letter, sent line init a new Mapping
        if line.chars().next().unwrap().is_alphabetic() {
            let m = Mapping::new(line);
            label = m.origin.clone();
            mappings.insert(label.clone(), m);
        } else {
            // else, add the line to the last Mapping
            if let Some(m) = mappings.get_mut(&label) {
                m.add_range(line);
            }
     }
    }
    //print_mappings(&mappings);
    (seeds, mappings)
}

pub fn solve(input: Vec<String>) {
    
    let mappings: (Vec<i64>,HashMap<String, Mapping>) = part_1_mapping(input.clone());

    // PART 1
    println!("part 1: {}", part_1(mappings));

    // PART 2
    println!("part 2: {}", part_2());

}