import React, { useState } from 'react';
import type { InstagramContent } from '../../types/platformContent';

interface InstagramViewProps { content: InstagramContent; }

export const InstagramView: React.FC<InstagramViewProps> = ({ content }) => {
  const [copiedCaption, setCopiedCaption] = useState(false);
  const [copiedPrompt, setCopiedPrompt] = useState(false);
  const handleCopyCaption = () => { navigator.clipboard.writeText(content.caption); setCopiedCaption(true); setTimeout(() => setCopiedCaption(false), 2000); };
  const handleCopyPrompt = () => { navigator.clipboard.writeText(content.image_prompt); setCopiedPrompt(true); setTimeout(() => setCopiedPrompt(false), 2000); };

  const renderCaption = (text: string) => {
    return text.split(/(#[a-zA-Z0-9_]+)/g).map((part, i) =>
      part.startsWith('#') ? <span key={i} style={{ color: 'var(--color-primary)', fontWeight: 500 }}>{part}</span> : part
    );
  };

  return (
    <div className="animate-fade-in">
      <div className="flex justify-between items-center mb-md">
        <h3 style={{ fontSize: 'var(--font-size-base)', fontWeight: 700 }}>📸 Instagram Caption</h3>
        <button onClick={handleCopyCaption} className="btn btn-secondary btn-sm">{copiedCaption ? '✅ Copied!' : '📋 Copy'}</button>
      </div>
      <div className="post-preview-box mb-lg">
        <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit', fontSize: 'var(--font-size-base)', lineHeight: 1.6 }}>{renderCaption(content.caption)}</pre>
      </div>

      <div className="flex justify-between items-center mb-md">
        <h3 style={{ fontSize: 'var(--font-size-base)', fontWeight: 700 }}>🖼️ AI Image Prompt</h3>
        <button onClick={handleCopyPrompt} className="btn btn-secondary btn-sm">{copiedPrompt ? '✅ Copied!' : '📋 Copy'}</button>
      </div>
      <div className="post-preview-box mb-lg" style={{ background: 'var(--bg-tertiary)' }}>
        <code style={{ color: 'var(--color-accent)', fontSize: 'var(--font-size-sm)', wordBreak: 'break-all', display: 'block', lineHeight: 1.6 }}>{content.image_prompt}</code>
      </div>

      {content.reel_script && content.reel_script.length > 0 && (
        <div>
          <h3 style={{ fontSize: 'var(--font-size-base)', fontWeight: 700, marginBottom: 'var(--space-md)' }}>🎬 Reel Script ({content.reel_script.length} Scenes)</h3>
          <div className="carousel-grid">
            {content.reel_script.map((scene, idx) => (
              <div key={idx} className="carousel-slide-card" style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
                <span className="badge badge-completed" style={{ display: 'inline-flex', alignSelf: 'flex-start' }}>Scene {scene.scene_number}</span>
                <div className="detail-group"><span className="detail-label">Visual</span><div style={{ fontSize: 'var(--font-size-sm)' }}>📹 {scene.visual_direction}</div></div>
                <div className="detail-group"><span className="detail-label">Audio</span><div style={{ fontSize: 'var(--font-size-sm)' }}>🎵 {scene.audio_cue}</div></div>
                <div className="detail-group" style={{ marginTop: 'auto', paddingTop: '0.5rem', borderTop: '1px solid var(--border-color)' }}>
                  <span className="detail-label">Copy</span><div style={{ fontSize: 'var(--font-size-sm)', fontWeight: 600, fontStyle: 'italic' }}>"{scene.spoken_text}"</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
