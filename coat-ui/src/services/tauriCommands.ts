import { invoke } from "@tauri-apps/api/core";

const testPythoncom = async () => {
    return await invoke("python_com", {})
}

export default testPythoncom;