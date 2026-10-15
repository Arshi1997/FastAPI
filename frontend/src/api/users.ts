import { api } from "./client";

export interface User {
  id: number;
  name: string;
  age: number;
  std: string;
  gender: string;
  email?: string; // email is optional
}

export async function getUsers(): Promise<User[]> {
  const response = await api.get("/api/users");
  return response.data.users;
}