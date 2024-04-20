import { StyleSheet, Text, View, Button } from 'react-native';
import RecordButton from './RecordButton';

function onPressLearnMore() {
  console.log('-1');
}

export default function App() {
  return (
    <View style={styles.container}>
      <RecordButton />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  button: {
    backgroundColor: 'blue',
    color: 'white',
    borderRadius: "9999px",
    padding: "1.5px",
  }
});
