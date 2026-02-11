import React, { useState, useEffect } from 'react';

function Activities() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        const codespace = process.env.REACT_APP_CODESPACE_NAME;
        const apiUrl = codespace 
          ? `https://${codespace}-8000.app.github.dev/api/activities/`
          : 'http://localhost:8000/api/activities/';
        
        console.log('Fetching activities from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Activities data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const activitiesData = data.results || data;
        console.log('Processed activities:', activitiesData);
        
        setActivities(Array.isArray(activitiesData) ? activitiesData : []);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching activities:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchActivities();
  }, []);

  if (loading) return <div className="container mt-4"><div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger">Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <h2><i className="bi bi-activity"></i> Activities</h2>
      <p className="lead">Track all superhero fitness activities</p>
      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead className="table-dark">
            <tr>
              <th>Activity Type</th>
              <th>Duration (min)</th>
              <th>Calories Burned</th>
              <th>Distance (km)</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {activities.length > 0 ? (
              activities.map((activity) => {
                // Parse date string (YYYY-MM-DD) to avoid timezone issues
                const dateStr = activity.date;
                const formattedDate = dateStr ? new Date(dateStr + 'T00:00:00').toLocaleDateString() : 'N/A';
                
                return (
                  <tr key={activity.id}>
                    <td>{activity.activity_type}</td>
                    <td>{activity.duration}</td>
                    <td>{activity.calories_burned}</td>
                    <td>{activity.distance || 'N/A'}</td>
                    <td>{formattedDate}</td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan="5" className="text-center">No activities found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Activities;
