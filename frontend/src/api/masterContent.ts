import client from './client';
import type { MasterContentResponse } from '../types/masterContent';

/**
 * Generate platform-neutral master content for a campaign.
 */
export async function generateMasterContent(campaignId: string): Promise<MasterContentResponse> {
  return client.post<MasterContentResponse>(`/api/v1/campaigns/${campaignId}/master-content/generate`);
}

/**
 * Get stored master content for a campaign.
 */
export async function getMasterContent(campaignId: string): Promise<MasterContentResponse> {
  return client.get<MasterContentResponse>(`/api/v1/campaigns/${campaignId}/master-content`);
}

/**
 * Regenerate master content by master content ID.
 */
export async function regenerateMasterContent(masterContentId: string): Promise<MasterContentResponse> {
  return client.post<MasterContentResponse>(`/api/v1/master-content/${masterContentId}/regenerate`);
}
