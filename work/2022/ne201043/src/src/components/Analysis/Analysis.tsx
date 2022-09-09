import { HStack } from '@chakra-ui/react';
import { IconCarCrash, IconSteeringWheel } from '@tabler/icons';
import EventCounts from './EventCounts';

type Props = {
  hardBrakingCount: number;
  hardHandlingCount: number;
};

const Analysis: React.FC<Props> = ({ hardBrakingCount, hardHandlingCount }) => {
  return (
    <HStack>
      <EventCounts
        label="急ブレーキ"
        count={hardBrakingCount}
        Icon={IconCarCrash}
        gradient={['#E70E02', '#EC7505']}
      />
      <EventCounts
        label="急ハンドル"
        count={hardHandlingCount}
        Icon={IconSteeringWheel}
        gradient={['#662C91', '#7888BD']}
      />
    </HStack>
  );
};

export default Analysis;
