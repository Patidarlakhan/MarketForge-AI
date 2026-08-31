import client from './client';
import type { StrategyResponse } from '../types/strategy';

/**
 * Generate marketing strategy for a campaign.
 */
export async function generateStrategy(campaignId: string): Promise<StrategyResponse> {
  return client.post<StrategyResponse>(`/api/v1/campaigns/${campaignId}/strategy/generate`);
}

/**
 * Get stored marketing strategy for a campaign.
 */
export async function getStrategy(campaignId: string): Promise<StrategyResponse> {
  return client.get<StrategyResponse>(`/api/v1/campaigns/${campaignId}/strategy`);
}

/**
 * Regenerate marketing strategy for a campaign.
 */
export async function regenerateStrategy(campaignId: string): Promise<StrategyResponse> {
  return client.post<StrategyResponse>(`/api/v1/campaigns/${campaignId}/strategy/regenerate`);
}
