import { useState } from 'react';
import { Container, Center, Heading, VStack, Text } from '@chakra-ui/react';
import type { NextPage } from 'next';
import useSWR from 'swr';
import Analysis from '@/components/Analysis/Analysis';
import DriveChart from '@/components/DriveChart';
import Dropdown from '@/components/Dropdown';
import SiteTitle from '@/components/SiteTitle';
import { formatDate } from '@/utils/utils';
import { DriveData } from './api/driveData';

// 選択肢
const options = [
  { value: 1, name: '2022/9/7' },
  { value: 2, name: '2022/9/8' },
];

const Home: NextPage = () => {
  // 選択中のログファイル名
  const [fileIdx, setFileIdx] = useState(options[0].value);

  // データフェッチ
  const fetcher = (url: string) => fetch(url).then((res) => res.json());
  const params = new URLSearchParams({ fileIdx: String(fileIdx) });
  const { data, error, mutate } = useSWR<DriveData>(`/api/driveData?${params}`, fetcher);

  if (error) return <Center>Error loading data. Please reload.</Center>;
  if (!data) return <Center>Loading...</Center>;

  // 選択したデータの日付
  const date = formatDate(new Date(data.data[0].timestamp));

  return (
    <Container maxW={'8xl'} pt="5vh" pb={'10vh'}>
      <VStack as={'main'}>
        {/* サイトタイトル */}
        <SiteTitle />

        <Dropdown
          label="Select Drive Log:"
          options={options}
          value={fileIdx}
          setValue={setFileIdx}
        />

        <Heading as={'h2'} pb="1.5rem">
          Drive Report at {date}
        </Heading>

        <Analysis
          hardBrakingCount={data.hardBrakingCount}
          hardHandlingCount={data.hardHandlingCount}
        />

        <DriveChart data={data.data} />
        <Text>
          左右方向の揺れはハンドルの加減を示しています。グラフが大きく振れている箇所で急ハンドルが観測されます。
        </Text>
        <Text>
          速度変化は車体の航行速度の変化を示しています。グラフが大きく振れている箇所で急ブレーキが観測されます。
        </Text>
      </VStack>
    </Container>
  );
};

export default Home;
