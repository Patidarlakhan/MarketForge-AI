import React, { useState } from 'react';
import type { PlatformContentItem, LinkedInContent, TwitterContent, InstagramContent, BlogContent } from '../types/platformContent';
import { updatePlatformContent } from '../api/platformContent';
import { LinkedInView } from './platforms/LinkedInView';
import { TwitterView } from './platforms/TwitterView';
import { InstagramView } from './platforms/InstagramView';
import { BlogView } from './platforms/BlogView';

interface PlatformContentViewProps {
  platformItems: PlatformContentItem[];
  onRegenerateSingle: (platform: string) => void;
  regeneratingPlatform: string | null;
  onContentUpdated?: (updatedItem: PlatformContentItem) => void;
}

export const PlatformContentView: React.FC<PlatformContentViewProps> = ({
  platformItems,
  onRegenerateSingle,
  regeneratingPlatform,
  onContentUpdated,
}) => {
  const [activeTab, setActiveTab] = useState<string>('linkedin');
  const [editing, setEditing] = useState<boolean>(false);
  const [saving, setSaving] = useState<boolean>(false);
  const [editPostText, setEditPostText] = useState<string>('');

  const itemsMap: Record<string, PlatformContentItem> = {};
  platformItems.forEach((item) => { itemsMap[item.platform.toLowerCase()] = item; });

  const activeItem = itemsMap[activeTab];
  const isRegenerating = regeneratingPlatform === activeTab;

  const handleStartEdit = () => {
    if (!activeItem) return;
    setEditing(true);
    if (activeTab === 'linkedin') setEditPostText((activeItem.content as LinkedInContent).post_text || '');
    else if (activeTab === 'twitter') setEditPostText((activeItem.content as TwitterContent).single_post || '');
    else if (activeTab === 'instagram') setEditPostText((activeItem.content as InstagramContent).caption || '');
    else if (activeTab === 'blog') setEditPostText((activeItem.content as BlogContent).markdown_content || '');
  };

  const handleSaveEdit = async () => {
    if (!activeItem) return;
    try {
      setSaving(true);
      const newContent = { ...activeItem.content };
      if (activeTab === 'linkedin') (newContent as LinkedInContent).post_text = editPostText;
      else if (activeTab === 'twitter') (newContent as TwitterContent).single_post = editPostText;
      else if (activeTab === 'instagram') (newContent as InstagramContent).caption = editPostText;
      else if (activeTab === 'blog') (newContent as BlogContent).markdown_content = editPostText;
      const updated = await updatePlatformContent(activeItem.id, newContent);
      if (onContentUpdated) onContentUpdated(updated);
      setEditing(false);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to save edits');
    } finally { setSaving(false); }
  };

  const platformTabs = [
    { key: 'linkedin', icon: '💼', label: 'LinkedIn' },
    { key: 'twitter', icon: '𝕏', label: 'Twitter' },
    { key: 'instagram', icon: '📸', label: 'Insta' },
    { key: 'blog', icon: '📝', label: 'Blog' },
  ];

  const consolidatedCount = platformItems.length;

  return (
    <div className="animate-fade-in">
      <div className="platform-split">
        {/* Left: Content Preview */}
        <div className="platform-main">
          {/* Top action bar */}
          <div className="flex justify-between items-center mb-md" style={{ flexWrap: 'wrap', gap: '0.5rem' }}>
            <div className="preview-tabs">
              {!editing && activeItem && (
                <>
                  <button className="preview-tab active">Content Preview</button>
                  <button className="preview-tab" onClick={handleStartEdit}>✏️ Edit</button>
                </>
              )}
              {editing && (
                <>
                  <button className="preview-tab" onClick={() => setEditing(false)}>Content Preview</button>
                  <button className="preview-tab active">✏️ Editing</button>
                </>
              )}
            </div>
            <div className="flex gap-sm">
              <button onClick={() => onRegenerateSingle(activeTab)} disabled={isRegenerating || editing} className="btn btn-secondary btn-sm">
                {isRegenerating ? (<><div className="spinner"></div> Regenerating...</>) : `🔄 Regenerate ${activeTab.charAt(0).toUpperCase() + activeTab.slice(1)}`}
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="card" style={{ minHeight: '400px' }}>
            {editing ? (
              <div>
                <div className="form-group mb-md">
                  <textarea className="form-textarea" rows={20} value={editPostText} onChange={(e) => setEditPostText(e.target.value)} style={{ fontFamily: 'monospace', fontSize: 'var(--font-size-sm)' }} />
                </div>
                <div className="flex gap-sm justify-end">
                  <button onClick={() => setEditing(false)} className="btn btn-secondary">Cancel</button>
                  <button onClick={handleSaveEdit} disabled={saving} className="btn btn-primary">
                    {saving ? <div className="spinner"></div> : '💾 Save Changes'}
                  </button>
                </div>
              </div>
            ) : activeItem ? (
              <>
                {activeTab === 'linkedin' && <LinkedInView content={activeItem.content as LinkedInContent} />}
                {activeTab === 'twitter' && <TwitterView content={activeItem.content as TwitterContent} />}
                {activeTab === 'instagram' && <InstagramView content={activeItem.content as InstagramContent} />}
                {activeTab === 'blog' && <BlogView content={activeItem.content as BlogContent} />}
              </>
            ) : (
              <div className="text-center" style={{ padding: '4rem 0' }}>
                <p className="text-muted">No content for {activeTab}.</p>
              </div>
            )}
          </div>
        </div>

        {/* Right: Platform Sidebar */}
        <div className="platform-sidebar-panel">
          <div className="platform-sidebar-header">
            <h3>🔗 Platform Output</h3>
          </div>
          <div className="platform-sidebar-body">
            {/* Platform mini tabs */}
            <div className="platform-mini-tabs">
              {platformTabs.map((tab) => (
                <button
                  key={tab.key}
                  className={`platform-mini-tab ${activeTab === tab.key ? 'active' : ''}`}
                  onClick={() => { setActiveTab(tab.key); setEditing(false); }}
                >
                  {tab.icon} {tab.label}
                  {activeTab === tab.key && itemsMap[tab.key] && (
                    <span style={{ fontSize: '0.65rem', opacity: 0.7 }}>(Active v{itemsMap[tab.key].version})</span>
                  )}
                </button>
              ))}
            </div>

            <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--text-secondary)', marginBottom: 'var(--space-lg)' }}>
              Consolidated asset count: <strong style={{ color: 'var(--text-primary)' }}>{consolidatedCount}</strong>
              <button className="btn btn-secondary btn-sm" style={{ marginLeft: 'var(--space-sm)' }}>🔄 Regenerate-all</button>
            </div>

            {/* SEO Metadata — show for blog */}
            {activeTab === 'blog' && activeItem && (
              <div>
                <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: 'var(--space-md)', marginBottom: 'var(--space-lg)' }}>
                  <h4 style={{ fontSize: 'var(--font-size-sm)', fontWeight: 700, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: 'var(--space-md)' }}>
                    🎯 SEO Metadata
                  </h4>
                  <div className="flex justify-between items-center mb-md">
                    <div>
                      <span className="detail-label">SEO Health</span>
                    </div>
                    <div className="seo-gauge" style={{ background: 'var(--color-success-bg)', color: 'var(--color-success)' }}>
                      <div className="seo-gauge-inner">
                        <div className="seo-gauge-score">94</div>
                        <div className="seo-gauge-max">/100</div>
                      </div>
                    </div>
                  </div>

                  <div className="detail-group mb-md">
                    <span className="detail-label">URL Slug</span>
                    <input className="form-input" readOnly value={`/${(activeItem.content as BlogContent).slug}`} style={{ fontSize: 'var(--font-size-sm)', padding: '0.375rem 0.5rem' }} />
                  </div>

                  <div className="detail-group mb-md">
                    <div className="flex justify-between">
                      <span className="detail-label">Meta Description</span>
                      <span style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-tertiary)' }}>
                        {(activeItem.content as BlogContent).meta_description.length} characters
                      </span>
                    </div>
                    <div style={{ fontSize: 'var(--font-size-sm)', fontStyle: 'italic', color: 'var(--text-secondary)', background: 'var(--bg-tertiary)', padding: '0.5rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
                      "{(activeItem.content as BlogContent).meta_description}"
                    </div>
                  </div>

                  <div className="detail-group">
                    <span className="detail-label">Target Keywords</span>
                    <div className="chip-container">
                      {(activeItem.content as BlogContent).target_keywords.map((kw, i) => (
                        <span key={i} className="chip chip-success" style={{ fontSize: '0.7rem' }}>🔑 {kw} <span className="chip-remove" style={{ fontSize: '0.8rem' }}>×</span></span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Action History */}
            <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: 'var(--space-md)' }}>
              <h4 style={{ fontSize: 'var(--font-size-sm)', fontWeight: 700, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: 'var(--space-md)' }}>
                🕐 Action History &amp; Revisions
              </h4>
              {platformItems
                .filter(item => item.platform.toLowerCase() === activeTab)
                .map((item, idx) => (
                  <div key={idx} className="revision-item">
                    <div className="revision-dot" style={{ background: idx === 0 ? 'var(--color-primary)' : 'var(--text-muted)' }}></div>
                    <div>
                      <div className="revision-title">{item.platform} Content v{item.version}</div>
                      <div className="revision-meta">
                        {new Date(item.updated_at).toLocaleString()}
                      </div>
                    </div>
                  </div>
                ))
              }
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
