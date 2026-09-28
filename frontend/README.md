# React + FastAPI Frontend

A ready-to-run React frontend built with:

- React
- Vite
- TypeScript
- React Router
- Axios
- Mock data by default

## Requirements

- Node.js 20+ recommended
- npm

## Run

```bash
npm install
npm run dev
```

Open:

http://localhost:5173

## Connect FastAPI

Create `.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_USE_MOCK_DATA=false
```

Then replace the mock API functions in:

```text
src/api/
```

Example:

```ts
export async function getUsers(): Promise<User[]> {
  const response = await api.get<User[]>("/api/users");
  return response.data;
}
```

Your FastAPI endpoint could be:

```python
@app.get("/api/users")
def get_users():
    ...
```

## Project structure

```text
src/
├── api/
│   ├── client.ts
│   └── users.ts
├── pages/
│   ├── Dashboard.tsx
│   ├── Users.tsx
│   └── Settings.tsx
├── App.tsx
├── main.tsx
└── styles.css
```

The UI is intentionally independent from the backend so you can integrate your FastAPI API layer yourself.
