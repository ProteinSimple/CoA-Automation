import { invoke } from "@tauri-apps/api/core";

export const pythonTestCom = async () => {
  return await invoke("python_com", {});
};

export const pythonFetchIds = async () => {
  return await invoke("python_fetch_ids", {});
};

export const pythonFetchRange = async (startDate: Date, endDate: Date) => {
  let start = startDate.toISOString().split('T')[0]
  let end = endDate.toISOString().split('T')[0]
  console.log(start, end);
  return await invoke("python_fetch_range", { start,  end})
}

export const pythonCheck = async () => {
  return await invoke("python_check", {})
}

export const pythonAuth = async (user: string, pass: string) => {
  return await invoke("python_auth", {user, pass})
}

export const pythonCoa = async (ids: string[]) => {
  return await invoke("python_coa", { ids })
}