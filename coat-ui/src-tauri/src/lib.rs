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

async fn run_python_command_with_output(args: Vec<String>) -> Result<String, String> {
    spawn_blocking(move || {
        let output_path = get_temp_output_path();
        let output_path_str = output_path.to_str().ok_or("Invalid output path")?;

        let mut full_args = args.clone();
        full_args.push("--output".to_string());
        full_args.push(output_path_str.to_string());

        let exe_path = std::path::Path::new("src").join("main.exe");

        // println!(
        //     "Running: {} {}",
        //     exe_path.display(),
        //     full_args
        //         .iter()
        //         .map(|s| format!("\"{}\"", s))
        //         .collect::<Vec<_>>()
        //         .join(" ")
        // );

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
    })
    .await
    .map_err(|e| format!("Failed to spawn blocking task: {}", e))?
}

// 🔁 All Tauri commands using subprocess now async

#[tauri::command]
async fn python_com() -> Result<String, String> {
    run_python_command_with_output(vec!["--help".to_string()]).await
}

#[tauri::command]
async fn python_fetch_ids() -> Result<String, String> {
    run_python_command_with_output(vec!["fetch".to_string(), "5".to_string(), "50".to_string()]).await
}

#[tauri::command]
async fn python_check() -> bool {
    match run_python_command_with_output(vec!["check".to_string()]).await {
        Ok(output) => output == "1",
        Err(_) => false,
    }
}

#[tauri::command]
async fn python_auth(user: String, pass: String) -> bool {
    match run_python_command_with_output(vec![
        "check".to_string(),
        "--user".to_string(),
        user,
        "--passkey".to_string(),
    pass]).await {
        Ok(output) => output == "1",
        Err(_) => false,
    }
}

#[tauri::command]
async fn python_coa(ids: Vec<String>) -> Result<Vec<String>, String> {
    // eprintln!("[CMD] python_coa invoked with ids: {:?}", ids); 
    let mut args = vec!["coa".to_string()];
    args.extend(ids);
    let output = run_python_command_with_output(args).await?;

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
            python_com,
            python_fetch_ids,
            python_check,
            python_coa,
            python_auth
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
