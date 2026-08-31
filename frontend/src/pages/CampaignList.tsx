import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { listCampaigns, deleteCampaign } from '../api/campaigns';
import type { Campaign } from '../types/campaign';
import { StatusBadge } from '../components/StatusBadge';

export const CampaignList: React.FC = () => {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>('');

  const fetchCampaigns = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await listCampaigns();
      setCampaigns(data);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to load campaigns';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchCampaigns(); }, []);

  const handleDelete = async (id: string, name: string, e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!window.confirm(`Are you sure you want to delete campaign "${name}"?`)) return;
    try {
      await deleteCampaign(id);
      setCampaigns((prev) => prev.filter((c) => c.id !== id));
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : 'Failed to delete campaign');
    }
  };

  const filteredCampaigns = campaigns.filter(
    (c) =>
      c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.industry.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.objective.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const completedCount = campaigns.filter(c => c.status === 'completed').length;
  const inProgressCount = campaigns.filter(c => c.status !== 'completed' && c.status !== 'draft').length;

  return (
    <div className="app-main animate-fade-in">
      <div className="page-header flex justify-between items-center" style={{ flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1>Marketing Campaigns</h1>
          <p>Manage, generate, and review AI content campaigns</p>
        </div>
      </div>

      {!loading && !error && (
        <div className="flex gap-md mb-xl" style={{ flexWrap: 'wrap' }}>
          <div className="stat-card" style={{ flex: 1 }}>
            <span className="stat-value">{campaigns.length}</span>
            <span className="stat-label">Total</span>
          </div>
          <div className="stat-card" style={{ flex: 1 }}>
            <span className="stat-value" style={{ color: 'var(--color-success)' }}>{completedCount}</span>
            <span className="stat-label">Completed</span>
          </div>
          <div className="stat-card" style={{ flex: 1 }}>
            <span className="stat-value" style={{ color: 'var(--color-primary)' }}>{inProgressCount}</span>
            <span className="stat-label">In Progress</span>
          </div>
        </div>
      )}

      <div className="mb-lg">
        <input
          type="text"
          className="form-input"
          placeholder="🔍 Search campaigns by name, industry, or objective..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{ maxWidth: '420px' }}
        />
      </div>

      {loading && (
        <div className="text-center" style={{ padding: '5rem 0' }}>
          <div className="spinner spinner-lg" style={{ margin: '0 auto var(--space-md)' }}></div>
          <p className="text-muted">Loading campaigns...</p>
        </div>
      )}

      {error && (
        <div className="card text-center" style={{ borderColor: 'var(--color-error)' }}>
          <p style={{ color: 'var(--color-error)', fontWeight: 600 }}>{error}</p>
          <button onClick={fetchCampaigns} className="btn btn-secondary mt-md">Retry</button>
        </div>
      )}

      {!loading && !error && filteredCampaigns.length === 0 && (
        <div className="card text-center" style={{ padding: '5rem 2rem', borderStyle: 'dashed' }}>
          <div style={{ fontSize: '3rem', marginBottom: '1rem', opacity: 0.5 }}>📋</div>
          <h2 style={{ fontSize: 'var(--font-size-xl)', fontWeight: 700, marginBottom: '0.5rem' }}>No campaigns found</h2>
          <p className="text-muted" style={{ maxWidth: '400px', margin: '0 auto var(--space-lg)' }}>
            {searchQuery ? 'No campaigns match your search.' : 'Create your first campaign to start generating AI marketing content.'}
          </p>
          <Link to="/campaigns/new" className="btn btn-primary">+ Create Campaign</Link>
        </div>
      )}

      {!loading && !error && filteredCampaigns.length > 0 && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: 'var(--space-md)' }}>
          {filteredCampaigns.map((campaign) => (
            <Link key={campaign.id} to={`/campaigns/${campaign.id}`} className="card" style={{ display: 'flex', flexDirection: 'column', textDecoration: 'none', color: 'inherit' }}>
              <div className="flex justify-between items-center mb-md">
                <StatusBadge status={campaign.status} />
                <span style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-tertiary)' }}>
                  {new Date(campaign.created_at).toLocaleDateString()}
                </span>
              </div>
              <h3 style={{ fontSize: 'var(--font-size-lg)', fontWeight: 700, marginBottom: '0.375rem' }}>{campaign.name}</h3>
              <div className="flex gap-xs mb-md" style={{ flexWrap: 'wrap' }}>
                <span className="chip" style={{ fontSize: '0.7rem' }}>🏢 {campaign.industry}</span>
                <span className="chip" style={{ fontSize: '0.7rem' }}>🎯 {campaign.objective}</span>
              </div>
              <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--text-secondary)', marginBottom: 'var(--space-md)', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                {campaign.product_service}
              </p>
              <div className="flex justify-between items-center mt-auto" style={{ borderTop: '1px solid var(--border-color)', paddingTop: 'var(--space-sm)' }}>
                <span style={{ fontSize: 'var(--font-size-sm)', fontWeight: 600, color: 'var(--color-primary)' }}>View →</span>
                <button onClick={(e) => handleDelete(campaign.id, campaign.name, e)} className="btn btn-ghost btn-sm" style={{ color: 'var(--color-error)' }}>Delete</button>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};
