import { useEffect, useState } from "react";
import { getUsers, type User } from "../api/users";

export default function Users() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getUsers()
      .then(setUsers)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <h2>Users</h2>
          <p>Users retrieved from FastAPI and PostgreSQL.</p>
        </div>
        <button className="primary-button">+ Add User</button>
      </div>

      {loading ? (
        <div className="empty-state">Loading users...</div>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Age</th>
                <th>Class</th>
                <th>Gender</th>
                <th>Email</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>{user.id}</td>
                  <td>
                    <strong>{user.name}</strong>
                  </td>
                  <td>{user.age}</td>
                  <td>{user.std}</td>
                  <td>{user.gender}</td>
                  <td>{user.email || "N/A"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}