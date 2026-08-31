/**
 * Common TypeScript types used across the application.
 */

/** API error response */
export interface ApiError {
  detail: string;
  status_code?: number;
}

/** Generation status enum */
export type GenerationStatus = 'pending' | 'generating' | 'completed' | 'failed';

/** Campaign status enum */
export type CampaignStatus =
  | 'draft'
  | 'strategy_generation'
  | 'strategy_generated'
  | 'master_content_generation'
  | 'master_content_generated'
  | 'platform_content_generation'
  | 'completed'
  | 'failed';

/** Platform types */
export type Platform = 'linkedin' | 'x' | 'instagram' | 'blog';
