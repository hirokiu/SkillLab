import { memo } from 'react';
import { Box, Heading, Text } from '@chakra-ui/react';
import { TablerIconProps } from '@tabler/icons';

type Props = {
  label: string;
  count: number;
  Icon: React.FC<TablerIconProps>;
  gradient: [string, string];
};

const EventCounts: React.FC<Props> = ({ label, count, Icon, gradient }) => {
  return (
    <Box
      p={'2rem'}
      borderRadius={'2xl'}
      textColor={'white'}
      bgGradient={`linear(to-br, ${gradient[0]}, ${gradient[1]})`}
    >
      <Icon size={'5rem'} />
      <Heading as={'h2'} fontSize="3xl" fontWeight={'medium'}>
        {label}の回数
      </Heading>
      <Text fontSize={'7xl'} fontWeight="bold">
        {count}
      </Text>
    </Box>
  );
};

export default memo(EventCounts);
