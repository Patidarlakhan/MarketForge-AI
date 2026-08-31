import React, { useState, useMemo } from 'react';
import type { BlogContent } from '../../types/platformContent';

interface BlogViewProps { content: BlogContent; }

// Simple markdown to HTML renderer
function renderMarkdownToHTML(md: string): string {
  let html = md
    // Headers
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    // Bold
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    // Italic
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    // Bullet lists
    .replace(/^[•\-\*] (.+)$/gm, '<li>$1</li>')
    // Code inline
    .replace(/`(.+?)`/g, '<code>$1</code>');

  // Wrap consecutive <li> in <ul>
  html = html.replace(/((?:<li>.*<\/li>\n?)+)/g, '<ul>$1</ul>');
  // Wrap remaining plain text lines as paragraphs (skip empty lines and already-tagged)
  html = html.split('\n').map(line => {
    const trimmed = line.trim();
    if (!trimmed) return '';
    if (trimmed.startsWith('<')) return line;
    return `<p>${trimmed}</p>`;
  }).join('\n');

  return html;
}

export const BlogView: React.FC<BlogViewProps> = ({ content }) => {
  const [viewMode, setViewMode] = useState<'rendered' | 'raw'>('rendered');
  const [copiedMarkdown, setCopiedMarkdown] = useState(false);

  const handleCopyMarkdown = () => {
    navigator.clipboard.writeText(content.markdown_content);
    setCopiedMarkdown(true);
    setTimeout(() => setCopiedMarkdown(false), 2000);
  };

  const renderedHTML = useMemo(() => renderMarkdownToHTML(content.markdown_content), [content.markdown_content]);

  return (
    <div className="animate-fade-in">
      {/* Toggle bar */}
      <div className="flex justify-between items-center mb-md" style={{ flexWrap: 'wrap', gap: '0.5rem' }}>
        <div className="preview-tabs">
          <button className={`preview-tab ${viewMode === 'rendered' ? 'active' : ''}`} onClick={() => setViewMode('rendered')}>
            Rendered Preview
          </button>
          <button className={`preview-tab ${viewMode === 'raw' ? 'active' : ''}`} onClick={() => setViewMode('raw')}>
            Raw Markdown
          </button>
        </div>
        <div className="flex gap-sm">
          <button onClick={handleCopyMarkdown} className="btn btn-secondary btn-sm">
            {copiedMarkdown ? '✅ Copied!' : '📋 Copy Markdown'}
          </button>
        </div>
      </div>

      {/* Content */}
      {viewMode === 'rendered' ? (
        <div className="rendered-markdown" dangerouslySetInnerHTML={{ __html: renderedHTML }} />
      ) : (
        <div className="post-preview-box" style={{ maxHeight: '700px', overflowY: 'auto' }}>
          <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace', fontSize: 'var(--font-size-sm)', lineHeight: 1.7, color: 'var(--text-secondary)' }}>
            {content.markdown_content}
          </pre>
        </div>
      )}
    </div>
  );
};
