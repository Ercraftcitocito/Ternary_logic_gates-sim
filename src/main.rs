use std::io::{self, Write};
use ternary_logic_sim::{Circuit, GateType, TernaryValue};

fn main() {
    println!("\n╔════════════════════════════════════════╗");
    println!("║  Ternary Logic Gate Simulator (CLI)   ║");
    println!("║  Values: -1, 0, 1                     ║");
    println!("╚════════════════════════════════════════╝\n");

    let mut circuit = Circuit::new();
    let mut running = true;

    while running {
        print_menu();
        let mut choice = String::new();
        io::stdin().read_line(&mut choice).unwrap();

        match choice.trim() {
            "1" => add_gate(&mut circuit),
            "2" => simulate(&mut circuit),
            "3" => print_circuit(&circuit),
            "4" => {
                circuit = Circuit::new();
                println!("✓ Circuit cleared");
            }
            "5" => {
                running = false;
                println!("\nGoodbye!");
            }
            _ => println!("Invalid option, try again."),
        }
    }
}

fn print_menu() {
    println!("\n┌─ Options ────────────────────┐");
    println!("│ 1) Add gate                   │");
    println!("│ 2) Simulate                   │");
    println!("│ 3) View circuit               │");
    println!("│ 4) Clear circuit              │");
    println!("│ 5) Exit                       │");
    println!("└──────────────────────────────┘");
    print!("> ");
    io::stdout().flush().unwrap();
}

fn add_gate(circuit: &mut Circuit) {
    println!("\n┌─ Gate Types ─────────────────┐");
    println!("│ 1) AND  (min)                 │");
    println!("│ 2) OR   (max)                 │");
    println!("│ 3) XOR  (sum mod 3)           │");
    println!("│ 4) NOT  (negate)              │");
    println!("│ 5) MIN  (minimum)             │");
    println!("│ 6) MAX  (maximum)             │");
    println!("└──────────────────────────────┘");
    print!("Select gate type: ");
    io::stdout().flush().unwrap();

    let mut choice = String::new();
    io::stdin().read_line(&mut choice).unwrap();

    let gate_type = match choice.trim() {
        "1" => GateType::And,
        "2" => GateType::Or,
        "3" => GateType::Xor,
        "4" => GateType::Not,
        "5" => GateType::Min,
        "6" => GateType::Max,
        _ => {
            println!("Invalid gate type");
            return;
        }
    };

    let id = circuit.add_gate(gate_type, vec![]);
    circuit.set_output(id);
    println!("✓ Added {} gate (ID: {})", gate_type.as_str(), id);
}

fn simulate(circuit: &mut Circuit) {
    println!("\n┌─ Input Values ────────────────┐");
    println!("│ Enter values: -1, 0, or 1    │");
    println!("└──────────────────────────────┘");

    print!("Input A (-1/0/1): ");
    io::stdout().flush().unwrap();
    let mut a_str = String::new();
    io::stdin().read_line(&mut a_str).unwrap();
    let a = a_str.trim().parse::<i32>().unwrap_or(0);

    print!("Input B (-1/0/1): ");
    io::stdout().flush().unwrap();
    let mut b_str = String::new();
    io::stdin().read_line(&mut b_str).unwrap();
    let b = b_str.trim().parse::<i32>().unwrap_or(0);

    print!("Input C (-1/0/1): ");
    io::stdout().flush().unwrap();
    let mut c_str = String::new();
    io::stdin().read_line(&mut c_str).unwrap();
    let c = c_str.trim().parse::<i32>().unwrap_or(0);

    circuit.set_inputs(vec![
        TernaryValue::from_i32(a),
        TernaryValue::from_i32(b),
        TernaryValue::from_i32(c),
    ]);

    let outputs = circuit.evaluate();

    println!("\n┌─ Results ──────────────────────┐");
    println!("│ Input:  A={}  B={}  C={}       │", a, b, c);
    println!("├────────────────────────────────┤");
    for (i, output) in outputs.iter().enumerate() {
        println!("│ Output {}: {}                  │", i + 1, output.as_str());
    }
    println!("└────────────────────────────────┘");
}

fn print_circuit(circuit: &Circuit) {
    println!("\n┌─ Circuit Status ──────────────┐");
    println!("│ Gates: {}                     │", circuit.gates.len());
    println!("│ Outputs: {}                   │", circuit.outputs.len());
    println!("├────────────────────────────────┤");

    if circuit.gates.is_empty() {
        println!("│ No gates added yet             │");
    } else {
        for (id, gate) in circuit.gates.iter() {
            println!("│ ID {}: {}                      │", id, gate.gate_type.as_str());
        }
    }

    println!("└────────────────────────────────┘");
}
