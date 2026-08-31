import React from 'react';
import { Link, useLocation } from 'react-router-dom';

export const Navbar: React.FC = () => {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <header style={{
      background: 'rgba(10, 10, 15, 0.9)',
      backdropFilter: 'blur(16px)',
      borderBottom: '1px solid var(--border-color)',
      position: 'sticky',
      top: 0,
      zIndex: 100
    }}>
      <div style={{
        maxWidth: 'var(--max-content-width)',
        margin: '0 auto',
        padding: '0.75rem var(--space-2xl)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)', textDecoration: 'none' }}>
          <div style={{
            fontSize: '1.25rem',
            background: 'linear-gradient(135deg, var(--color-primary), var(--color-primary-dark))',
            width: '32px',
            height: '32px',
            borderRadius: 'var(--radius-sm)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: 'var(--shadow-sm)'
          }}>✨</div>
          <span style={{ fontWeight: 800, fontSize: 'var(--font-size-lg)', color: 'var(--text-primary)', letterSpacing: '-0.01em' }}>
            Content Engine AI
          </span>
        </Link>

        <nav style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-lg)' }}>
          <Link
            to="/"
            style={{
              color: isActive('/') ? 'var(--text-primary)' : 'var(--text-secondary)',
              fontWeight: 600,
              fontSize: 'var(--font-size-sm)',
              textDecoration: 'none',
              transition: 'color var(--transition-fast)'
            }}
          >
            Campaigns
          </Link>
          <Link
            to="/campaigns/new"
            className="btn btn-primary btn-sm"
          >
            + New Campaign
          </Link>
        </nav>
      </div>
    </header>
  );
};
