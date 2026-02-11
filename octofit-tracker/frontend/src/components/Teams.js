import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const codespace = process.env.REACT_APP_CODESPACE_NAME;
        const baseUrl = codespace 
          ? `https://${codespace}-8000.app.github.dev/api`
          : 'http://localhost:8000/api';
        
        console.log('Fetching teams and users from:', baseUrl);
        
        // Fetch both teams and users
        const [teamsResponse, usersResponse] = await Promise.all([
          fetch(`${baseUrl}/teams/`),
          fetch(`${baseUrl}/users/`)
        ]);
        
        if (!teamsResponse.ok || !usersResponse.ok) {
          throw new Error('HTTP error! Failed to fetch data');
        }
        
        const teamsData = await teamsResponse.json();
        const usersData = await usersResponse.json();
        
        console.log('Teams data received:', teamsData);
        console.log('Users data received:', usersData);
        
        // Handle both paginated (.results) and plain array responses
        const processedTeams = teamsData.results || teamsData;
        const processedUsers = usersData.results || usersData;
        
        setTeams(Array.isArray(processedTeams) ? processedTeams : []);
        setUsers(Array.isArray(processedUsers) ? processedUsers : []);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Count members for a team
  const getMemberCount = (teamId) => {
    return users.filter(user => user.team_id === teamId).length;
  };

  if (loading) return <div className="container mt-4"><div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger">Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <h2><i className="bi bi-people-fill"></i> Teams</h2>
      <p className="lead">Superhero fitness teams competing for glory</p>
      <div className="row">
        {teams.length > 0 ? (
          teams.map((team) => (
            <div key={team.id} className="col-md-6 mb-4">
              <div className="card">
                <div className="card-header bg-primary text-white">
                  <h5 className="card-title mb-0">{team.name}</h5>
                </div>
                <div className="card-body">
                  <p className="card-text">{team.description}</p>
                  <div className="mb-2">
                    <span className="badge bg-primary">
                      {getMemberCount(team.id)} Members
                    </span>
                  </div>
                  <p className="text-muted small">Created: {new Date(team.created_at).toLocaleDateString()}</p>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-12">
            <div className="alert alert-info">No teams found</div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Teams;
