import { invoke } from "@tauri-apps/api/core";

export const pythonTestCom = async () => {
  return await invoke("python_call", {args: ["--help"]});
};

export const pythonFetchRange = async (startDate: Date, endDate: Date) => {
  let start = startDate.toISOString().split('T')[0]
  let end = endDate.toISOString().split('T')[0]
  return await invoke("python_call", { args: ["fetch", "range", start,  end]})
}

export const pythonCheck = async () => {
  return await invoke("python_check", {})
}

export const pythonAuth = async (user: string, pass: string) => {
  return await invoke("python_auth", {user, pass})
}

export const pythonCoa = async (ids: string[]) => {
  return await invoke("python_call", { args:  ["coa", ...ids] })
}

export const pythonConfigList = async () => {
  return await invoke("python_call", { args: ["config", "list"]})
}

export const pythonConfigAddPdf = async (path: string[]): Promise<string>  => {
  return await invoke("python_call", { args: ["config", "add", "--pdf", ...path]})
}

export const pythonConfigDeletePdf = async (path: string[]): Promise<string>  => {
  return await invoke("python_call", { args: ["config", "delete", "--pdf", ...path]})
}


export const pythonConfigAddMapping = async (path: string[]): Promise<string>  => {
  return await invoke("python_call", { args: ["config", "add", "--csv", ...path]})
}

export const pythonConfigDeleteMapping = async (path: string[]): Promise<string>  => {
  return await invoke("python_call", { args: ["config", "delete", "--csv", ...path]})
}