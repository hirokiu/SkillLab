import { HStack, Heading } from '@chakra-ui/react';
import { IconCar } from '@tabler/icons';

const SiteTitle: React.FC = () => (
  <HStack mb={'7vh'}>
    <IconCar size={'6rem'} color="#a9a9a9" />
    <Heading as={'h1'} textAlign="center">
      Drive Score
    </Heading>
  </HStack>
);

export default SiteTitle;
