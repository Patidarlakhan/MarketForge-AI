import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getCampaign } from '../api/campaigns';
import { generateStrategy, getStrategy, regenerateStrategy } from '../api/strategies';
import { generateMasterContent, getMasterContent, regenerateMasterContent } from '../api/masterContent';
import {
  generateAllPlatformContent,
  getAllPlatformContent,
  regenerateSinglePlatformContent,
} from '../api/platformContent';
import type { Campaign } from '../types/campaign';
import type { StrategyContent } from '../types/strategy';
import type { MasterContentResponse } from '../types/masterContent';
import type { PlatformContentItem } from '../types/platformContent';
import { StatusBadge } from '../components/StatusBadge';
import { StrategyView } from '../components/StrategyView';
import { MasterContentView } from '../components/MasterContentView';
import { PlatformContentView } from '../components/PlatformContentView';

type DetailTab = 'brief' | 'strategy' | 'master' | 'platform';

export const CampaignDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [campaign, setCampaign] = useState<Campaign | null>(null);
  const [strategy, setStrategy] = useState<StrategyContent | null>(null);
  const [masterContent, setMasterContent] = useState<MasterContentResponse | null>(null);
  const [platformContents, setPlatformContents] = useState<PlatformContentItem[]>([]);

  const [activeTab, setActiveTab] = useState<DetailTab>('brief');

  const [loading, setLoading] = useState<boolean>(true);
  const [generatingStrategy, setGeneratingStrategy] = useState<boolean>(false);
  const [generatingMasterContent, setGeneratingMasterContent] = useState<boolean>(false);
  const [generatingPlatformContent, setGeneratingPlatformContent] = useState<boolean>(false);
  const [regeneratingPlatform, setRegeneratingPlatform] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      loadData(id);
    }
  }, [id]);

  const loadData = async (campaignId: string) => {
    try {
      setLoading(true);
      setError(null);

      // Fetch campaign details
      const cData = await getCampaign(campaignId);
      setCampaign(cData);

      // Try fetching existing strategy
      try {
        const sData = await getStrategy(campaignId);
        if (sData && sData.content) {
          setStrategy(sData.content);
        }
      } catch {
        setStrategy(null);
      }

      // Try fetching existing master content
      try {
        const mcData = await getMasterContent(campaignId);
        if (mcData && mcData.content) {
          setMasterContent(mcData);
        }
      } catch {
        setMasterContent(null);
      }

      // Try fetching existing platform content items
      try {
        const pcData = await getAllPlatformContent(campaignId);
        if (pcData && pcData.length > 0) {
          setPlatformContents(pcData);
        }
      } catch {
        setPlatformContents([]);
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to load campaign data');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateStrategy = async () => {
    if (!id) return;
    try {
      setGeneratingStrategy(true);
      setError(null);

      const res = await generateStrategy(id);
      setStrategy(res.content);

      const updatedCampaign = await getCampaign(id);
      setCampaign(updatedCampaign);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to generate strategy');
    } finally {
      setGeneratingStrategy(false);
    }
  };

  const handleRegenerateStrategy = async () => {
    if (!id) return;
    try {
      setGeneratingStrategy(true);
      setError(null);

      const res = await regenerateStrategy(id);
      setStrategy(res.content);

      const updatedCampaign = await getCampaign(id);
      setCampaign(updatedCampaign);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to regenerate strategy');
    } finally {
      setGeneratingStrategy(false);
    }
  };

  const handleGenerateMasterContent = async () => {
    if (!id) return;
    try {
      setGeneratingMasterContent(true);
      setError(null);

      const res = await generateMasterContent(id);
      setMasterContent(res);

      const updatedCampaign = await getCampaign(id);
      setCampaign(updatedCampaign);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to generate master content');
    } finally {
      setGeneratingMasterContent(false);
    }
  };

  const handleRegenerateMasterContent = async () => {
    if (!masterContent) return;
    try {
      setGeneratingMasterContent(true);
      setError(null);

      const res = await regenerateMasterContent(masterContent.id);
      setMasterContent(res);

      if (id) {
        const updatedCampaign = await getCampaign(id);
        setCampaign(updatedCampaign);
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to regenerate master content');
    } finally {
      setGeneratingMasterContent(false);
    }
  };

  const handleGeneratePlatformContent = async () => {
    if (!id) return;
    try {
      setGeneratingPlatformContent(true);
      setError(null);

      const res = await generateAllPlatformContent(id);
      setPlatformContents(res);

      const updatedCampaign = await getCampaign(id);
      setCampaign(updatedCampaign);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to generate platform content');
    } finally {
      setGeneratingPlatformContent(false);
    }
  };

  const handleRegenerateSinglePlatform = async (platform: string) => {
    if (!id) return;
    try {
      setRegeneratingPlatform(platform);
      setError(null);

      const updatedItem = await regenerateSinglePlatformContent(id, platform);
      setPlatformContents((prev) =>
        prev.map((item) => (item.platform.toLowerCase() === platform.toLowerCase() ? updatedItem : item))
      );
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : `Failed to regenerate ${platform} content`);
    } finally {
      setRegeneratingPlatform(null);
    }
  };

  if (loading) {
    return (
      <div className="app-main text-center" style={{ padding: '6rem 0' }}>
        <div className="spinner spinner-lg" style={{ margin: '0 auto var(--space-md)' }}></div>
        <p className="text-muted">Loading campaign details...</p>
      </div>
    );
  }

  if (error && !campaign) {
    return (
      <div className="app-main" style={{ maxWidth: '600px', margin: '4rem auto', textAlign: 'center' }}>
        <div className="card" style={{ borderColor: 'var(--color-error)' }}>
          <p style={{ color: 'var(--color-error)', fontWeight: 600 }}>⚠️ {error}</p>
          <Link to="/" className="btn btn-secondary mt-lg">
            ← Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  if (!campaign) return null;

  // Tab configuration
  const tabs: { key: DetailTab; label: string; icon: string; ready: boolean }[] = [
    { key: 'brief', label: '1. Brief', icon: '📋', ready: true },
    { key: 'strategy', label: '2. Strategy', icon: '⚙️', ready: !!strategy },
    { key: 'master', label: '3. Master', icon: '☑️', ready: !!masterContent },
    { key: 'platform', label: '4. Platform Suite', icon: '🔗', ready: platformContents.length > 0 },
  ];

  // Find the next step that needs action
  const nextAction: DetailTab | null = !strategy
    ? 'strategy'
    : !masterContent
    ? 'master'
    : platformContents.length === 0
    ? 'platform'
    : null;

  const renderBriefTab = () => (
    <div className="animate-fade-in">
      <div className="card brief-card">
        <div className="flex items-center gap-sm" style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: 'var(--space-md)' }}>
          <div style={{ fontSize: '1.5rem' }}>📋</div>
          <h2 className="section-heading" style={{ border: 'none', padding: 0, margin: 0 }}>Campaign Brief</h2>
        </div>

        <div className="detail-grid" style={{ marginTop: 'var(--space-xl)' }}>
          <div className="detail-group">
            <span className="detail-label">Objective</span>
            <div className="detail-value">{campaign.objective}</div>
          </div>

          <div className="detail-group">
            <span className="detail-label">Industry &amp; Tone</span>
            <div className="flex gap-xs" style={{ flexWrap: 'wrap' }}>
              <span className="chip" style={{ padding: '0.15rem 0.5rem', fontSize: 'var(--font-size-xs)' }}>🏢 {campaign.industry}</span>
              <span className="chip" style={{ padding: '0.15rem 0.5rem', fontSize: 'var(--font-size-xs)' }}>🗣️ {campaign.tone}</span>
            </div>
          </div>

          <div className="detail-group" style={{ gridColumn: '1 / -1' }}>
            <span className="detail-label">Product / Service</span>
            <div className="detail-value" style={{ padding: '1rem', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
              {campaign.product_service}
            </div>
          </div>

          <div className="detail-group" style={{ gridColumn: '1 / -1' }}>
            <span className="detail-label">Target Audience</span>
            <div className="detail-value">{campaign.target_audience}</div>
          </div>

          {campaign.target_personas && campaign.target_personas.length > 0 && (
            <div className="detail-group" style={{ gridColumn: '1 / -1' }}>
              <span className="detail-label">Target Personas</span>
              <div className="chip-container">
                {campaign.target_personas.map((p, idx) => (
                  <span key={idx} className="chip">
                    👤 {p}
                  </span>
                ))}
              </div>
            </div>
          )}

          {campaign.pain_points && campaign.pain_points.length > 0 && (
            <div className="detail-group" style={{ gridColumn: '1 / -1' }}>
              <span className="detail-label">Customer Pain Points</span>
              <div className="chip-container">
                {campaign.pain_points.map((pt, idx) => (
                  <span key={idx} className="chip chip-warning">
                    ⚡ {pt}
                  </span>
                ))}
              </div>
            </div>
          )}

          {campaign.offer && (
            <div className="detail-group">
              <span className="detail-label">Offer / Lead Magnet</span>
              <div className="detail-value">🎁 {campaign.offer}</div>
            </div>
          )}

          {campaign.landing_page && (
            <div className="detail-group">
              <span className="detail-label">Landing Page</span>
              <div className="detail-value">
                <a href={campaign.landing_page} target="_blank" rel="noreferrer" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}>
                  🔗 {campaign.landing_page}
                </a>
              </div>
            </div>
          )}

          {campaign.brand_info && (
            <div className="detail-group" style={{ gridColumn: '1 / -1' }}>
              <span className="detail-label">Brand Guidelines</span>
              <div className="detail-value" style={{ fontStyle: 'italic', color: 'var(--text-secondary)', padding: '1rem', borderLeft: '3px solid var(--border-color)' }}>
                "{campaign.brand_info}"
              </div>
            </div>
          )}
        </div>

        {/* Show next action CTA inside the brief tab */}
        {nextAction === 'strategy' && (
          <div style={{ marginTop: 'var(--space-2xl)', borderTop: '1px solid var(--border-color)', paddingTop: 'var(--space-xl)', textAlign: 'center' }}>
            <p className="text-muted mb-md">Ready to generate your AI marketing strategy?</p>
            <button
              onClick={handleGenerateStrategy}
              disabled={generatingStrategy}
              className="btn btn-primary"
              style={{ padding: '0.875rem 2rem' }}
            >
              {generatingStrategy ? (
                <>
                  <div className="spinner"></div> Generating AI Strategy...
                </>
              ) : (
                '🚀 Generate AI Strategy'
              )}
            </button>
          </div>
        )}
      </div>
    </div>
  );

  const renderStrategyTab = () => {
    if (!strategy) {
      return (
        <div className="card text-center animate-fade-in" style={{ padding: '4rem 2rem' }}>
          <div style={{ fontSize: '4rem', marginBottom: '1rem', opacity: 0.6 }}>🧠</div>
          <h3 style={{ fontSize: 'var(--font-size-xl)', fontWeight: 700, marginBottom: '0.5rem' }}>
            Strategy Not Generated Yet
          </h3>
          <p className="text-muted" style={{ maxWidth: '500px', margin: '0 auto 2rem' }}>
            The AI Strategy Agent will analyze your campaign brief, target personas, and pain points to produce positioning angles, audience insights, content pillars, and call-to-actions.
          </p>
          <button
            onClick={handleGenerateStrategy}
            disabled={generatingStrategy}
            className="btn btn-primary"
            style={{ padding: '0.875rem 2rem' }}
          >
            {generatingStrategy ? (
              <>
                <div className="spinner"></div> Generating AI Strategy...
              </>
            ) : (
              '🚀 Generate AI Strategy'
            )}
          </button>
        </div>
      );
    }

    return (
      <div className="animate-fade-in">
        <StrategyView
          strategy={strategy}
          onRegenerate={handleRegenerateStrategy}
          regenerating={generatingStrategy}
        />

        {/* Show next action CTA */}
        {nextAction === 'master' && (
          <div className="card text-center" style={{ padding: 'var(--space-xl)', borderTop: '4px solid var(--color-accent)' }}>
            <p className="text-muted mb-md">Strategy is ready! Continue to Master Content.</p>
            <button
              onClick={() => { setActiveTab('master'); }}
              className="btn btn-primary"
              style={{ padding: '0.875rem 2rem' }}
            >
              Continue to Master Content →
            </button>
          </div>
        )}
      </div>
    );
  };

  const renderMasterTab = () => {
    if (!masterContent || !masterContent.content) {
      return (
        <div className="card text-center animate-fade-in" style={{ padding: '4rem 2rem' }}>
          <div style={{ fontSize: '4rem', marginBottom: '1rem', opacity: 0.6 }}>✍️</div>
          <h3 style={{ fontSize: 'var(--font-size-xl)', fontWeight: 700, marginBottom: '0.5rem' }}>
            Master Content Not Generated Yet
          </h3>
          <p className="text-muted" style={{ maxWidth: '500px', margin: '0 auto 2rem' }}>
            {strategy
              ? 'Strategy generated! The Master Content Agent will synthesize the campaign brief and strategy into a single platform-neutral core narrative.'
              : 'You need to generate a Marketing Strategy first before creating Master Content.'}
          </p>
          <button
            onClick={strategy ? handleGenerateMasterContent : () => setActiveTab('strategy')}
            disabled={generatingMasterContent}
            className="btn btn-primary"
            style={{ padding: '0.875rem 2rem' }}
          >
            {!strategy ? (
              '🧠 Go to Strategy First'
            ) : generatingMasterContent ? (
              <>
                <div className="spinner"></div> Generating Master Content...
              </>
            ) : (
              '✨ Generate Master Content'
            )}
          </button>
        </div>
      );
    }

    return (
      <div className="animate-fade-in">
        <MasterContentView
          content={masterContent.content}
          onRegenerate={handleRegenerateMasterContent}
          regenerating={generatingMasterContent}
        />

        {/* Show next action CTA */}
        {nextAction === 'platform' && (
          <div className="card text-center" style={{ padding: 'var(--space-xl)', borderTop: '4px solid var(--color-success)' }}>
            <p className="text-muted mb-md">Master Content is ready! Generate platform-specific content.</p>
            <button
              onClick={() => { setActiveTab('platform'); }}
              className="btn btn-primary"
              style={{ padding: '0.875rem 2rem' }}
            >
              Continue to Platform Content →
            </button>
          </div>
        )}
      </div>
    );
  };

  const renderPlatformTab = () => {
    if (platformContents.length === 0) {
      return (
        <div className="card text-center animate-fade-in" style={{ padding: '4rem 2rem' }}>
          <div style={{ fontSize: '4rem', marginBottom: '1rem', opacity: 0.6 }}>📱</div>
          <h3 style={{ fontSize: 'var(--font-size-xl)', fontWeight: 700, marginBottom: '0.5rem' }}>
            Platform Content Not Generated Yet
          </h3>
          <p className="text-muted" style={{ maxWidth: '500px', margin: '0 auto 2rem' }}>
            {masterContent
              ? 'Master Content generated! Specialized platform generators (LinkedIn, X/Twitter, Instagram, Blog) will generate multi-channel posts in parallel.'
              : 'You need to generate Master Content first before creating Platform Content.'}
          </p>
          <button
            onClick={masterContent ? handleGeneratePlatformContent : () => setActiveTab('master')}
            disabled={generatingPlatformContent}
            className="btn btn-primary"
            style={{ padding: '0.875rem 2rem' }}
          >
            {!masterContent ? (
              '✍️ Go to Master Content First'
            ) : generatingPlatformContent ? (
              <>
                <div className="spinner"></div> Generating Platform Assets...
              </>
            ) : (
              '⚡ Generate All Platform Content'
            )}
          </button>
        </div>
      );
    }

    return (
      <div className="animate-fade-in">
        <PlatformContentView
          platformItems={platformContents}
          onRegenerateSingle={handleRegenerateSinglePlatform}
          regeneratingPlatform={regeneratingPlatform}
        />
      </div>
    );
  };

  return (
    <div className="app-main animate-fade-in">
      {/* Top Navigation */}
      <div className="mb-lg">
        <Link to="/" className="btn btn-ghost" style={{ padding: '0.25rem 0.5rem', marginLeft: '-0.5rem' }}>
          ← Back to Campaigns
        </Link>
      </div>

      {/* Header */}
      <div className="page-header flex justify-between items-center" style={{ flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div className="flex items-center gap-md mb-sm">
            <StatusBadge status={campaign.status} />
            <span style={{ color: 'var(--text-tertiary)', fontSize: 'var(--font-size-sm)', fontWeight: 500 }}>
              Created: {new Date(campaign.created_at).toLocaleString()}
            </span>
          </div>
          <h1 style={{ marginBottom: 0 }}>{campaign.name}</h1>
        </div>
      </div>

      {/* Workflow Stepper — Now clickable tabs */}
      <div className="card mb-xl" style={{ padding: 0, overflow: 'hidden' }}>
        <div className="detail-tabs">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              className={`detail-tab-btn ${activeTab === tab.key ? 'active' : ''} ${tab.ready ? 'ready' : ''}`}
              onClick={() => setActiveTab(tab.key)}
            >
              <span className="detail-tab-icon">
                {tab.ready ? '✓' : tab.icon}
              </span>
              <span className="detail-tab-label">{tab.label}</span>
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="card mb-lg" style={{ borderColor: 'var(--color-error)', backgroundColor: 'rgba(239, 68, 68, 0.05)' }}>
          <p style={{ color: 'var(--color-error)', fontWeight: 600 }}>⚠️ {error}</p>
        </div>
      )}

      {/* Tab Content */}
      <div>
        {activeTab === 'brief' && renderBriefTab()}
        {activeTab === 'strategy' && renderStrategyTab()}
        {activeTab === 'master' && renderMasterTab()}
        {activeTab === 'platform' && renderPlatformTab()}
      </div>
    </div>
  );
};
