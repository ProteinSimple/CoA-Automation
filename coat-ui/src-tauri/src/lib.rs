// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
use std::process::Command;
use std::path::PathBuf;
use std::fs;
use dirs::home_dir;

fn get_output_path() -> PathBuf {
    let home = home_dir().expect("Could not determine home directory");
    home.join("data").join("coat_output.txt")
}


fn run_python_command_with_output(args: Vec<&str>) -> Result<String, String> {
    let output_path = get_output_path();
    let output_path_str = output_path.to_str().ok_or("Invalid output path")?;

    // Append --output <file> to args
    let mut full_args = args.clone();
    full_args.push("--output");
    full_args.push(output_path_str);

    let exe_path = std::path::Path::new("src").join("main.exe");
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
fn python_coa(id: String) {
    let exe_path = std::path::Path::new("src").join("main.exe");

    let _ = Command::new(exe_path)
        .arg("coa")
        .arg(id)
        .output(); // Ignore result intentionally, as it returns nothing
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
