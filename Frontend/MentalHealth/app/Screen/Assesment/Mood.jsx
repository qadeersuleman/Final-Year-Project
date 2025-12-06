import React, { useState, useRef, useEffect } from "react";
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  Dimensions,
  Animated,
  Easing,
  TouchableOpacity,
  Platform,
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import Headers from "../../components/Assesment/Header";
import Colors from "../../assets/colors";
import Title from "../../components/Assesment/Title";
import AppButton from "../../components/AppButton";

const moods = [
  {
    id: "1",
    label: "Anxious",
    emoji: "😰",
    color: Colors.brand.primaryDark,
    bgColor: Colors.brand.primaryPastel,
  },
  {
    id: "2",
    label: "Sad",
    emoji: "😔",
    color: Colors.features.mood,
    bgColor: Colors.status.infoLight,
  },
  {
    id: "3",
    label: "Neutral",
    emoji: "😐",
    color: Colors.features.journal,
    bgColor: Colors.status.successLight,
  },
  {
    id: "4",
    label: "Happy",
    emoji: "😊",
    color: Colors.accent.coral,
    bgColor: Colors.status.warningLight,
  },
  {
    id: "5",
    label: "Excited",
    emoji: "🤩",
    color: Colors.accent.coralLight,
    bgColor: Colors.status.errorLight,
  },
];

const { width, height } = Dimensions.get("window");
const EMOJI_SIZE = width * 0.25;
const OPTION_SIZE = width * 0.18;

const MoodSelector = ({ route, navigation }) => {
  const [selectedMood, setSelectedMood] = useState(moods[1]);
  const scaleAnim = useRef(new Animated.Value(1)).current;
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideUpAnim = useRef(new Animated.Value(height * 0.1)).current;
  const optionScale = moods.reduce((acc, mood) => {
    acc[mood.id] = useRef(new Animated.Value(1)).current;
    return acc;
  }, {});

  // Get all data of previous Assesment Screens
  const { health_goal, age, weight } = route.params;

  useEffect(() => {
    // Entry animations
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 500,
        useNativeDriver: true,
      }),
      Animated.timing(slideUpAnim, {
        toValue: 0,
        duration: 600,
        easing: Easing.out(Easing.exp),
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  const handleMoodChange = (mood) => {
    // Pulse animation for selected emoji
    Animated.sequence([
      Animated.timing(scaleAnim, {
        toValue: 1.2,
        duration: 150,
        useNativeDriver: true,
      }),
      Animated.timing(scaleAnim, {
        toValue: 1,
        duration: 150,
        useNativeDriver: true,
      }),
    ]).start();

    // Bounce animation for selected option
    Animated.sequence([
      Animated.timing(optionScale[mood.id], {
        toValue: 0.9,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.timing(optionScale[mood.id], {
        toValue: 1.1,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.timing(optionScale[mood.id], {
        toValue: 1,
        duration: 100,
        useNativeDriver: true,
      }),
    ]).start();

    setSelectedMood(mood);
  };

  const renderMoodOption = ({ item }) => (
    <TouchableOpacity
      onPress={() => handleMoodChange(item)}
      activeOpacity={0.7}
    >
      <Animated.View
        style={[
          styles.emojiOption,
          {
            backgroundColor: item.bgColor,
            transform: [{ scale: optionScale[item.id] }],
          },
          selectedMood.id === item.id && styles.selectedOption,
        ]}
      >
        <Text style={[styles.optionEmoji, { color: item.color }]}>
          {item.emoji}
        </Text>
        {selectedMood.id === item.id && (
          <View
            style={[styles.selectionIndicator, { backgroundColor: item.color }]}
          />
        )}
      </Animated.View>
    </TouchableOpacity>
  );

  return (
    <LinearGradient
      colors={[Colors.neutrals.background, Colors.neutrals.surfaceLow]}
      style={styles.container}
    >
      <Headers
        onBack={() => navigation.goBack()}
        currentStep="4"
        color={Colors.text.primary}
      />

      <Animated.View
        style={[
          styles.content,
          {
            opacity: fadeAnim,
            transform: [{ translateY: slideUpAnim }],
          },
        ]}
      >
        <View style={{ marginTop: 30 }}>
          <Title style={[styles.title]}>
            {" "}
            How would you Describe your Mood?
          </Title>
        </View>

        <Animated.View
          style={[styles.emojiContainer, { transform: [{ scale: scaleAnim }] }]}
        >
          <LinearGradient
            colors={[Colors.brand.primary, Colors.accent.teal]}
            style={styles.emojiBackground}
            start={[0, 0]}
            end={[1, 1]}
          >
            <Text style={[styles.emoji, { color: selectedMood.color }]}>
              {selectedMood.emoji}
            </Text>
          </LinearGradient>
          <Text style={styles.selectedMood}>
            I feel{" "}
            <Text style={{ color: selectedMood.color, fontWeight: "bold" }}>
              {selectedMood.label.toLowerCase()}
            </Text>
          </Text>
        </Animated.View>

        <View style={styles.optionsContainer}>
          <FlatList
            data={moods}
            horizontal
            showsHorizontalScrollIndicator={false}
            keyExtractor={(item) => item.id}
            contentContainerStyle={styles.sliderContainer}
            renderItem={renderMoodOption}
          />
        </View>

        <View style={styles.buttonContainer}>
          <AppButton
            onPress={() =>
              navigation.navigate("SleepQuality", {
                health_goal: health_goal,
                age: age,
                weight: weight,
                mood: selectedMood.label,
              })
            }
            text="Continue"
          />
        </View>
      </Animated.View>
    </LinearGradient>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: Platform.OS === "ios" ? 30 : 20,
    paddingHorizontal: 24,
  },
  content: {
    flex: 1,
  },
  question: {
    fontSize: 28,
    color: Colors.text.primary,
    fontWeight: "600",
    marginTop: 30,
    marginBottom: 16,
    fontFamily: Platform.OS === "ios" ? "Helvetica Neue" : "sans-serif",
  },
  selectedMood: {
    fontSize: 20,
    color: Colors.text.secondary,
    marginTop: 20,
    textAlign: "center",
    fontFamily: Platform.OS === "ios" ? "Helvetica Neue" : "sans-serif",
  },
  emojiContainer: {
    alignItems: "center",
    marginVertical: 30,
  },
  emojiBackground: {
    width: EMOJI_SIZE,
    height: EMOJI_SIZE,
    borderRadius: EMOJI_SIZE / 2,
    justifyContent: "center",
    alignItems: "center",
    shadowColor: Colors.ui.shadowDark,
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.1,
    shadowRadius: 16,
    elevation: 8,
  },
  emoji: {
    fontSize: EMOJI_SIZE * 0.5,
  },
  optionsContainer: {
    marginTop: 40,
  },
  sliderContainer: {
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 20,
  },
  emojiOption: {
    width: OPTION_SIZE,
    height: OPTION_SIZE,
    borderRadius: OPTION_SIZE / 2,
    marginHorizontal: 12,
    justifyContent: "center",
    alignItems: "center",
    shadowColor: Colors.ui.shadow,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  selectedOption: {
    shadowColor: Colors.accent.teal,
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.3,
    shadowRadius: 12,
    elevation: 8,
  },
  optionEmoji: {
    fontSize: OPTION_SIZE * 0.5,
  },
  selectionIndicator: {
    position: "absolute",
    bottom: -10,
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  buttonContainer: {
    marginTop: 60,
  },
});

export default MoodSelector;
