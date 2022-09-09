import type { NextApiRequest, NextApiResponse } from 'next';
import accellog1 from '@/assets/json/accellog_20220907.json';
import accellog2 from '@/assets/json/accellog_20220908.json';
import {
  arrangeDriveData,
  countHardBraking,
  countHardHandling,
} from '@/utils/analyzeAccellog';

// JSONの型
export type Accellog = {
  x: number[];
  y: number[];
  timestamp: string[];
};

// ドライブログとして整形後の型
export type DriveData = {
  // 生データ
  data: {
    x: number;
    y: number;
    timestamp: string;
  }[];
  // 急ブレーキの回数
  hardBrakingCount: number;
  // 急ハンドルの回数
  hardHandlingCount: number;
};

// AccellogをDriveDataに変換する
const getDriveData = (accellog: Accellog): DriveData => {
  return {
    data: arrangeDriveData(accellog),
    hardBrakingCount: countHardBraking(accellog.y),
    hardHandlingCount: countHardHandling(accellog.x),
  };
};

export default function handler(req: NextApiRequest, res: NextApiResponse<DriveData>) {
  // クエリ読み取り
  const fileIdx = req.query['fileIdx'];

  if (fileIdx === '1') {
    const data = getDriveData(accellog1);
    res.status(200).json(data);
  } else {
    const data = getDriveData(accellog2);
    res.status(200).json(data);
  }
}
