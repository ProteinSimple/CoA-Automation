// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
use std::process::Command;

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[tauri::command]
fn python_com() -> Result<String, String>  {
    let exe_path = std::path::Path::new("src").join("main.exe");
    let output = Command::new(exe_path)
        .arg("--help")
        .output()
        .map_err(|e| format!("Failed to run main.exe: {}", e))?;

    if output.status.success() {
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    } else {
        Err(String::from_utf8_lossy(&output.stderr).to_string())
    }

}


#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![
            greet,
            python_com
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
