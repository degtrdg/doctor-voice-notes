import React, { useState } from 'react';
import { TouchableOpacity, StyleSheet } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome';
import AudioRecorderPlayer from 'react-native-audio-recorder-player';

const size = 80;
const audioRecorderPlayer = new AudioRecorderPlayer();

const RecordButton = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordPath, setRecordPath] = useState('');

  const onStartRecord = async () => {
    console.log('onStartRecord');
    console.log('start record');
    const path = Platform.select({
      ios: 'hello.m4a',
      android: 'sdcard/hello.mp4',
    });
    console.log(`path: ${path}`);
    const uri = await audioRecorderPlayer.startRecorder(path);
    console.log(`uri: ${uri}`)
    setRecordPath(path);
    audioRecorderPlayer.addRecordBackListener((e) => {
      console.log('recording', e);
      return;
    });
    console.log(`uri: ${uri}`);
  };

  const onStopRecord = async () => {
    const result = await audioRecorderPlayer.stopRecorder();
    audioRecorderPlayer.removeRecordBackListener();
    console.log(result);
    uploadAudioFile(recordPath);
  };

  const uploadAudioFile = async (audioPath) => {
    const data = new FormData();
    data.append('file', {
        uri: audioUri,
        name: 'audio.caf',
        type: 'audio/caf',
    });

    try {
      const response = await fetch('https://8c0f-131-179-94-24.ngrok-free.app/api/v1/upload_audio', {
        method: 'POST',
        body: data,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const responseBody = await response.json();
      if (response.status === 200) {
        Alert.alert('Upload Success', 'Audio file uploaded successfully');
      } else {
        Alert.alert('Upload Failed', 'Failed to upload audio file');
      }
    } catch (error) {
      console.error('Upload error:', error);
      Alert.alert('Upload Error', 'An error occurred while uploading the file');
    }
  };

  const handlePress = () => {
    if (!isRecording) {
      onStartRecord();
    } else {
      onStopRecord();
    }
    setIsRecording(!isRecording);
  };

  const styles = StyleSheet.create({
    button: {
      backgroundColor: isRecording ? '#ef4444' : '#2563eb',
      borderRadius: 99999,
      width: size,
      height: size,
      justifyContent: 'center',
      alignItems: 'center',
    },
  });

  return (
    <TouchableOpacity
      style={styles.button}
      onPress={handlePress}
      backgroundColor="blue"
    >
      <Icon
        name={isRecording ? 'pause' : 'microphone'}
        size={size / 2.75}
        color="white"
      />
    </TouchableOpacity>
  );
};

export default RecordButton;
