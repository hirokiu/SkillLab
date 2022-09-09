import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
} from 'recharts';
import { DriveData } from '@/pages/api/driveData';
import { formatTime } from '@/utils/utils';

type Props = {
  data: DriveData['data'];
};

const lineConfig = {
  dot: false,
  activeDot: { r: 5 },
};

const DriveChart: React.FC<Props> = ({ data }) => {
  const formattedData: DriveData['data'] = data.map((d) => ({
    ...d,
    timestamp: formatTime(new Date(d.timestamp)),
  }));

  return (
    <ResponsiveContainer width={'100%'} height={'100%'} minHeight={300}>
      <LineChart data={formattedData} width={500} height={500} margin={{ right: 30 }}>
        <XAxis dataKey="timestamp" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line
          {...lineConfig}
          name="左右方向の揺れ"
          type="monotone"
          dataKey="x"
          stroke="#8884d8"
        />
        <Line
          {...lineConfig}
          name="速度変化"
          type="monotone"
          dataKey="y"
          stroke="#82ca9d"
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default DriveChart;
