import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
          <div className="container-fluid">
            <Link className="navbar-brand" to="/">
              <img src="/logo.png" alt="OctoFit Logo" className="navbar-logo" />
              <strong>OctoFit Tracker</strong>
            </Link>
            <button 
              className="navbar-toggler" 
              type="button" 
              data-bs-toggle="collapse" 
              data-bs-target="#navbarNav"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">Teams</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/users">Users</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">Activities</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">Workouts</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">Leaderboard</Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <div className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/teams" element={<Teams />} />
            <Route path="/users" element={<Users />} />
            <Route path="/activities" element={<Activities />} />
            <Route path="/workouts" element={<Workouts />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

function Home() {
  return (
    <div className="container mt-5">
      <div className="jumbotron">
        <h1 className="display-4">Welcome to OctoFit Tracker! 🏋️</h1>
        <p className="lead">Track your fitness journey with superhero-themed teams and activities.</p>
        <hr className="my-4" />
        <p>Navigate through the menu to explore:</p>
        <div className="row mt-4">
          <div className="col-md-4 mb-3">
            <Link to="/teams" style={{ textDecoration: 'none' }}>
              <div className="card" style={{ cursor: 'pointer' }}>
                <div className="card-body">
                  <h5 className="card-title">👥 Teams</h5>
                  <p className="card-text">View Team Marvel and Team DC</p>
                  <span className="btn btn-primary">View Teams</span>
                </div>
              </div>
            </Link>
          </div>
          <div className="col-md-4 mb-3">
            <Link to="/users" style={{ textDecoration: 'none' }}>
              <div className="card" style={{ cursor: 'pointer' }}>
                <div className="card-body">
                  <h5 className="card-title">🦸 Users</h5>
                  <p className="card-text">See all superhero members</p>
                  <span className="btn btn-primary">View Users</span>
                </div>
              </div>
            </Link>
          </div>
          <div className="col-md-4 mb-3">
            <Link to="/activities" style={{ textDecoration: 'none' }}>
              <div className="card" style={{ cursor: 'pointer' }}>
                <div className="card-body">
                  <h5 className="card-title">🏃 Activities</h5>
                  <p className="card-text">Track fitness activities</p>
                  <span className="btn btn-primary">View Activities</span>
                </div>
              </div>
            </Link>
          </div>
          <div className="col-md-4 mb-3">
            <Link to="/workouts" style={{ textDecoration: 'none' }}>
              <div className="card" style={{ cursor: 'pointer' }}>
                <div className="card-body">
                  <h5 className="card-title">💪 Workouts</h5>
                  <p className="card-text">Browse workout plans</p>
                  <span className="btn btn-primary">View Workouts</span>
                </div>
              </div>
            </Link>
          </div>
          <div className="col-md-4 mb-3">
            <Link to="/leaderboard" style={{ textDecoration: 'none' }}>
              <div className="card" style={{ cursor: 'pointer' }}>
                <div className="card-body">
                  <h5 className="card-title">🏆 Leaderboard</h5>
                  <p className="card-text">Check team rankings</p>
                  <span className="btn btn-primary">View Leaderboard</span>
                </div>
              </div>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
