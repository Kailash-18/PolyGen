/**
 * Mesh Telemetry and Decimation Metrics Unit Tests
 * Author: Kailash-18
 */

export function testReductionCalculation() {
  const calcReduction = (before: number, after: number): string => {
    if (before <= 0) return '0.0%';
    const pct = ((before - after) / before) * 100;
    return `${pct.toFixed(1)}%`;
  };

  const res1 = calcReduction(10000, 5000);
  if (res1 !== '50.0%') throw new Error(`Expected 50.0%, got ${res1}`);

  const res2 = calcReduction(10000, 10000);
  if (res2 !== '0.0%') throw new Error(`Expected 0.0%, got ${res2}`);

  return true;
}

export function testNumberFormatting() {
  const formatNumber = (num: number): string => num.toLocaleString('en-US');
  if (formatNumber(12500) !== '12,500') throw new Error('Number formatting failed');
  return true;
}
