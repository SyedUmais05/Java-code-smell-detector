import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
    const location = useLocation();

    return (
        <nav className="glass-nav">
            <div className="nav-container">
                <Link to="/" className="nav-logo">
                    <span>☕</span> JavaSmells
                </Link>
                <div className="nav-links">
                    <Link to="/" className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>
                        Home
                    </Link>
                    <Link to="/analyze" className={`nav-link ${location.pathname === '/analyze' ? 'active' : ''}`}>
                        Analyzer
                    </Link>
                    {/* Simple hash anchor for About, could be a real page too */}
                    <a href="/#about" className="nav-link">
                        About
                    </a>
                </div>
                {/* Placeholder for right side balance or action */}
                <div style={{ minWidth: '150px', textAlign: 'right' }}>
                    <Link to="/analyze" style={{
                        padding: '0.5rem 1.25rem',
                        fontSize: '0.9rem',
                        borderRadius: '8px',
                        background: '#1e293b',
                        color: 'white',
                        textDecoration: 'none',
                        fontWeight: '600'
                    }}>Launch App</Link>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
