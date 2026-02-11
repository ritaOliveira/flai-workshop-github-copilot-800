import React, { useState, useEffect } from 'react';

function Users() {
  const [users, setUsers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingUser, setEditingUser] = useState(null);
  const [formData, setFormData] = useState({ name: '', email: '', team_id: '' });
  const [saveError, setSaveError] = useState(null);
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const codespace = process.env.REACT_APP_CODESPACE_NAME;
      const baseUrl = codespace 
        ? `https://${codespace}-8000.app.github.dev/api`
        : 'http://localhost:8000/api';
      
      console.log('Fetching users and teams from:', baseUrl);
      
      const [usersResponse, teamsResponse] = await Promise.all([
        fetch(`${baseUrl}/users/`),
        fetch(`${baseUrl}/teams/`)
      ]);
      
      if (!usersResponse.ok || !teamsResponse.ok) {
        throw new Error('HTTP error! Failed to fetch data');
      }
      
      const usersData = await usersResponse.json();
      const teamsData = await teamsResponse.json();
      
      console.log('Users data received:', usersData);
      console.log('Teams data received:', teamsData);
      
      const processedUsers = usersData.results || usersData;
      const processedTeams = teamsData.results || teamsData;
      
      setUsers(Array.isArray(processedUsers) ? processedUsers : []);
      setTeams(Array.isArray(processedTeams) ? processedTeams : []);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError(err.message);
      setLoading(false);
    }
  };

  const handleEdit = (user) => {
    setEditingUser(user);
    setFormData({
      name: user.name,
      email: user.email,
      team_id: user.team_id || ''
    });
    setSaveError(null);
    setSaveSuccess(false);
  };

  const handleClose = () => {
    setEditingUser(null);
    setFormData({ name: '', email: '', team_id: '' });
    setSaveError(null);
    setSaveSuccess(false);
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSave = async () => {
    try {
      const codespace = process.env.REACT_APP_CODESPACE_NAME;
      const apiUrl = codespace 
        ? `https://${codespace}-8000.app.github.dev/api/users/${editingUser.id}/`
        : `http://localhost:8000/api/users/${editingUser.id}/`;
      
      const response = await fetch(apiUrl, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error('Failed to update user');
      }

      setSaveSuccess(true);
      setTimeout(() => {
        handleClose();
        fetchData(); // Refresh data
      }, 1000);
    } catch (err) {
      console.error('Error saving user:', err);
      setSaveError(err.message);
    }
  };

  const getTeamName = (teamId) => {
    const team = teams.find(t => t.id === teamId);
    return team ? team.name : 'No Team';
  };

  if (loading) return <div className="container mt-4"><div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger">Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <h2><i className="bi bi-person-badge-fill"></i> Users</h2>
      <p className="lead">All registered superhero members</p>
      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead className="table-dark">
            <tr>
              <th>Name</th>
              <th>Username</th>
              <th>Email</th>
              <th>Team</th>
              <th>Created At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.length > 0 ? (
              users.map((user) => (
                <tr key={user.id}>
                  <td><strong>{user.name}</strong></td>
                  <td>@{user.email ? user.email.split('@')[0] : 'N/A'}</td>
                  <td>{user.email}</td>
                  <td>{getTeamName(user.team_id)}</td>
                  <td>{new Date(user.created_at).toLocaleDateString()}</td>
                  <td>
                    <button 
                      className="btn btn-primary btn-sm" 
                      onClick={() => handleEdit(user)}
                    >
                      Edit
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6" className="text-center">No users found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Edit Modal */}
      {editingUser && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Edit User</h5>
                <button type="button" className="btn-close" onClick={handleClose}></button>
              </div>
              <div className="modal-body">
                {saveSuccess && (
                  <div className="alert alert-success">User updated successfully!</div>
                )}
                {saveError && (
                  <div className="alert alert-danger">Error: {saveError}</div>
                )}
                <div className="mb-3">
                  <label className="form-label">Name</label>
                  <input
                    type="text"
                    className="form-control"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Email</label>
                  <input
                    type="email"
                    className="form-control"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Team</label>
                  <select
                    className="form-select"
                    name="team_id"
                    value={formData.team_id}
                    onChange={handleChange}
                  >
                    <option value="">No Team</option>
                    {teams.map((team) => (
                      <option key={team.id} value={team.id}>
                        {team.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={handleClose}>
                  Cancel
                </button>
                <button type="button" className="btn btn-primary" onClick={handleSave}>
                  Save Changes
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Users;
