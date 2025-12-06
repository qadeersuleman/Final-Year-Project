import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  StyleSheet,
  Animated,
  Dimensions,
  StatusBar,
  SafeAreaView,
  KeyboardAvoidingView,
  Platform,
  Alert
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Feather, Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';

const { width, height } = Dimensions.get('window');

const MindfulJournal = () => {
  const [currentEntry, setCurrentEntry] = useState('');
  const [mood, setMood] = useState('');
  const [gratitude, setGratitude] = useState('');
  const [selectedMood, setSelectedMood] = useState(null);
  const [isExpanded, setIsExpanded] = useState(false);
  
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(50)).current;

  const moods = [
    { id: 1, emoji: '😢', label: 'Sad', color: '#6B73FF' },
    { id: 2, emoji: '😐', label: 'Neutral', color: '#4ECDC4' },
    { id: 3, emoji: '😊', label: 'Happy', color: '#FFD166' },
    { id: 4, emoji: '😄', label: 'Excited', color: '#FF6B6B' },
    { id: 5, emoji: '😌', label: 'Calm', color: '#96CEB4' },
  ];

  const prompts = [
    "What made you smile today?",
    "What are you grateful for right now?",
    "How are you really feeling?",
    "What would make today better?",
    "What's on your mind?"
  ];

  const animateIn = () => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 600,
        useNativeDriver: true,
      }),
      Animated.timing(slideAnim, {
        toValue: 0,
        duration: 600,
        useNativeDriver: true,
      })
    ]).start();
  };

  React.useEffect(() => {
    animateIn();
  }, []);

  const handleSaveEntry = () => {
    if (!currentEntry.trim()) {
      Alert.alert('Empty Entry', 'Please write something before saving.');
      return;
    }
    
    // In a real app, you would save to storage/API here
    Alert.alert(
      'Entry Saved',
      'Your mindful reflection has been saved successfully.',
      [
        {
          text: 'OK',
          onPress: () => {
            setCurrentEntry('');
            setGratitude('');
            setSelectedMood(null);
          }
        }
      ]
    );
  };

  const MoodSelector = () => (
    <View style={styles.moodContainer}>
      <Text style={styles.sectionTitle}>How are you feeling?</Text>
      <View style={styles.moodOptions}>
        {moods.map((item) => (
          <TouchableOpacity
            key={item.id}
            style={[
              styles.moodOption,
              selectedMood === item.id && { backgroundColor: item.color + '20', borderColor: item.color }
            ]}
            onPress={() => setSelectedMood(item.id)}
          >
            <Text style={styles.moodEmoji}>{item.emoji}</Text>
            <Text style={[
              styles.moodLabel,
              selectedMood === item.id && { color: item.color, fontWeight: '600' }
            ]}>
              {item.label}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );

  const GratitudeSection = () => (
    <View style={styles.gratitudeContainer}>
      <View style={styles.sectionHeader}>
        <Ionicons name="heart" size={20} color="#FF6B6B" />
        <Text style={styles.sectionTitle}>Today I'm grateful for...</Text>
      </View>
      <TextInput
        style={styles.gratitudeInput}
        placeholder="Three things I appreciate today..."
        placeholderTextColor="#A0A0A0"
        multiline
        value={gratitude}
        onChangeText={setGratitude}
      />
    </View>
  );

  const PromptSection = () => (
    <View style={styles.promptContainer}>
      <View style={styles.sectionHeader}>
        <MaterialCommunityIcons name="lightbulb-on" size={20} color="#FFD166" />
        <Text style={styles.sectionTitle}>Mindful Prompt</Text>
      </View>
      <Text style={styles.promptText}>
        {prompts[Math.floor(Math.random() * prompts.length)]}
      </Text>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#5E72EB" />
      <KeyboardAvoidingView 
        style={styles.container} 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <LinearGradient
          colors={['#5E72EB', '#9D50EA']}
          style={styles.header}
        >
          <View style={styles.headerContent}>
            <View>
              <Text style={styles.date}>{new Date().toLocaleDateString('en-US', { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
              })}</Text>
              <Text style={styles.title}>Mindful Journal</Text>
            </View>
            <TouchableOpacity style={styles.statsButton}>
              <Feather name="bar-chart-2" size={22} color="white" />
            </TouchableOpacity>
          </View>
        </LinearGradient>

        <ScrollView 
          style={styles.content}
          showsVerticalScrollIndicator={false}
        >
          <Animated.View 
            style={[
              styles.animatedContainer,
              { opacity: fadeAnim, transform: [{ translateY: slideAnim }] }
            ]}
          >
            <PromptSection />
            
            <MoodSelector />
            
            <GratitudeSection />
            
            <View style={styles.journalContainer}>
              <View style={styles.sectionHeader}>
                <Feather name="edit-3" size={20} color="#4ECDC4" />
                <Text style={styles.sectionTitle}>Your Reflection</Text>
              </View>
              <TextInput
                style={styles.journalInput}
                placeholder="Express your thoughts freely... This is your safe space."
                placeholderTextColor="#A0A0A0"
                multiline
                textAlignVertical="top"
                value={currentEntry}
                onChangeText={setCurrentEntry}
              />
              <View style={styles.entryStats}>
                <Text style={styles.wordCount}>{currentEntry.length} characters</Text>
                <Text style={styles.privateNote}>
                  <Feather name="lock" size={12} color="#A0A0A0" /> Private and secure
                </Text>
              </View>
            </View>
            
            <TouchableOpacity 
              style={[
                styles.saveButton,
                !currentEntry.trim() && styles.saveButtonDisabled
              ]}
              onPress={handleSaveEntry}
              disabled={!currentEntry.trim()}
            >
              <LinearGradient
                colors={['#5E72EB', '#9D50EA']}
                style={styles.saveButtonGradient}
              >
                <Text style={styles.saveButtonText}>Save Reflection</Text>
                <Ionicons name="ios-send" size={18} color="white" />
              </LinearGradient>
            </TouchableOpacity>
            
            <View style={styles.breathingExercise}>
              <Text style={styles.breathingTitle}>Quick Breathing Exercise</Text>
              <Text style={styles.breathingText}>Breathe in for 4 seconds, hold for 4, exhale for 6</Text>
              <View style={styles.breathingAnimation}>
                <View style={styles.breathCircle} />
              </View>
            </View>
          </Animated.View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8F9FF',
  },
  header: {
    paddingTop: Platform.OS === 'ios' ? 0 : StatusBar.currentHeight,
    paddingHorizontal: 20,
    paddingBottom: 20,
  },
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 10,
  },
  date: {
    color: 'rgba(255,255,255,0.8)',
    fontSize: 14,
    marginBottom: 4,
  },
  title: {
    color: 'white',
    fontSize: 28,
    fontWeight: '700',
    fontFamily: Platform.OS === 'ios' ? 'System' : 'sans-serif-medium',
  },
  statsButton: {
    padding: 10,
    borderRadius: 12,
    backgroundColor: 'rgba(255,255,255,0.2)',
  },
  content: {
    flex: 1,
  },
  animatedContainer: {
    padding: 20,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#2D3748',
    marginLeft: 8,
  },
  promptContainer: {
    backgroundColor: 'white',
    borderRadius: 16,
    padding: 16,
    marginBottom: 20,
    shadowColor: '#5E72EB',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 3,
  },
  promptText: {
    fontSize: 16,
    color: '#4A5568',
    lineHeight: 22,
    fontStyle: 'italic',
  },
  moodContainer: {
    backgroundColor: 'white',
    borderRadius: 16,
    padding: 16,
    marginBottom: 20,
    shadowColor: '#5E72EB',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 3,
  },
  moodOptions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  moodOption: {
    alignItems: 'center',
    padding: 12,
    borderRadius: 12,
    borderWidth: 1.5,
    borderColor: '#E2E8F0',
    width: (width - 80) / 5,
  },
  moodEmoji: {
    fontSize: 24,
    marginBottom: 6,
  },
  moodLabel: {
    fontSize: 12,
    color: '#718096',
  },
  gratitudeContainer: {
    backgroundColor: 'white',
    borderRadius: 16,
    padding: 16,
    marginBottom: 20,
    shadowColor: '#5E72EB',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 3,
  },
  gratitudeInput: {
    backgroundColor: '#F7FAFC',
    borderRadius: 12,
    padding: 14,
    fontSize: 16,
    color: '#2D3748',
    minHeight: 80,
    textAlignVertical: 'top',
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  journalContainer: {
    backgroundColor: 'white',
    borderRadius: 16,
    padding: 16,
    marginBottom: 20,
    shadowColor: '#5E72EB',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 3,
  },
  journalInput: {
    backgroundColor: '#F7FAFC',
    borderRadius: 12,
    padding: 14,
    fontSize: 16,
    color: '#2D3748',
    minHeight: 150,
    textAlignVertical: 'top',
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  entryStats: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 10,
  },
  wordCount: {
    fontSize: 12,
    color: '#A0A0A0',
  },
  privateNote: {
    fontSize: 12,
    color: '#A0A0A0',
  },
  saveButton: {
    borderRadius: 16,
    marginBottom: 20,
    overflow: 'hidden',
    shadowColor: '#5E72EB',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.3,
    shadowRadius: 12,
    elevation: 5,
  },
  saveButtonDisabled: {
    opacity: 0.6,
  },
  saveButtonGradient: {
    paddingVertical: 16,
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'center',
  },
  saveButtonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: '600',
    marginRight: 8,
  },
  breathingExercise: {
    backgroundColor: 'white',
    borderRadius: 16,
    padding: 16,
    alignItems: 'center',
    shadowColor: '#5E72EB',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 3,
  },
  breathingTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2D3748',
    marginBottom: 8,
  },
  breathingText: {
    fontSize: 14,
    color: '#718096',
    marginBottom: 16,
    textAlign: 'center',
  },
  breathingAnimation: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#F7FAFC',
    justifyContent: 'center',
    alignItems: 'center',
  },
  breathCircle: {
    width: 30,
    height: 30,
    borderRadius: 15,
    backgroundColor: '#4ECDC4',
  },
});

export default MindfulJournal;