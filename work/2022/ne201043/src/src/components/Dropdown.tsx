import { Dispatch, memo, SetStateAction } from 'react';
import { HStack, Select, Text } from '@chakra-ui/react';

type Props = {
  label: string;
  options: { value: number; name: string }[];
  value: number;
  setValue: Dispatch<SetStateAction<number>>;
};

const Dropdown: React.FC<Props> = ({ label, options, value, setValue }) => (
  <HStack pb={'5vh'}>
    <Text whiteSpace={'nowrap'}></Text>
    <Select
      minW={'10rem'}
      value={value}
      onChange={(e) => setValue(Number(e.target.value))}
    >
      {options.map((o) => (
        <option key={o.value} value={o.value}>
          {o.name}
        </option>
      ))}
    </Select>
  </HStack>
);

export default memo(Dropdown);
