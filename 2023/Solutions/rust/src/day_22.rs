use ahash::AHashMap as HashMap;
use ahash::AHashSet as HashSet;
use std::collections::VecDeque;
use std::time::Instant;

#[derive(Debug, Copy, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
struct Coord {
    z: usize,
    x: usize,
    y: usize,
}

// I'm doing a bunch of nested for-loops, so... just make an iterator for it.
impl Coord {
    fn iter_to(&self, to: &Self) -> Box<dyn Iterator<Item = Self>> {
        use std::iter::repeat;
        let (from, to) = if self > to {
            (*to, *self)
        } else {
            (*self, *to)
        };
        Box::new(
            (from.z..=to.z)
                .flat_map(move |z| {
                    repeat(z).zip((from.x..=to.x).flat_map(move |x| repeat(x).zip(from.y..=to.y)))
                })
                .map(|(z, (x, y))| Self { z, x, y }),
        )
    }
}

type BrickId = usize;

#[derive(Debug, Copy, Clone)]
struct Brick {
    id: BrickId,
    from: Coord,
    to: Coord,
}

impl Brick {
    fn iter_cubes(&self) -> Box<dyn Iterator<Item = Coord>> {
        self.from.iter_to(&self.to)
    }
}

type EdgeMap = HashMap<BrickId, HashSet<BrickId>>;

fn parse_line(line: &str, id: usize) -> Brick {
    let (from, to) = line.split_once('~').unwrap();
    let [from_x, from_y, from_z] = from
        .split(',')
        .map(|d| d.parse::<usize>().unwrap())
        .collect::<Vec<_>>()
        .try_into()
        .unwrap();

    let [to_x, to_y, to_z] = to
        .split(',')
        .map(|d| d.parse::<usize>().unwrap())
        .collect::<Vec<_>>()
        .try_into()
        .unwrap();
    
    let mut from = Coord {
        z: from_z,
        x: from_x,
        y: from_y,
    };
    let mut to = Coord {
        z: to_z,
        x: to_x,
        y: to_y,
    };
    // I expect at least one brick to be set up backwards.
    if from > to {
        std::mem::swap(&mut from, &mut to);
    }
    Brick { id, from, to }
}

fn parse(input: &str) -> Vec<Brick> {
    input
        .lines()
        .enumerate()
        .map(|(id, line)| parse_line(line, id))
        .collect()
}

fn process_input(input: &str) -> (Vec<Brick>, EdgeMap, EdgeMap) {
    let mut bricks = parse(input);
    // Coord has z first, so this'll sort by Z, then X, then Y.
    bricks.sort_by_key(|b| b.from);
    let mut grid: HashMap<Coord, BrickId> = HashMap::new();
    // brick B supports all of these bricks
    let mut supports: EdgeMap = HashMap::with_capacity(bricks.len());
    // All of these bricks support brick B
    let mut supported_by: EdgeMap = HashMap::with_capacity(bricks.len());
    for brick in bricks.iter_mut() {
        supports.insert(brick.id, HashSet::new());
        supported_by.insert(brick.id, HashSet::new());
        let mut bottom = 1;
        for z in (1..brick.from.z).rev() {
            for id in brick
                .iter_cubes()
                .map(|Coord { x, y, .. }| Coord { z, x, y })
                .filter_map(|c| grid.get(&c))
            {
                supported_by.entry(brick.id).or_default().insert(*id);
                supports.entry(*id).or_default().insert(brick.id);
            }
            // If we found any bricks below this one, then we've found the spot to settle at.
            if supported_by.get(&brick.id).is_some_and(|e| !e.is_empty()) {
                bottom = z + 1;
                break;
            }
        }
        brick.to.z -= brick.from.z - bottom;
        brick.from.z = bottom;
        brick.iter_cubes().fold(&mut grid, |g, c| {
            g.insert(c, brick.id);
            g
        });
    }
    (bricks, supports, supported_by)
}

fn part1(input: &str) -> usize {
    let (bricks, supports, supported_by) = process_input(input);
    // If all the bricks that are supported by brick B are also supported by at least one other
    // brick, then brick B is safe to disintegrate.
    bricks
        .iter()
        .filter(|brick| {
            supports[&brick.id]
                .iter()
                .all(|b| supported_by[b].len() > 1)
        })
        .count()
}

// Part 2 is the inverse(?) of part 1: which bricks are the least safe to disintegrate?
// We can use the answer from part 1: none of the safe bricks need to be checked, because they'll
// never cause a chain reaction. That cuts out ~1/3 of the bricks.
fn part2(input: &str) -> usize {
    let (bricks, supports, supported_by) = process_input(input);
    let skips: HashSet<BrickId> = HashSet::from_iter(
        bricks
            .iter()
            .filter(|brick| {
                supports[&brick.id]
                    .iter()
                    .all(|b| supported_by[b].len() > 1)
            })
            .map(|b| b.id),
    );
    let mut all_cuts = vec![];
    for brick in bricks.iter().filter(|b| !skips.contains(&b.id)) {
        let mut cuts = HashSet::new();
        cuts.insert(brick.id);
        let mut q: VecDeque<&BrickId> = VecDeque::from_iter(
            supports[&brick.id]
                .iter()
                .filter(|b| supported_by[b].len() == 1),
        );
        // extend the queue by all the nodes that have all their supports in the cut.
        while let Some(bid) = q.pop_front() {
            cuts.insert(*bid);
            for sup_brick in supports[bid].iter() {
                if cuts.is_superset(&supported_by[&sup_brick]) {
                    cuts.insert(*sup_brick);
                    q.push_back(sup_brick);
                }
            }
        }
        all_cuts.push(cuts);
    }
    // each cut includes the start node, so we have to remove those from the final count.
    all_cuts.iter().map(|c| c.len() - 1).sum()
}

#[allow(dead_code)]
const TEST: &str = "1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9";

const INPUT: &str = include_str!("C:/Users/raikoug/SyncThing/shared_code_tests/adventOfCode/2023/day_22/input.txt");

fn solve(input: Vec<String>) {
    let start = Instant::now();
    let p1 = part1(INPUT);
    let duration = start.elapsed();
    println!("Part 1: {} ({:?})", p1, duration);

    let start = Instant::now();
    let p2 = part2(INPUT);
    let duration = start.elapsed();
    println!("Part 2: {} ({:?})", p2, duration);
}