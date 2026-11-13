import { CheckCircle2, Loader2, Sparkles, Box, Scissors, Compass } from 'lucide-react';
import type { ProgressUpdate } from '../types';

interface ProgressBarProps {
  progressData: ProgressUpdate | null;
}

const STAGES = [
  { step: 1, title: 'Geometry Synthesis', icon: Sparkles },
  { step: 2, title: 'QEM Decimation', icon: Scissors },
  { step: 3, title: 'UV Parameterization', icon: Compass },
  { step: 4, title: 'GLB Packaging', icon: Box }
];

export function ProgressBar({ progressData }: ProgressBarProps) {
  if (!progressData) return null;

  return (
    <div className="progress-banner">
      <div className="progress-header">
        <div className="flex items-center gap-2">
          {progressData.progress < 100 ? (
            <Loader2 className="w-4 h-4 animate-spin text-purple-400" />
          ) : (
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          )}
          <span className="progress-stage-title">{progressData.stage}</span>
        </div>
        <span className="progress-percentage">{progressData.progress}%</span>
      </div>

      <div className="progress-bar-track">
        <div
          className="progress-bar-fill"
          style={{ width: `${progressData.progress}%` }}
        />
      </div>

      <p className="progress-msg">{progressData.message}</p>

      {/* Steps visualization */}
      <div className="steps-row">
        {STAGES.map((s) => {
          const isDone = progressData.step > s.step || progressData.progress === 100;
          const isCurrent = progressData.step === s.step && progressData.progress < 100;
          const Icon = s.icon;

          return (
            <div
              key={s.step}
              className={`step-item ${isDone ? 'step-done' : isCurrent ? 'step-active' : 'step-pending'}`}
            >
              <div className="step-circle">
                {isDone ? <CheckCircle2 className="w-3.5 h-3.5" /> : <Icon className="w-3.5 h-3.5" />}
              </div>
              <span className="step-label">{s.title}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
