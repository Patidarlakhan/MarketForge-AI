import React from 'react';
import type { MasterContentOutput } from '../types/masterContent';

interface MasterContentViewProps {
  content: MasterContentOutput;
  onRegenerate: () => void;
  regenerating: boolean;
}

export const MasterContentView: React.FC<MasterContentViewProps> = ({ content, onRegenerate, regenerating }) => {
  return (
    <div className="card animate-fade-in mb-xl">
      <div className="flex justify-between items-center mb-lg" style={{ flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: 'var(--font-size-xl)', fontWeight: 700 }}>✍️ Master Content Blueprint</h2>
          <p className="text-muted" style={{ fontSize: 'var(--font-size-sm)' }}>Platform-neutral core narrative</p>
        </div>
        <button onClick={onRegenerate} disabled={regenerating} className="btn btn-secondary">
          {regenerating ? (<><div className="spinner"></div> Regenerating...</>) : '🔄 Regenerate'}
        </button>
      </div>

      <div className="master-title-box mb-lg">
        <span className="master-label">Master Campaign Headline</span>
        <h3 style={{ fontSize: 'var(--font-size-2xl)', fontWeight: 800, marginTop: '0.5rem' }}>"{content.title}"</h3>
      </div>

      <div className="master-grid mb-lg">
        <div className="card-flat strategy-section" style={{ borderLeftColor: 'var(--color-primary)' }}>
          <h4 className="strategy-title">🌟 Core Concept</h4>
          <p style={{ lineHeight: 1.6 }}>{content.core_idea}</p>
        </div>
        <div className="card-flat strategy-section" style={{ borderLeftColor: 'var(--color-accent)' }}>
          <h4 className="strategy-title">🎯 Key Message</h4>
          <p style={{ fontWeight: 600, fontStyle: 'italic', lineHeight: 1.6 }}>"{content.key_message}"</p>
        </div>
      </div>

      <div className="master-grid mb-lg">
        <div className="card-flat strategy-section" style={{ borderLeftColor: 'var(--color-error)', background: 'var(--color-error-bg)' }}>
          <h4 className="strategy-title" style={{ color: 'var(--color-error)' }}>⚠️ Problem &amp; Pain Points</h4>
          <p style={{ lineHeight: 1.6 }}>{content.problem}</p>
        </div>
        <div className="card-flat strategy-section" style={{ borderLeftColor: 'var(--color-success)', background: 'var(--color-success-bg)' }}>
          <h4 className="strategy-title" style={{ color: 'var(--color-success)' }}>✅ Solution &amp; Differentiation</h4>
          <p style={{ lineHeight: 1.6 }}>{content.solution}</p>
        </div>
      </div>

      <div className="master-grid">
        <div className="card-flat strategy-section" style={{ borderLeftColor: 'var(--color-secondary)' }}>
          <h4 className="strategy-title">💎 Business Value Drivers</h4>
          <ul className="strategy-list">{content.business_value.map((v, i) => (<li key={i}>{v}</li>))}</ul>
        </div>
        <div className="card-flat strategy-section" style={{ borderLeftColor: 'var(--color-warning)' }}>
          <h4 className="strategy-title">👤 Personas &amp; CTAs</h4>
          <div className="chip-container mb-md">{content.target_personas.map((p, i) => (<span key={i} className="chip">👤 {p}</span>))}</div>
          <div className="cta-box mb-sm"><span className="cta-tag cta-primary">Primary CTA</span><p className="cta-text">{content.cta.primary}</p></div>
          <div className="cta-box"><span className="cta-tag cta-secondary">Secondary CTA</span><p className="cta-text">{content.cta.secondary}</p></div>
        </div>
      </div>
    </div>
  );
};
