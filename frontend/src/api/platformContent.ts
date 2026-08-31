import client from './client';
import type { PlatformContentItem } from '../types/platformContent';

/**
 * Generate all platform content in parallel.
 */
export async function generateAllPlatformContent(campaignId: string): Promise<PlatformContentItem[]> {
  return client.post<PlatformContentItem[]>(`/api/v1/campaigns/${campaignId}/platform-content/generate`);
}

/**
 * Get all generated platform content items for a campaign.
 */
export async function getAllPlatformContent(campaignId: string): Promise<PlatformContentItem[]> {
  return client.get<PlatformContentItem[]>(`/api/v1/campaigns/${campaignId}/platform-content`);
}

/**
 * Get content for a specific platform.
 */
export async function getSinglePlatformContent(campaignId: string, platform: string): Promise<PlatformContentItem> {
  return client.get<PlatformContentItem>(`/api/v1/campaigns/${campaignId}/platform-content/${platform}`);
}

/**
 * Independently regenerate single platform content.
 */
export async function regenerateSinglePlatformContent(campaignId: string, platform: string): Promise<PlatformContentItem> {
  return client.post<PlatformContentItem>(`/api/v1/campaigns/${campaignId}/platform-content/${platform}/regenerate`);
}

/**
 * Update platform content JSON payload by content ID.
 */
export async function updatePlatformContent(contentId: string, content: Record<string, any>): Promise<PlatformContentItem> {
  return client.put<PlatformContentItem>(`/api/v1/campaigns/platform-content/${contentId}`, { content });
}

