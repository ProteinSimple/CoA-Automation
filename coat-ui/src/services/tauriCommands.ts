import { invoke } from "@tauri-apps/api/core";

export const pythonTestCom = async () => {
  return await invoke("python_call", {args: ["--help"]});
};

export const pythonFetchRange = async (startDate: Date, endDate: Date) => {
  let start = startDate.toISOString().split('T')[0]
  let end = endDate.toISOString().split('T')[0]
  return await invoke("python_call", { args: ["fetch" , start,  end]})
}

export const pythonCheck = async () => {
  const result = await invoke("python_check");
  return result;
}

export const pythonAuth = async (user: string, pass: string) => {
  return await invoke("python_auth", {user, pass})
}

export const pythonCoa = async (ids: number[], name: string, startDate: Date, endDate: Date) => {
  const start = startDate.toISOString().split('T')[0]
  const end = endDate.toISOString().split('T')[0]
  const ids_str = ids.map(String);
  return await invoke("python_call", { args:  ["coa", ...ids_str, "--name", name, "--start", start, '--end', end] })
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