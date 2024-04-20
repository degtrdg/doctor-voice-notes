import React, { useState, useEffect } from 'react';
import { TouchableOpacity, StyleSheet } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome';
import AudioRecorderPlayer from 'react-native-audio-recorder-player';
import { Audio } from 'expo-av';
import { FAST_API_URL } from "./constants";
import * as FileSystem from 'expo-file-system';
import axios from 'axios';

const size = 80;
const audioRecorderPlayer = new AudioRecorderPlayer();

const RecordButton = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordPath, setRecordPath] = useState('');
  const [recording, setRecording] = useState(null);
  const [audioPermission, setAudioPermission] = useState(null);

  useEffect(() => {
    async function getPermission() {
      await Audio.requestPermissionsAsync().then((permission) => {
        console.log('Permission Granted: ' + permission.granted);
        setAudioPermission(permission.granted)
      }).catch(error => {
        console.log(error);
      });
    };

    getPermission();
  }, []);

  const startRecording = async () => {
    try {
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true
      });
      const newRecording = new Audio.Recording();
      await newRecording.prepareToRecordAsync(Audio.RECORDING_OPTIONS_PRESET_HIGH_QUALITY);
      await newRecording.startAsync();
      setRecording(newRecording);
      setIsRecording(true);

      // Automatically stop and restart recording every 10 seconds
      setInterval(async () => {
        if (newRecording) {
          await stopRecording(newRecording);
          await startRecording();
        }
      }, 10000);  // 10000 ms = 10 seconds
    } catch (error) {
      console.error('Failed to start recording', error);
    }
  };

  const stopRecording = async (recording) => {
    try {
      console.log('Stopping Recording');
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      const fileInfo = await FileSystem.getInfoAsync(uri);
      uploadAudio(fileInfo.uri);
      // setRecording(null);
    } catch (error) {
      console.error('Failed to stop recording', error);
    }
  };

  const uploadAudio = async (uri) => {
    const data = new FormData();
    data.append('file', {
      uri: uri,
      name: 'audio.caf',
      type: 'audio/caf',
    });
    try {
      const response = await axios.post(`FAST_API_URL`, data, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('Audio uploaded:', response.data);
    } catch (error) {
      console.error('Upload failed:', error);
    }
  };

  const handleRecordButtonPress = async () => {
    if (isRecording) {
      await stopRecording(recording);
    } else {
      await startRecording();
    }
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
      onPress={handleRecordButtonPress}
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
