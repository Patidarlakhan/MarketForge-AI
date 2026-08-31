import React, { useState } from 'react';
import type { LinkedInContent } from '../../types/platformContent';

interface LinkedInViewProps { content: LinkedInContent; }

export const LinkedInView: React.FC<LinkedInViewProps> = ({ content }) => {
  const [copiedPost, setCopiedPost] = useState(false);
  const handleCopyPost = () => { navigator.clipboard.writeText(content.post_text); setCopiedPost(true); setTimeout(() => setCopiedPost(false), 2000); };

  return (
    <div className="animate-fade-in">
      <div className="flex justify-between items-center mb-md">
        <h3 style={{ fontSize: 'var(--font-size-base)', fontWeight: 700 }}>💼 LinkedIn Post</h3>
        <button onClick={handleCopyPost} className="btn btn-secondary btn-sm">{copiedPost ? '✅ Copied!' : '📋 Copy'}</button>
      </div>
      <div className="post-preview-box mb-lg">
        <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit', fontSize: 'var(--font-size-base)', lineHeight: 1.7 }}>{content.post_text}</pre>
      </div>

      {content.carousel_slides && content.carousel_slides.length > 0 && (
        <div>
          <h3 style={{ fontSize: 'var(--font-size-base)', fontWeight: 700, marginBottom: 'var(--space-md)' }}>📊 Carousel Script ({content.carousel_slides.length} Slides)</h3>
          <div className="carousel-grid">
            {content.carousel_slides.map((slide, idx) => (
              <div key={idx} className="carousel-slide-card">
                <span className="badge badge-generating mb-sm" style={{ display: 'inline-flex' }}>Slide {slide.slide_number}</span>
                <h4 style={{ fontSize: 'var(--font-size-base)', fontWeight: 700, marginBottom: '0.5rem' }}>{slide.header}</h4>
                <ul className="strategy-list">{slide.body_points.map((pt, pIdx) => (<li key={pIdx}>{pt}</li>))}</ul>
                {slide.visual_note && <div className="visual-note">💡 {slide.visual_note}</div>}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
