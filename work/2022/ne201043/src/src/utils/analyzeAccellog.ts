import { hardBrakingBasis, hardHandlingBasis } from '@/constants';
import { Accellog } from '@/pages/api/driveData';

// グラフ描画用にデータを整形
export const arrangeDriveData = (accellog: Accellog) =>
  accellog.x.map((x, idx) => ({
    x,
    y: accellog.y[idx],
    timestamp: accellog.timestamp[idx],
  }));

// 急ブレーキの回数を算出
export const countHardBraking = (y: number[]): number => {
  return y.filter((v, idx) => {
    if (idx < 2) return false;
    if (Math.abs(v - y[idx - 1]) > hardBrakingBasis) return true;
  }).length;
};

// 急ハンドルの回数を算出
export const countHardHandling = (x: number[]): number => {
  return x.filter((v, idx) => {
    if (idx < 2) return false;
    if (Math.abs(v - x[idx - 1]) > hardHandlingBasis) return true;
  }).length;
};
