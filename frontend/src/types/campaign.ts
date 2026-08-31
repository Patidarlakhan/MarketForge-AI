import type { CampaignStatus } from './common';

export interface Campaign {
  id: string;
  name: string;
  objective: string;
  industry: string;
  product_service: string;
  target_audience: string;
  target_personas: string[];
  pain_points: string[];
  offer?: string | null;
  landing_page?: string | null;
  brand_info?: string | null;
  tone: string;
  status: CampaignStatus;
  created_at: string;
  updated_at: string;
}

export interface CampaignCreateInput {
  name: string;
  objective: string;
  industry: string;
  product_service: string;
  target_audience: string;
  target_personas: string[];
  pain_points: string[];
  offer?: string;
  landing_page?: string;
  brand_info?: string;
  tone: string;
}

export interface CampaignUpdateInput {
  name?: string;
  objective?: string;
  industry?: string;
  product_service?: string;
  target_audience?: string;
  target_personas?: string[];
  pain_points?: string[];
  offer?: string;
  landing_page?: string;
  brand_info?: string;
  tone?: string;
  status?: CampaignStatus;
}
