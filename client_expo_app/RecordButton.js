import React, { useState, useEffect } from 'react';
import { TouchableOpacity, StyleSheet } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome';
import { Audio } from 'expo-av';
import { FAST_API_URL } from "./constants";
import * as FileSystem from 'expo-file-system';
import axios from 'axios';

const size = 80;
let recording = new Audio.Recording();

const RecordButton = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioPermission, setAudioPermission] = useState(null);

  useEffect(() => {
    function getPermission() {
      Audio.requestPermissionsAsync().then((permission) => {
        console.log('Permission Granted: ' + permission.granted);
        setAudioPermission(permission.granted);
      }).catch(error => {
        console.log(error);
      });
    };
    getPermission();
  }, []);

  const startRecording = async () => {
    try {
      console.log('Requesting permissions..');
      setIsRecording(true);
      await Audio.requestPermissionsAsync();
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });
      console.log('Starting recording..');
      await recording.prepareToRecordAsync(
        Audio.RECORDING_OPTIONS_PRESET_HIGH_QUALITY
      );
      await recording.startAsync();
      console.log('Recording started');
    } catch (err) {
      console.error('Failed to start recording', err);
    }
  };

  async function stopRecording() {
    try {
      console.log('Stopping recording..');
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      console.log('Recording stopped and stored at', uri);
      recording = new Audio.Recording();

      const fileInfo = await FileSystem.getInfoAsync(uri);
      uploadAudio(fileInfo.uri);
    }
    catch (error) {
      console.error('Failed to stop recording', error);
    }

  }

  const uploadAudio = async (uri) => {
    const data = new FormData();
    data.append('file', {
      uri: uri,
      name: 'audio.caf',
      type: 'audio/caf',
    });
    try {
      const response = await axios.post(`${FAST_API_URL}/api/upload_audio`, data, {
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
    startRecording();

    setInterval(async () => {
      await stopRecording();
      await startRecording();
    }, 10000);
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
