// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
use std::env;
use std::fs;
use std::path::PathBuf;
use std::process::Command;
use tauri::async_runtime::spawn_blocking;
use uuid::Uuid;

fn get_temp_output_path() -> PathBuf {
    let mut temp_dir = env::temp_dir();
    let unique_id = Uuid::new_v4(); // generate a truly unique identifier
    temp_dir.push(format!("coat_{}.out", unique_id));
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
    })
    .await
    .map_err(|e| format!("Failed to spawn blocking task: {}", e))?
}


#[tauri::command]
async fn python_check() -> Result<bool, String> {
    match run_python_command_with_output(vec![
        "check".to_string(),
    ])
    .await
    {
        Ok(output) => {
            let result = output.trim().starts_with("1");
            Ok(result)
        },
        Err(e) => {
            Err(format!("Check failed: {}", e))
        }
    }
}

#[tauri::command]
async fn python_auth(user: String, pass: String) -> bool {
    match run_python_command_with_output(vec![
        "check".to_string(),
        "--user".to_string(),
        user,
        "--passkey".to_string(),
        pass,
    ])
    .await
    {
        Ok(output) => output == "1",
        Err(_) => false,
    }
}


#[tauri::command]
async fn python_call(args: Vec<String>) -> Result<String, String> {
    let output = run_python_command_with_output(args).await?;
    
    // println!("[python_call] output:\n{}", output);
    let mut lines = output.lines();
    match lines.next() {
        Some("1") => {
            let result = lines.collect::<Vec<_>>().join("\n");
            Ok(result)
        },
        Some("0") => {
            let err_msg = lines.collect::<Vec<_>>().join("\n");
            Err(format!("Python script failed:\n{}", err_msg))
        }
        Some(other) => Err(format!("Unexpected output prefix: {}", other)),
        None => Err("No output from Python script.".to_string()),
    }
}


#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![
            python_check,
            python_auth,
            python_call,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
