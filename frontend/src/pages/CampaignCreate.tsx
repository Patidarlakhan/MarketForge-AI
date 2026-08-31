import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createCampaign } from '../api/campaigns';

export const CampaignCreate: React.FC = () => {
  const navigate = useNavigate();
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    name: 'Construction AI Leads',
    objective: 'Generate MQLs for AI Safety & Inspection Platform',
    industry: 'Construction',
    product_service: 'Physical AI Autonomous Jobsite Safety & Inspection Platform',
    target_audience: 'Mid-to-large General Contractors and Commercial Construction Firms',
    offer: 'Free Jobsite AI Safety Assessment',
    landing_page: 'https://example.com/ai-assessment',
    brand_info: 'Enterprise AI provider helping construction firms reduce delays and eliminate safety hazards.',
    tone: 'Professional',
  });

  const [personas, setPersonas] = useState<string[]>(['Chief Executive Officer (CEO)', 'Chief Operating Officer (COO)', 'Head of Safety & Risk Management']);
  const [newPersona, setNewPersona] = useState<string>('');
  const [painPoints, setPainPoints] = useState<string[]>(['Costly project delays and budget overruns', 'High rate of safety incidents and OSHA penalties', 'Manual inspection bottlenecks and inefficient compliance reporting', 'Skilled labor shortage impacting project execution']);
  const [newPainPoint, setNewPainPoint] = useState<string>('');

  const handleAddPersona = () => { if (newPersona.trim()) { setPersonas([...personas, newPersona.trim()]); setNewPersona(''); } };
  const handleRemovePersona = (index: number) => { setPersonas(personas.filter((_, idx) => idx !== index)); };
  const handleAddPainPoint = () => { if (newPainPoint.trim()) { setPainPoints([...painPoints, newPainPoint.trim()]); setNewPainPoint(''); } };
  const handleRemovePainPoint = (index: number) => { setPainPoints(painPoints.filter((_, idx) => idx !== index)); };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSubmitting(true); setError(null);
      const created = await createCampaign({ ...formData, target_personas: personas, pain_points: painPoints });
      navigate(`/campaigns/${created.id}`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to create campaign');
    } finally { setSubmitting(false); }
  };

  return (
    <div className="app-main animate-fade-in" style={{ maxWidth: '800px' }}>
      <div className="page-header">
        <h1>Create Campaign</h1>
        <p>Enter details about your product, audience, and offer.</p>
      </div>

      {error && (
        <div className="card mb-lg" style={{ borderColor: 'var(--color-error)', background: 'var(--color-error-bg)' }}>
          <p style={{ color: 'var(--color-error)', fontWeight: 600 }}>⚠️ {error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="card" style={{ padding: 'var(--space-2xl)' }}>
        <h3 className="section-heading mb-lg">1. Campaign Overview</h3>
        <div className="form-group">
          <label className="form-label">Campaign Name *</label>
          <input type="text" className="form-input" required value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} placeholder="e.g., Construction AI Leads" />
        </div>
        <div className="form-group">
          <label className="form-label">Objective *</label>
          <input type="text" className="form-input" required value={formData.objective} onChange={(e) => setFormData({ ...formData, objective: e.target.value })} />
        </div>
        <div className="form-group">
          <label className="form-label">Industry *</label>
          <input type="text" className="form-input" required value={formData.industry} onChange={(e) => setFormData({ ...formData, industry: e.target.value })} />
        </div>
        <div className="form-group">
          <label className="form-label">Product / Service *</label>
          <textarea className="form-textarea" required rows={3} value={formData.product_service} onChange={(e) => setFormData({ ...formData, product_service: e.target.value })} />
        </div>

        <div style={{ height: '1px', background: 'var(--border-color)', margin: 'var(--space-xl) 0' }}></div>
        <h3 className="section-heading mb-lg">2. Audience &amp; Personas</h3>
        <div className="form-group">
          <label className="form-label">Target Audience *</label>
          <input type="text" className="form-input" required value={formData.target_audience} onChange={(e) => setFormData({ ...formData, target_audience: e.target.value })} />
        </div>
        <div className="form-group">
          <label className="form-label">Target Personas</label>
          <div className="flex gap-sm mb-sm">
            <input type="text" className="form-input" value={newPersona} onChange={(e) => setNewPersona(e.target.value)} placeholder="Add persona..." onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); handleAddPersona(); } }} />
            <button type="button" onClick={handleAddPersona} className="btn btn-secondary">Add</button>
          </div>
          <div className="chip-container">
            {personas.map((p, idx) => (<span key={idx} className="chip">👤 {p}<button type="button" onClick={() => handleRemovePersona(idx)} className="chip-remove">×</button></span>))}
          </div>
        </div>
        <div className="form-group">
          <label className="form-label">Pain Points</label>
          <div className="flex gap-sm mb-sm">
            <input type="text" className="form-input" value={newPainPoint} onChange={(e) => setNewPainPoint(e.target.value)} placeholder="Add pain point..." onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); handleAddPainPoint(); } }} />
            <button type="button" onClick={handleAddPainPoint} className="btn btn-secondary">Add</button>
          </div>
          <div className="chip-container">
            {painPoints.map((pt, idx) => (<span key={idx} className="chip chip-warning">⚡ {pt}<button type="button" onClick={() => handleRemovePainPoint(idx)} className="chip-remove">×</button></span>))}
          </div>
        </div>

        <div style={{ height: '1px', background: 'var(--border-color)', margin: 'var(--space-xl) 0' }}></div>
        <h3 className="section-heading mb-lg">3. Offer &amp; Brand</h3>
        <div className="form-group">
          <label className="form-label">Lead Magnet / Offer</label>
          <input type="text" className="form-input" value={formData.offer} onChange={(e) => setFormData({ ...formData, offer: e.target.value })} />
        </div>
        <div className="form-group">
          <label className="form-label">Landing Page URL</label>
          <input type="url" className="form-input" value={formData.landing_page} onChange={(e) => setFormData({ ...formData, landing_page: e.target.value })} />
        </div>
        <div className="form-group">
          <label className="form-label">Brand Context</label>
          <textarea className="form-textarea" rows={3} value={formData.brand_info} onChange={(e) => setFormData({ ...formData, brand_info: e.target.value })} />
        </div>
        <div className="form-group">
          <label className="form-label">Tone</label>
          <select className="form-select" value={formData.tone} onChange={(e) => setFormData({ ...formData, tone: e.target.value })}>
            <option value="Professional">Professional &amp; Authoritative</option>
            <option value="Bold & Tech-forward">Bold &amp; Tech-forward</option>
            <option value="Conversational & Friendly">Conversational &amp; Friendly</option>
            <option value="Urgent & Action-Oriented">Urgent &amp; Action-Oriented</option>
            <option value="Educational & Insightful">Educational &amp; Insightful</option>
          </select>
        </div>

        <div style={{ height: '1px', background: 'var(--border-color)', margin: 'var(--space-xl) 0' }}></div>
        <div className="flex justify-between items-center">
          <button type="button" onClick={() => navigate('/')} className="btn btn-ghost">Cancel</button>
          <button type="submit" disabled={submitting} className="btn btn-primary" style={{ padding: '0.625rem 1.5rem' }}>
            {submitting ? (<><div className="spinner"></div> Creating...</>) : 'Save & Proceed →'}
          </button>
        </div>
      </form>
    </div>
  );
};
