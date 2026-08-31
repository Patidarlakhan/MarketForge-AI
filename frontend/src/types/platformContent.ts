export interface LinkedInContent {
  post_text: string;
  carousel_slides: Array<{
    slide_number: number;
    header: string;
    body_points: string[];
    visual_note?: string;
  }>;
}

export interface TwitterContent {
  thread: Array<{
    tweet_number: number;
    text: string;
  }>;
  single_post: string;
}

export interface InstagramContent {
  caption: string;
  image_prompt: string;
  reel_script: Array<{
    scene_number: number;
    visual_direction: string;
    audio_cue: string;
    spoken_text: string;
  }>;
}

export interface BlogContent {
  title: string;
  meta_description: string;
  slug: string;
  target_keywords: string[];
  markdown_content: string;
}

export interface PlatformContentItem {
  id: string;
  campaign_id: string;
  platform: 'linkedin' | 'twitter' | 'instagram' | 'blog' | string;
  content: LinkedInContent | TwitterContent | InstagramContent | BlogContent | Record<string, any>;
  status: string;
  version: number;
  created_at: string;
  updated_at: string;
}
