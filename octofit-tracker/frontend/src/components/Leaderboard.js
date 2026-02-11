import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [users, setUsers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const codespace = process.env.REACT_APP_CODESPACE_NAME;
        const baseUrl = codespace 
          ? `https://${codespace}-8000.app.github.dev/api`
          : 'http://localhost:8000/api';
        
        console.log('Fetching leaderboard, users, and teams from:', baseUrl);
        
        // Fetch all data
        const [leaderboardResponse, usersResponse, teamsResponse] = await Promise.all([
          fetch(`${baseUrl}/leaderboard/`),
          fetch(`${baseUrl}/users/`),
          fetch(`${baseUrl}/teams/`)
        ]);
        
        if (!leaderboardResponse.ok || !usersResponse.ok || !teamsResponse.ok) {
          throw new Error('HTTP error! Failed to fetch data');
        }
        
        const leaderboardData = await leaderboardResponse.json();
        const usersData = await usersResponse.json();
        const teamsData = await teamsResponse.json();
        
        console.log('Leaderboard data received:', leaderboardData);
        console.log('Users data received:', usersData);
        console.log('Teams data received:', teamsData);
        
        // Handle both paginated (.results) and plain array responses
        const processedLeaderboard = leaderboardData.results || leaderboardData;
        const processedUsers = usersData.results || usersData;
        const processedTeams = teamsData.results || teamsData;
        
        setLeaderboard(Array.isArray(processedLeaderboard) ? processedLeaderboard : []);
        setUsers(Array.isArray(processedUsers) ? processedUsers : []);
        setTeams(Array.isArray(processedTeams) ? processedTeams : []);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Get user name by user_id
  const getUserName = (userId) => {
    const user = users.find(u => u.id === userId);
    return user ? user.name : 'Unknown User';
  };

  // Get team name by team_id
  const getTeamName = (teamId) => {
    const team = teams.find(t => t.id === teamId);
    return team ? team.name : 'N/A';
  };

  if (loading) return <div className="container mt-4"><div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger">Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <h2><i className="bi bi-trophy-fill"></i> Leaderboard</h2>
      <p className="lead">Top performers ranked by total calories burned</p>
      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead className="table-dark">
            <tr>
              <th>Rank</th>
              <th>User</th>
              <th>Team</th>
              <th>Total Calories</th>
              <th>Total Activities</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.length > 0 ? (
              leaderboard.map((entry) => (
                <tr key={entry.id}>
                  <td><span className="badge bg-primary">#{entry.rank}</span></td>
                  <td><strong>{getUserName(entry.user_id)}</strong></td>
                  <td>{getTeamName(entry.team_id)}</td>
                  <td><span className="badge bg-warning">{entry.total_calories || 0} cal</span></td>
                  <td>{entry.total_activities || 0}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5" className="text-center">No leaderboard entries found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Leaderboard;
