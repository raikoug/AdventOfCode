use ndarray::Array2;
use ndarray::s;
use regex::Regex;

const GRID_SIZE: usize = 1000;

#[derive(Debug)]
enum Action {
    TurnOn,
    TurnOff,
    Toggle,
}

#[derive(Debug)]
struct Instruction {
    action: Action,
    x1: usize,
    y1: usize,
    x2: usize,
    y2: usize,
}

impl Instruction {
    // Metodo per creare un'istruzione da una stringa
    // toggle x1,y1 through x2,y2
    // turn off x1,y1 through x2,y2
    // turn on x1,y1 through x2,y2

    fn from_str(s: &str) -> Option<Self> {
        //let re = Regex::new(r"(.*) (\d*),(\d*) through (\d*),(\d*)").unwrap();
        let re = Regex::new(
            r"(?x)
            (?P<action>turn\ on|turn\ off|toggle)    # Azione
            \s+
            (?P<x1>\d+),(?P<y1>\d+)               # Coordinate iniziali
            \s+through\s+
            (?P<x2>\d+),(?P<y2>\d+)               # Coordinate finali
            ",
        ).unwrap();
        
        // Applichiamo la regex alla stringa di input
        if let Some(caps) = re.captures(s) {
            // Parsiamo l'azione
            let action_str = &caps["action"];
            let action = match action_str {
                "turn on" => Action::TurnOn,
                "turn off" => Action::TurnOff,
                "toggle" => Action::Toggle,
                _ => return None,
            };

            // Parsiamo le coordinate
            let x1 = caps["x1"].parse::<usize>().ok()?;
            let y1 = caps["y1"].parse::<usize>().ok()?;
            let x2 = caps["x2"].parse::<usize>().ok()?;
            let y2 = caps["y2"].parse::<usize>().ok()?;

            Some(Instruction { action, x1, y1, x2, y2 })
        } else {
            println!("Fallito con {s}");
            None
        }
    }
}


fn change_lights(
    grid: &mut Array2<u16>,
    i: Instruction,
    v2: bool
) {
    
    let mut subgrid = grid.slice_mut(s![i.x1..=i.x2, i.y1..=i.y2]);

    subgrid.map_inplace(|elem| {
        match i.action {
            Action::TurnOn => {
                if !v2 {
                    *elem = 1;
                } else {
                    *elem += 1;
                }
            }
            Action::TurnOff => {
                if !v2 {
                    *elem = 0;
                } else {
                    if *elem > 0 {
                        *elem -= 1;
                    }
                }
            }
            Action::Toggle => {
                if !v2 {
                    *elem = if *elem == 0 { 1 } else { 0 };
                } else {
                    *elem += 2;
                }
            }
        }
    });
    
}

fn count_lights(grid: &mut Array2<u16>,){
    let mut result: u64 = 0;
    grid.map_inplace(|el: &mut u16|{
        result += u64::from(*el);
    });
    println!("{result}");
}

pub fn part_1(input: &str) {
    let mut grid: ndarray::ArrayBase<ndarray::OwnedRepr<u16>, ndarray::Dim<[usize; 2]>> = Array2::<u16>::from_elem((GRID_SIZE, GRID_SIZE), 0);
    // let test_row: &str  = "toggle 461,550 through 564,900";
    // let i =Instruction::from_str(test_row);

    input.lines().for_each(|riga| {
        if let Some(instruction) = Instruction::from_str(riga){
            change_lights(&mut grid, instruction, false)
    } else {
        println!("Errore nel parsing dell'istruzione: {}", riga);
    }
    });

    count_lights(&mut grid);
}

pub fn part_2(input: &str) {
    let mut grid: ndarray::ArrayBase<ndarray::OwnedRepr<u16>, ndarray::Dim<[usize; 2]>> = Array2::<u16>::from_elem((GRID_SIZE, GRID_SIZE), 0);
    // let test_row: &str  = "toggle 461,550 through 564,900";
    // let i =Instruction::from_str(test_row);

    input.lines().for_each(|riga| {
        if let Some(instruction) = Instruction::from_str(riga){
            change_lights(&mut grid, instruction, true)
    } else {
        println!("Errore nel parsing dell'istruzione: {}", riga);
    }
    });

    count_lights(&mut grid);
    
}
