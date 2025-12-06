import React from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Dimensions,
} from "react-native";

import AITherapySection from "./AITherapySection";
import ArticlesSection from "./ArticlesSection";
import HomeCards from "../../Screen/Home/HomeCards";
import HomeProfile from "../../Screen/Home/HeaderProfile";
import MindfulTracker from "./MindfulTracker";
import Colors from "../../assets/colors";
import Screen from "../../components/Screen";
import YoutubeSection from "./YoutubeSection";
import BottomNavigation from "./BottomNavigation"; // Import the BottomNavigation

const { width } = Dimensions.get("window");

const Home = ({ navigation }) => {
  return (
    <Screen>
      <View style={styles.container}>
        <ScrollView
          style={styles.scrollView}
          showsVerticalScrollIndicator={false}
        >
          <HomeProfile />
          <HomeCards />
          <MindfulTracker />
          <AITherapySection />
          <ArticlesSection />
          <YoutubeSection />
        </ScrollView>

        {/* Bottom Navigation */}
        <BottomNavigation navigation={navigation} />
      </View>
    </Screen>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.neutrals.background,
  },
  scrollView: {
    flex: 1,
    marginBottom: 80, // Keep margin to ensure content doesn't hide behind navigation
  },
});

export default Home;