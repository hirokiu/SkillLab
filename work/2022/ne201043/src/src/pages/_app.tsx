import '@/styles/globals.css';
import { ChakraProvider } from '@chakra-ui/react';
import type { AppProps } from 'next/app';
import MetaInfo from '@/components/MetaInfo';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ChakraProvider>
      <MetaInfo />
      <Component {...pageProps} />
    </ChakraProvider>
  );
}
export default MyApp;
