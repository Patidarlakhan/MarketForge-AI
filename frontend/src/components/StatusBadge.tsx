import React from 'react';
import type { CampaignStatus } from '../types/common';

interface StatusBadgeProps {
  status: CampaignStatus;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const getBadgeClass = (s: CampaignStatus) => {
    switch (s) {
      case 'completed':
      case 'master_content_generated':
      case 'strategy_generated':
        return 'badge-completed';
      case 'strategy_generation':
      case 'master_content_generation':
      case 'platform_content_generation':
        return 'badge-generating';
      case 'failed':
        return 'badge-failed';
      default:
        return 'badge-draft';
    }
  };

  const formatLabel = (s: string) => {
    return s.replace(/_/g, ' ').toUpperCase();
  };

  return (
    <span className={`badge ${getBadgeClass(status)}`}>
      {formatLabel(status)}
    </span>
  );
};
