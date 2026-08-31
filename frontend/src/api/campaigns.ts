import client from './client';
import type { Campaign, CampaignCreateInput, CampaignUpdateInput } from '../types/campaign';

const BASE_PATH = '/api/v1/campaigns';

/**
 * Fetch all marketing campaigns.
 */
export async function listCampaigns(skip = 0, limit = 50): Promise<Campaign[]> {
  return client.get<Campaign[]>(`${BASE_PATH}?skip=${skip}&limit=${limit}`);
}

/**
 * Fetch a single campaign by ID.
 */
export async function getCampaign(id: string): Promise<Campaign> {
  return client.get<Campaign>(`${BASE_PATH}/${id}`);
}

/**
 * Create a new marketing campaign.
 */
export async function createCampaign(data: CampaignCreateInput): Promise<Campaign> {
  return client.post<Campaign>(BASE_PATH, data);
}

/**
 * Update an existing marketing campaign.
 */
export async function updateCampaign(id: string, data: CampaignUpdateInput): Promise<Campaign> {
  return client.patch<Campaign>(`${BASE_PATH}/${id}`, data);
}

/**
 * Delete a campaign.
 */
export async function deleteCampaign(id: string): Promise<void> {
  return client.del<void>(`${BASE_PATH}/${id}`);
}
