import React, { useState } from 'react';
import type { TwitterContent } from '../../types/platformContent';

interface TwitterViewProps { content: TwitterContent; }

export const TwitterView: React.FC<TwitterViewProps> = ({ content }) => {
  const [copiedSingle, setCopiedSingle] = useState(false);
  const [copiedThread, setCopiedThread] = useState(false);
  const handleCopySingle = () => { navigator.clipboard.writeText(content.single_post); setCopiedSingle(true); setTimeout(() => setCopiedSingle(false), 2000); };
  const handleCopyThread = () => { const t = content.thread.map(t => `${t.tweet_number}/ ${t.text}`).join('\n\n---\n\n'); navigator.clipboard.writeText(t); setCopiedThread(true); setTimeout(() => setCopiedThread(false), 2000); };

  const charCount = content.single_post.length;
  const pct = Math.min((charCount / 280) * 100, 100);

  return (
    <div className="animate-fade-in">
      <div className="flex justify-between items-center mb-md">
        <h3 style={{ fontSize: 'var(--font-size-base)', fontWeight: 700 }}>📌 Standalone Tweet</h3>
        <button onClick={handleCopySingle} className="btn btn-secondary btn-sm">{copiedSingle ? '✅ Copied!' : '📋 Copy'}</button>
      </div>
      <div className="post-preview-box mb-sm">
        <p style={{ fontSize: 'var(--font-size-lg)', lineHeight: 1.5 }}>{content.single_post}</p>
      </div>
      <div className="flex items-center mb-lg" style={{ gap: '0.75rem' }}>
        <div style={{ flex: 1, height: '4px', background: 'var(--bg-tertiary)', borderRadius: '2px', overflow: 'hidden' }}>
          <div style={{ height: '100%', width: `${pct}%`, background: charCount > 280 ? 'var(--color-error)' : 'var(--color-primary)', transition: 'width 0.3s' }}></div>
        </div>
        <span style={{ fontSize: 'var(--font-size-xs)', color: charCount > 280 ? 'var(--color-error)' : 'var(--text-tertiary)', fontWeight: 600 }}>{charCount}/280</span>
      </div>

      {content.thread && content.thread.length > 0 && (
        <div>
          <div className="flex justify-between items-center mb-md">
            <h3 style={{ fontSize: 'var(--font-size-base)', fontWeight: 700 }}>🧵 Thread ({content.thread.length} Tweets)</h3>
            <button onClick={handleCopyThread} className="btn btn-secondary btn-sm">{copiedThread ? '✅ Copied!' : '📋 Copy Thread'}</button>
          </div>
          <div className="flex flex-col gap-md">
            {content.thread.map((tweet, idx) => (
              <div key={idx} className="card-flat" style={{ padding: 'var(--space-md)' }}>
                <div className="flex justify-between items-center mb-xs">
                  <span className="badge badge-generating">{tweet.tweet_number}/{content.thread.length}</span>
                  <span style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-tertiary)' }}>{tweet.text.length} chars</span>
                </div>
                <p style={{ whiteSpace: 'pre-wrap', fontSize: 'var(--font-size-sm)', lineHeight: 1.5 }}>{tweet.text}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
