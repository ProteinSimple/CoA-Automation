import { invoke } from "@tauri-apps/api/core";

export const pythonTestCom = async () => {
  return await invoke("python_com", {});
};

export const pythonFetchIds = async () => {
  return await invoke("python_fetch_ids", {});
};

export const pythonCheck = async () => {
  return await invoke("python_check", {})
}

export const pythonAuth = async (user: string, pass: string) => {
  return await invoke("python_auth", {user, pass})
}

export const pythonCoa = async (ids: string[]) => {
  return await invoke("python_coa", { ids })
}