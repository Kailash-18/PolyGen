import { CheckCircle2, Loader2, Sparkles, Box, Scissors, Compass, Paintbrush } from 'lucide-react';
import type { ProgressUpdate } from '../types';

interface ProgressBarProps {
  progressData: ProgressUpdate | null;
}

const STAGES = [
  { step: 1, title: 'Geometry', icon: Sparkles },
  { step: 2, title: 'Decimation', icon: Scissors },
  { step: 3, title: 'UV Mapping', icon: Compass },
  { step: 4, title: 'PBR Texturing', icon: Paintbrush },
  { step: 5, title: 'Packaging', icon: Box }
];

export function ProgressBar({ progressData }: ProgressBarProps) {
  if (!progressData) return null;

  const isComplete = progressData.progress >= 100;

  return (
    <div className={`floating-pipeline-hud ${isComplete ? 'complete' : ''}`}>
      <div className="pipeline-hud-top">
        <div className="flex items-center gap-2">
          {isComplete ? (
            <div className="status-badge-circle complete">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
            </div>
          ) : (
            <div className="status-badge-circle running">
              <Loader2 className="w-3.5 h-3.5 text-indigo-400 animate-spin" />
            </div>
          )}
          <span className="pipeline-stage-title font-semibold text-xs text-slate-100">
            {progressData.stage}
          </span>
        </div>
        <span className="font-mono text-xs font-bold text-indigo-300">
          {progressData.progress}%
        </span>
      </div>

      {/* Progress track */}
      <div className="pipeline-track">
        <div
          className="pipeline-fill"
          style={{ width: `${progressData.progress}%` }}
        />
      </div>

      {/* Message */}
      <p className="pipeline-message text-[11px] text-slate-400 truncate">
        {progressData.message}
      </p>

      {/* Micro Stage Pills */}
      <div className="pipeline-steps-chips">
        {STAGES.map((s) => {
          const isDone = progressData.step > s.step || isComplete;
          const isCurrent = progressData.step === s.step && !isComplete;
          const Icon = s.icon;

          return (
            <div
              key={s.step}
              className={`pipeline-step-chip ${isDone ? 'done' : isCurrent ? 'active' : 'pending'}`}
            >
              <Icon className="w-2.5 h-2.5" />
              <span>{s.title}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
