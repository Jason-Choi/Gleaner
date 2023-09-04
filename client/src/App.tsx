import { Center, Flex, Spinner } from '@chakra-ui/react';
import { Footer, Header } from './components/Layout';
import { Main } from './components/Main';
import { initializedSignal } from './controller/init';

const App = () => (
  <Flex flexDir={'column'}>
    <Header />
    {initializedSignal.value ? (
      <Main />
    ) : (
      <Center minH={'80vh'} flexDir="column" gap={10}>
        Loading ...
        <Spinner size="xl" />
      </Center>
    )}
    <Footer />
  </Flex>
);

export default App;
