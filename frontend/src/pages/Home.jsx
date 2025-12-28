import React from 'react';
import { Link } from 'react-router-dom';

/* Note: image will be in public folder or assets, 
   but for direct public serving we can just use /hero_illustration.webp if we move it there.
   Let's assume we place it in public/ as requested by standard Vite patterns for dynamic assets, 
   or src/assets for imports. I'll use src/assets import if possible, but the user said "i will add images in the folder here". 
   Structure-wise, dumping in public is easier for them.
   Let's use absolute path /hero_illustration.webp assuming it's in public.
*/

const Home = () => {

    const smells = [
        { category: "Bloaters", smell: "Long Method", heuristic: "> 40 lines (estimated)" },
        { category: "", smell: "Large Class", heuristic: "> 15 methods" },
        { category: "", smell: "Data Clumps", heuristic: "≥3 repeated params in ≥2 methods" },
        { category: "OO Abusers", smell: "Switch Statements", heuristic: "> 5 cases" },
        { category: "", smell: "Refused Bequest", heuristic: "Throws UnsupportedOperationException" },
        { category: "Dispensables", smell: "Duplicate Code", heuristic: "Identical block > 6 lines" },
        { category: "", smell: "Dead Code", heuristic: "Unused private methods" },
        { category: "Couplers", smell: "Message Chains", heuristic: "> 3 chained calls" },
        { category: "", smell: "Feature Envy", heuristic: "Frequent foreign data usage" },
    ];

    return (
        <div className="home-page">
            {/* Hero Section */}
            <section className="hero-section">
                <div className="hero-container">
                    <div className="hero-content fade-in">
                        <h1 className="hero-title">
                            Code Quality <br />
                            <span className="hero-highlight">Redefined.</span>
                        </h1>
                        <p className="hero-subtitle">
                            Don't let code smells rot your software. Detected instantly, explained clearly, and refactored easily with JavaSmells.
                        </p>
                        <div className="hero-actions">
                            <Link to="/analyze" className="btn-large">
                                Get Started
                            </Link>
                        </div>
                    </div>
                    <div className="hero-image-wrapper fade-in">
                        {/* User can replace this with their own image if they want, but we provide the generated one */}
                        <img src="/hero_illustration.png" alt="Code Analysis" className="hero-img" />
                    </div>
                </div>
            </section>

            {/* About Section */}
            <section className="about-section" id="about">
                <div className="section-container">
                    <div className="section-header">
                        <h2>Supported Code Smells</h2>
                        <p className="section-desc">
                            Our engine uses academic rule-based heuristics to identify these specific design flaws.
                        </p>
                    </div>

                    <div className="smell-table-wrapper">
                        <table className="smell-table">
                            <thead>
                                <tr>
                                    <th>Category</th>
                                    <th>Smell</th>
                                    <th>Heuristic Rule</th>
                                </tr>
                            </thead>
                            <tbody>
                                {smells.map((item, index) => (
                                    <tr key={index}>
                                        <td>{item.category}</td>
                                        <td><strong>{item.smell}</strong></td>
                                        <td>{item.heuristic}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>

            {/* Team Section */}
            <section className="team-section">
                <div className="section-container">
                    <div className="section-header">
                        <h2>Meet The Team</h2>
                        <p className="section-desc">The developers behind JavaSmells.</p>
                    </div>

                    <div className="team-grid">
                        {[
                            { id: 1, name: "Syed Umais", role: "Cross-Platform App Developer", linkedin: "https://www.linkedin.com/in/syed-umais-ix3" },
                            { id: 2, name: "Danial Saleem", role: "Cybersecurity Engineer", linkedin: "https://www.linkedin.com/in/danial-saleem-38144225a/" },
                            { id: 3, name: "Atta Ur Rehman", role: "UML / Documentation Specialist" },
                            { id: 4, name: "M Faseeh", role: "Full-Stack Web Developer" },
                            { id: 5, name: "Muhammad Raza", role: "Game Developer" }
                        ].map((member) => (
                            <div key={member.id} className="team-card">
                                {member.linkedin ? (
                                    <a href={member.linkedin} target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none', color: 'inherit', display: 'block', height: '100%' }}>
                                        <div className="team-img-wrapper">
                                            <img src={`/p${member.id}.jpg`} alt={member.name} className="team-img"
                                                onError={(e) => { e.target.src = 'https://via.placeholder.com/150' }} />
                                        </div>
                                        <h3>{member.name}</h3>
                                        <span className="team-role">{member.role}</span>
                                    </a>
                                ) : (
                                    <>
                                        <div className="team-img-wrapper">
                                            <img src={`/p${member.id}.jpg`} alt={member.name} className="team-img"
                                                onError={(e) => { e.target.src = 'https://via.placeholder.com/150' }} />
                                        </div>
                                        <h3>{member.name}</h3>
                                        <span className="team-role">{member.role}</span>
                                    </>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            <footer className="home-footer">
                <p>© 2025 JavaSmells. Built for Academic Software Re-engineering.</p>
            </footer>
        </div>
    );
};

export default Home;
