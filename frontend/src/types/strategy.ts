export interface CallToAction {
  primary: string;
  secondary: string;
}

export interface StrategyContent {
  audience_insights: string[];
  content_pillars: string[];
  key_messages: string[];
  topics: string[];
  content_angles: string[];
  cta: CallToAction;
}

export interface StrategyResponse {
  id: string;
  campaign_id: string;
  content: StrategyContent;
  status: string;
  created_at: string;
  updated_at: string;
}
