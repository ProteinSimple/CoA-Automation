import { invoke } from "@tauri-apps/api/core";

export const testPythoncom = async () => {
  return await invoke("python_com", {});
};

export const pythonListIds = async () => {
  return await invoke("python_list_ids", {});
};