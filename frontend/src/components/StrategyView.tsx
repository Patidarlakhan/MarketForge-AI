import React from 'react';
import type { StrategyContent } from '../types/strategy';

interface StrategyViewProps {
  strategy: StrategyContent;
  onRegenerate: () => void;
  regenerating: boolean;
}

export const StrategyView: React.FC<StrategyViewProps> = ({ strategy, onRegenerate, regenerating }) => {
  return (
    <div className="card animate-fade-in mb-xl">
      <div className="flex justify-between items-center mb-lg" style={{ flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: 'var(--font-size-xl)', fontWeight: 700 }}>🧠 Marketing Strategy Blueprint</h2>
          <p className="text-muted" style={{ fontSize: 'var(--font-size-sm)' }}>Formulated by StrategyAgent based on your campaign brief</p>
        </div>
        <button onClick={onRegenerate} disabled={regenerating} className="btn btn-secondary">
          {regenerating ? (<><div className="spinner"></div> Regenerating...</>) : '🔄 Regenerate Strategy'}
        </button>
      </div>

      <div className="strategy-grid">
        <div className="strategy-section">
          <h3 className="strategy-title">💡 Audience Insights</h3>
          <ul className="strategy-list">{strategy.audience_insights.map((insight, idx) => (<li key={idx}>{insight}</li>))}</ul>
        </div>
        <div className="strategy-section" style={{ borderLeftColor: 'var(--color-secondary)' }}>
          <h3 className="strategy-title">🏛️ Content Pillars</h3>
          <ul className="strategy-list">{strategy.content_pillars.map((p, idx) => (<li key={idx}><strong>Pillar {idx + 1}:</strong> {p}</li>))}</ul>
        </div>
        <div className="strategy-section" style={{ borderLeftColor: 'var(--color-accent)' }}>
          <h3 className="strategy-title">📢 Key Messages</h3>
          <ul className="strategy-list">{strategy.key_messages.map((msg, idx) => (<li key={idx} style={{ fontStyle: 'italic' }}>"{msg}"</li>))}</ul>
        </div>
        <div className="strategy-section" style={{ borderLeftColor: 'var(--color-success)' }}>
          <h3 className="strategy-title">📌 Content Topics</h3>
          <ul className="strategy-list">{strategy.topics.map((t, idx) => (<li key={idx}>{t}</li>))}</ul>
        </div>
        <div className="strategy-section" style={{ borderLeftColor: 'var(--color-warning)' }}>
          <h3 className="strategy-title">📐 Positioning Angles</h3>
          <ul className="strategy-list">{strategy.content_angles.map((a, idx) => (<li key={idx}>{a}</li>))}</ul>
        </div>
        <div className="strategy-section" style={{ borderLeftColor: 'var(--color-error)' }}>
          <h3 className="strategy-title">📣 Call-to-Actions</h3>
          <div className="cta-box mb-sm">
            <span className="cta-tag cta-primary">Primary CTA</span>
            <p className="cta-text">{strategy.cta.primary}</p>
          </div>
          <div className="cta-box">
            <span className="cta-tag cta-secondary">Secondary CTA</span>
            <p className="cta-text">{strategy.cta.secondary}</p>
          </div>
        </div>
      </div>
    </div>
  );
};
