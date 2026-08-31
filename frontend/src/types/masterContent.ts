import type { CallToAction } from './strategy';

export interface MasterContentOutput {
  title: string;
  core_idea: string;
  problem: string;
  solution: string;
  business_value: string[];
  target_personas: string[];
  key_message: string;
  cta: CallToAction;
}

export interface MasterContentResponse {
  id: string;
  campaign_id: string;
  content: MasterContentOutput;
  status: string;
  created_at: string;
  updated_at: string;
}
