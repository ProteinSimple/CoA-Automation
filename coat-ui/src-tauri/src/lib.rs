// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
use std::process::Command;
use std::path::PathBuf;
use std::fs;
use dirs::home_dir;
use std::env;
use tauri::async_runtime::spawn_blocking;


// Not used anymore !
fn get_output_path() -> PathBuf {
    let home = home_dir().expect("Could not determine home directory");
    home.join("data").join("coat_output.txt")
}

fn get_temp_output_path() -> PathBuf {
    let mut temp_dir = env::temp_dir();
    let timestamp = chrono::Utc::now().timestamp();
    temp_dir.push(format!("coat_{}.out", timestamp));
    temp_dir
}

fn run_python_command_with_output(args: Vec<&str>) -> Result<String, String> {
    let output_path = get_temp_output_path();
    let output_path_str = output_path.to_str().ok_or("Invalid output path")?;

    // Append --output <file> to args
    let mut full_args = args.clone();
    full_args.push("--output");
    full_args.push(output_path_str);

    let exe_path = std::path::Path::new("src").join("main.exe");

    println!(
        "Running: {} {}",
        exe_path.display(),
        full_args
            .iter()
            .map(|s| format!("\"{}\"", s))
            .collect::<Vec<_>>()
            .join(" ")
    );

    let status = Command::new(exe_path)
        .args(full_args)
        .status()
        .map_err(|e| format!("Failed to run main.exe: {}", e))?;

    
    if !status.success() {
        return Err("Python script failed".into());
    }

    let result = fs::read_to_string(&output_path)
        .map_err(|e| format!("Failed to read output file: {}", e))?;

    Ok(result.trim().to_string())
}

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[tauri::command]
fn python_com() -> Result<String, String> {
    run_python_command_with_output(vec!["--help"])
}

#[tauri::command]
fn python_fetch_ids() -> Result<String, String> {
    run_python_command_with_output(vec!["fetch", "5", "50"])
}


#[tauri::command]
fn python_check() -> bool {
    match run_python_command_with_output(vec!["check"]) {
        Ok(output) => output == "1",
        Err(_) => false,
    }
}

#[tauri::command]
fn python_auth(user: String, pass: String) -> bool {
    match run_python_command_with_output(vec!["check", "--user", &user, "--passkey", &pass]) {
        Ok(output) => output == "1",
        Err(_) => false,
    }
}

#[tauri::command]
fn python_coa(id: String) -> Result<Vec<String>, String> {
    let output = run_python_command_with_output(vec!["coa", &id])?;

    let mut lines = output.lines();
    match lines.next() {
        Some("1") => Ok(lines.map(|s| s.to_string()).collect()),
        Some("0") => Err("Error during CoA creation".to_string()),
        Some(other) => Err(format!("Unexpected output prefix: {}", other)),
        None => Err("No output from Python script".to_string()),
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![
            greet,
            python_com,
            python_fetch_ids,
            python_check,
            python_coa,
            python_auth
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
