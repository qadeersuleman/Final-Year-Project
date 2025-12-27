// components/EditProfile.jsx
import React, { useState, useRef, useEffect } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Image,
  Dimensions,
  Animated,
  Easing,
  KeyboardAvoidingView,
  Alert,
  Platform,
  Keyboard,
  ScrollView,
  Modal,
  SafeAreaView,
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import {
  MaterialIcons,
  FontAwesome,
  Ionicons,
  Feather,
} from "@expo/vector-icons";
import { Formik } from "formik";
import * as Yup from "yup";
import LottieView from "lottie-react-native";
import * as ImagePicker from "expo-image-picker";
import DateTimePicker from "@react-native-community/datetimepicker";
// import Svg, { Circle } from "react-native-svg";
import * as Haptics from "expo-haptics";

import { getSession, saveSession } from "../../utils/session";
import { updateUserProfile } from "../../Services/api";
import Screen from "../../components/Screen";
import Colors from "../../assets/colors";
import SuccessModal from "../../components/SuccessModal";

const { width, height } = Dimensions.get("window");
const isSmallDevice = width < 375;

const EditProfile = ({ navigation, route }) => {
  const { username } = route.params || {};

  const [profileImage, setProfileImage] = useState(null);
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [genderModalVisible, setGenderModalVisible] = useState(false);
  const [countryModalVisible, setCountryModalVisible] = useState(false);
  const [keyboardStatus, setKeyboardStatus] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [modalMessage, setModalMessage] = useState('');

  // Animation refs - Fixed to avoid conflicts
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideUpAnim = useRef(new Animated.Value(50)).current;
  const buttonScale = useRef(new Animated.Value(1)).current;
  const imageScale = useRef(new Animated.Value(1)).current;
  const modalScale = useRef(new Animated.Value(0.8)).current;
  const modalOpacity = useRef(new Animated.Value(0)).current;
  const countryModalScale = useRef(new Animated.Value(0.8)).current;
  const countryModalOpacity = useRef(new Animated.Value(0)).current;
  const particle1 = useRef(new Animated.Value(0)).current;
  const particle2 = useRef(new Animated.Value(0)).current;

  const genderOptions = [
    { label: "Male", value: "male", icon: "male", color: Colors.brand.primary },
    { label: "Female", value: "female", icon: "female", color: Colors.accent.violet },
    { label: "Other", value: "other", icon: "person-outline", color: Colors.accent.teal },
    { 
      label: "Prefer not to say", 
      value: "prefer_not_to_say", 
      icon: "eye-off-outline", 
      color: Colors.text.tertiary 
    },
  ];

  const countryOptions = [
    { code: "+92", name: "Pakistan", flag: "🇵🇰", maxLength: 10 },
    { code: "+91", name: "India", flag: "🇮🇳", maxLength: 10 },
    { code: "+1", name: "USA", flag: "🇺🇸", maxLength: 10 },
  ];

  useEffect(() => {
    // Entrance animations using only timing to avoid conflicts
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 800,
        useNativeDriver: true,
        easing: Easing.out(Easing.cubic),
      }),
      Animated.timing(slideUpAnim, {
        toValue: 0,
        duration: 1000,
        useNativeDriver: true,
        easing: Easing.out(Easing.cubic),
      }),
      Animated.timing(particle1, {
        toValue: 1,
        duration: 600,
        useNativeDriver: true,
        delay: 200,
      }),
      Animated.timing(particle2, {
        toValue: 1,
        duration: 600,
        useNativeDriver: true,
        delay: 400,
      }),
    ]).start();

    // Keyboard listeners
    const keyboardDidShowListener = Keyboard.addListener(
      "keyboardDidShow",
      () => setKeyboardStatus(true)
    );
    const keyboardDidHideListener = Keyboard.addListener(
      "keyboardDidHide",
      () => setKeyboardStatus(false)
    );

    return () => {
      keyboardDidShowListener.remove();
      keyboardDidHideListener.remove();
    };
  }, []);

  const openGenderModal = () => {
    setGenderModalVisible(true);
    Animated.parallel([
      Animated.timing(modalScale, {
        toValue: 1,
        duration: 300,
        useNativeDriver: true,
        easing: Easing.out(Easing.back(1)),
      }),
      Animated.timing(modalOpacity, {
        toValue: 1,
        duration: 300,
        useNativeDriver: true,
      }),
    ]).start();
  };

  const closeGenderModal = () => {
    Animated.parallel([
      Animated.timing(modalScale, {
        toValue: 0.8,
        duration: 200,
        useNativeDriver: true,
      }),
      Animated.timing(modalOpacity, {
        toValue: 0,
        duration: 200,
        useNativeDriver: true,
      }),
    ]).start(() => setGenderModalVisible(false));
  };

  const openCountryModal = () => {
    setCountryModalVisible(true);
    Animated.parallel([
      Animated.timing(countryModalScale, {
        toValue: 1,
        duration: 300,
        useNativeDriver: true,
        easing: Easing.out(Easing.back(1)),
      }),
      Animated.timing(countryModalOpacity, {
        toValue: 1,
        duration: 300,
        useNativeDriver: true,
      }),
    ]).start();
  };

  const closeCountryModal = () => {
    Animated.parallel([
      Animated.timing(countryModalScale, {
        toValue: 0.8,
        duration: 200,
        useNativeDriver: true,
      }),
      Animated.timing(countryModalOpacity, {
        toValue: 0,
        duration: 200,
        useNativeDriver: true,
      }),
    ]).start(() => setCountryModalVisible(false));
  };

  const pickImage = async () => {
    // Image picker animation
    Animated.sequence([
      Animated.timing(imageScale, {
        toValue: 0.9,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.timing(imageScale, {
        toValue: 1,
        duration: 100,
        useNativeDriver: true,
      }),
    ]).start();

    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [1, 1],
      quality: 1,
    });

    if (!result.canceled) {
      setProfileImage(result.assets[0].uri);
    }
  };

  const validationSchema = Yup.object().shape({
    fullName: Yup.string().required("Full name is required"),
    gender: Yup.string().required("Gender is required"),
    birthDate: Yup.date()
      .max(new Date(), "Birth date cannot be in the future")
      .required("Birth date is required"),
    phoneNumber: Yup.string()
      .matches(/^[0-9]+$/, "Phone number must contain only digits")
      .required("Phone number is required"),
  });

  const handleSubmit = async (values) => {
    setIsSubmitting(true);
    try {
      // Button animation
      Animated.sequence([
        Animated.timing(buttonScale, {
          toValue: 0.95,
          duration: 100,
          useNativeDriver: true,
        }),
        Animated.timing(buttonScale, {
          toValue: 1,
          duration: 100,
          useNativeDriver: true,
        }),
      ]).start();

      const userSession = await getSession();

      if (!userSession || !userSession.id) {
        Alert.alert("Error", "User not logged in. Please login again.");
        navigation.navigate("Login");
        return;
      }

      const formData = new FormData();
      formData.append("user_id", userSession.id);
      formData.append("email", userSession.email);
      formData.append("full_name", values.fullName);
      formData.append("gender", values.gender);
      formData.append("date_of_birth", values.birthDate.toISOString().split("T")[0]);
      
      const fullPhoneNumber = `${values.countryCode}${values.phoneNumber}`;
      formData.append("phone_number", fullPhoneNumber);

      if (profileImage) {
        let filename = profileImage.split("/").pop();
        let match = /\.(\w+)$/.exec(filename);
        let type = match ? `image/${match[1]}` : "image/jpeg";

        formData.append("profile_image", {
          uri: profileImage,
          name: filename,
          type: type,
        });
      }

      const response = await updateUserProfile(formData);

      const updatedUser = {
        ...userSession,
        full_name: values.fullName,
        gender: values.gender,
        date_of_birth: values.birthDate.toISOString().split("T")[0],
        phone_number: fullPhoneNumber,
        hasCompletedProfile: true,
        profile_image: response.user.profile_image,
      };
      await saveSession(updatedUser);

      // ✅ Show success modal instead of Alert
      setModalMessage('Your profile has been updated successfully!');
      setIsModalVisible(true);
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

    } catch (error) {
      console.error("Profile update error:", error.message);
      Alert.alert("Error", error.message || "Failed to update profile. Please try again.");
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleRedirectToHealthGoal = () => {
    navigation.navigate('Mood');
  };

  const formatDate = (date) => {
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  const FloatingParticle = ({ animValue, delay, size, color, style }) => (
    <Animated.View
      style={[
        styles.floatingParticle,
        {
          width: size,
          height: size,
          backgroundColor: color,
          opacity: animValue,
          transform: [
            {
              translateY: animValue.interpolate({
                inputRange: [0, 1],
                outputRange: [20, 0],
              }),
            },
          ],
        },
        style,
      ]}
    />
  );

  const GenderOption = ({ option, onSelect, isSelected }) => (
    <TouchableOpacity
      style={[
        styles.genderOption,
        isSelected && styles.genderOptionSelected,
      ]}
      onPress={onSelect}
      activeOpacity={0.7}
    >
      <View style={styles.genderOptionContent}>
        <View style={[styles.genderIconContainer, { backgroundColor: option.color + '15' }]}>
          <Ionicons 
            name={option.icon} 
            size={24} 
            color={option.color} 
          />
        </View>
        <Text style={[
          styles.genderOptionText,
          isSelected && styles.genderOptionTextSelected
        ]}>
          {option.label}
        </Text>
      </View>
      {isSelected && (
        <Ionicons name="checkmark-circle" size={24} color={Colors.status.success} />
      )}
    </TouchableOpacity>
  );

  const CountryOption = ({ option, onSelect, isSelected }) => (
    <TouchableOpacity
      style={[
        styles.countryOption,
        isSelected && styles.countryOptionSelected,
      ]}
      onPress={onSelect}
      activeOpacity={0.7}
    >
      <View style={styles.countryOptionContent}>
        <Text style={styles.countryFlag}>{option.flag}</Text>
        <View style={styles.countryTextContainer}>
          <Text style={styles.countryName}>{option.name}</Text>
          <Text style={styles.countryCode}>{option.code}</Text>
        </View>
      </View>
      {isSelected && (
        <Ionicons name="checkmark-circle" size={24} color={Colors.status.success} />
      )}
    </TouchableOpacity>
  );

  const GenderModal = ({ 
    visible, 
    onClose, 
    modalScale, 
    modalOpacity, 
    selectedGender, 
    onGenderSelect 
  }) => (
    <Modal
      visible={visible}
      transparent
      animationType="none"
      onRequestClose={onClose}
    >
      <View style={styles.modalOverlay}>
        <Animated.View 
          style={[
            styles.modalContainer,
            {
              opacity: modalOpacity,
              transform: [{ scale: modalScale }]
            }
          ]}
        >
          <View style={styles.modalHeader}>
            <Text style={styles.modalTitle}>Select Gender</Text>
            <TouchableOpacity onPress={onClose} style={styles.closeButton}>
              <Ionicons name="close" size={24} color={Colors.text.primary} />
            </TouchableOpacity>
          </View>
          
          <View style={styles.genderOptionsContainer}>
            {genderOptions.map((option) => (
              <GenderOption
                key={option.value}
                option={option}
                isSelected={selectedGender === option.value}
                onSelect={() => onGenderSelect(option.value)}
              />
            ))}
          </View>
        </Animated.View>
      </View>
    </Modal>
  );

  const CountryModal = ({ 
    visible, 
    onClose, 
    modalScale, 
    modalOpacity, 
    selectedCountry, 
    onCountrySelect 
  }) => (
    <Modal
      visible={visible}
      transparent
      animationType="none"
      onRequestClose={onClose}
    >
      <View style={styles.modalOverlay}>
        <Animated.View 
          style={[
            styles.modalContainer,
            {
              opacity: modalOpacity,
              transform: [{ scale: modalScale }]
            }
          ]}
        >
          <View style={styles.modalHeader}>
            <Text style={styles.modalTitle}>Select Country</Text>
            <TouchableOpacity onPress={onClose} style={styles.closeButton}>
              <Ionicons name="close" size={24} color={Colors.text.primary} />
            </TouchableOpacity>
          </View>
          
          <View style={styles.countryOptionsContainer}>
            {countryOptions.map((option) => (
              <CountryOption
                key={option.code}
                option={option}
                isSelected={selectedCountry === option.code}
                onSelect={() => onCountrySelect(option)}
              />
            ))}
          </View>
        </Animated.View>
      </View>
    </Modal>
  );

  return (
    <Screen>
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        style={{ flex: 1, backgroundColor: Colors.background.main }}
        keyboardVerticalOffset={Platform.OS === "ios" ? 60 : 0}
      >
        <SafeAreaView style={{ flex: 1 }}>
          {/* Animated Background Elements */}
          <View style={styles.backgroundContainer}>
            <FloatingParticle
              animValue={particle1}
              size={100}
              color={Colors.brand.primary + '15'}
              style={styles.particle1}
            />
            <FloatingParticle
              animValue={particle2}
              size={80}
              color={Colors.accent.violet + '10'}
              style={styles.particle2}
            />
          </View>

          <Animated.View style={{ opacity: fadeAnim, flex: 1 }}>
            {/* Enhanced Header */}
            <LinearGradient
              colors={Colors.gradients.calm}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
              style={styles.header}
            >
              <TouchableOpacity
                style={styles.backButton}
                onPress={() => navigation.goBack()}
              >
                <Ionicons name="chevron-back" size={28} color={Colors.text.inverted} />
              </TouchableOpacity>
              
              <View style={styles.headerTitleContainer}>
                <Text style={styles.headerTitle}>Edit Profile</Text>
                <Text style={styles.headerSubtitle}>Update your information</Text>
              </View>
              
              <View style={styles.placeholderButton} />
            </LinearGradient>

            {/* Main Content */}
            <ScrollView 
              style={styles.scrollContainer}
              showsVerticalScrollIndicator={false}
              contentContainerStyle={styles.scrollContent}
              keyboardShouldPersistTaps="handled"
            >
              <Animated.View
                style={[
                  styles.container,
                  { 
                    transform: [{ translateY: slideUpAnim }],
                    opacity: fadeAnim 
                  },
                ]}
              >
                {/* Profile Picture */}
                <View style={styles.profilePictureContainer}>
                  <Animated.View style={{ transform: [{ scale: imageScale }] }}>
                    <TouchableOpacity
                      onPress={pickImage}
                      style={styles.profileImageWrapper}
                      activeOpacity={0.8}
                    >
                      <LinearGradient
                        colors={profileImage ? ["transparent", "transparent"] : Colors.gradients.calm}
                        start={{ x: 0, y: 0 }}
                        end={{ x: 1, y: 1 }}
                        style={styles.profileImageGradient}
                      >
                        {profileImage ? (
                          <Image
                            source={{ uri: profileImage }}
                            style={styles.profileImage}
                          />
                        ) : (
                          <View style={styles.profileImagePlaceholder}>
                            <FontAwesome name="user" size={40} color={Colors.text.inverted} />
                          </View>
                        )}
                        <LinearGradient
                          colors={[Colors.brand.primary + 'CC', Colors.accent.violet + 'CC']}
                          style={styles.editIconOverlay}
                        >
                          <Feather name="camera" size={20} color={Colors.text.inverted} />
                        </LinearGradient>
                      </LinearGradient>
                    </TouchableOpacity>
                  </Animated.View>
                  <Text style={styles.profilePictureText}>Tap to change photo</Text>
                </View>

                <Formik
                  initialValues={{
                    fullName: "",
                    gender: "",
                    birthDate: new Date(1990, 0, 1),
                    countryCode: "+92",
                    phoneNumber: "",
                  }}
                  validationSchema={validationSchema}
                  onSubmit={handleSubmit}
                >
                  {({
                    handleChange,
                    handleBlur,
                    handleSubmit,
                    setFieldValue,
                    values,
                    errors,
                    touched,
                  }) => {
                    const selectedCountry = countryOptions.find(opt => opt.code === values.countryCode);
                    const maxPhoneLength = selectedCountry?.maxLength || 10;

                    return (
                    <View style={styles.formContainer}>
                      {/* Full Name */}
                      <View style={styles.inputGroup}>
                        <Text style={styles.label}>Full Name</Text>
                        <View style={styles.inputContainer}>
                          <Ionicons
                            name="person-outline"
                            size={22}
                            color={Colors.brand.primary}
                            style={styles.icon}
                          />
                          <TextInput
                            style={styles.input}
                            placeholder="Enter your full name"
                            placeholderTextColor={Colors.text.tertiary}
                            value={values.fullName}
                            onChangeText={handleChange("fullName")}
                            onBlur={handleBlur("fullName")}
                            onFocus={() => setKeyboardStatus(true)}
                          />
                        </View>
                        {touched.fullName && errors.fullName && (
                          <Text style={styles.error}>{errors.fullName}</Text>
                        )}
                      </View>

                      {/* Gender Selection */}
                      <View style={styles.inputGroup}>
                        <Text style={styles.label}>Gender</Text>
                        <TouchableOpacity
                          style={styles.genderInputContainer}
                          onPress={openGenderModal}
                          activeOpacity={0.8}
                        >
                          <Ionicons
                            name="people-outline"
                            size={22}
                            color={Colors.brand.primary}
                            style={styles.icon}
                          />
                          <View style={styles.genderTextContainer}>
                            <Text style={[
                              styles.genderText,
                              !values.gender && styles.genderPlaceholder
                            ]}>
                              {values.gender 
                                ? genderOptions.find(opt => opt.value === values.gender)?.label
                                : "Select your gender"
                              }
                            </Text>
                          </View>
                          <Ionicons
                            name="chevron-down"
                            size={22}
                            color={Colors.brand.primary}
                            style={styles.dropdownIcon}
                          />
                        </TouchableOpacity>
                        {touched.gender && errors.gender && (
                          <Text style={styles.error}>{errors.gender}</Text>
                        )}
                      </View>

                      {/* Birth Date */}
                      <View style={styles.inputGroup}>
                        <Text style={styles.label}>Birth Date</Text>
                        <TouchableOpacity
                          style={styles.inputContainer}
                          onPress={() => setShowDatePicker(true)}
                          activeOpacity={0.8}
                        >
                          <Ionicons
                            name="calendar-outline"
                            size={22}
                            color={Colors.brand.primary}
                            style={styles.icon}
                          />
                          <View style={styles.dateTextContainer}>
                            <Text
                              style={[
                                styles.dateText,
                                !values.birthDate && { color: Colors.text.tertiary },
                              ]}
                            >
                              {values.birthDate
                                ? formatDate(values.birthDate)
                                : "Select your birth date"}
                            </Text>
                          </View>
                        </TouchableOpacity>
                        {touched.birthDate && errors.birthDate && (
                          <Text style={styles.error}>{errors.birthDate}</Text>
                        )}
                        {showDatePicker && (
                          <DateTimePicker
                            value={values.birthDate}
                            mode="date"
                            display={Platform.OS === "ios" ? "spinner" : "default"}
                            maximumDate={new Date()}
                            onChange={(event, date) => {
                              setShowDatePicker(Platform.OS === "ios");
                              if (date) {
                                setFieldValue("birthDate", date);
                              }
                            }}
                          />
                        )}
                      </View>

                      {/* Phone Number */}
                      <View style={styles.inputGroup}>
                        <Text style={styles.label}>Phone Number</Text>
                        <View style={styles.phoneInputContainer}>
                          <TouchableOpacity
                            style={styles.countryCodeSelector}
                            onPress={openCountryModal}
                            activeOpacity={0.8}
                          >
                            <Text style={styles.countryCodeText}>
                              {selectedCountry?.flag} {values.countryCode}
                            </Text>
                            <Ionicons
                              name="chevron-down"
                              size={16}
                              color={Colors.brand.primary}
                              style={styles.countryDropdownIcon}
                            />
                          </TouchableOpacity>

                          <View style={styles.phoneNumberInput}>
                            <Ionicons
                              name="call-outline"
                              size={22}
                              color={Colors.brand.primary}
                              style={styles.phoneIcon}
                            />
                            <TextInput
                              style={styles.phoneInput}
                              placeholder={`Enter phone number (${maxPhoneLength} digits)`}
                              placeholderTextColor={Colors.text.tertiary}
                              keyboardType="phone-pad"
                              value={values.phoneNumber}
                              onChangeText={(text) => {
                                const numbersOnly = text.replace(/[^0-9]/g, '');
                                if (numbersOnly.length <= maxPhoneLength) {
                                  handleChange("phoneNumber")(numbersOnly);
                                }
                              }}
                              onBlur={handleBlur("phoneNumber")}
                              onFocus={() => setKeyboardStatus(true)}
                              maxLength={maxPhoneLength}
                            />
                          </View>
                        </View>
                        {touched.phoneNumber && errors.phoneNumber && (
                          <Text style={styles.error}>{errors.phoneNumber}</Text>
                        )}
                      </View>

                      {/* Save Button */}
                      <Animated.View
                        style={[
                          { transform: [{ scale: buttonScale }] },
                          keyboardStatus && styles.saveButtonKeyboardOpen,
                        ]}
                      >
                        <TouchableOpacity
                          style={styles.saveButton}
                          onPress={handleSubmit}
                          activeOpacity={0.9}
                          disabled={isSubmitting}
                        >
                          {isSubmitting ? (
                            <View style={styles.loadingContainer}>
                              <LottieView
                                source={require("../../assets/json/Trail loading.json")}
                                autoPlay
                                loop
                                style={styles.loadingAnimation}
                              />
                            </View>
                          ) : (
                            <LinearGradient
                              colors={Colors.gradients.calm}
                              start={{ x: 0, y: 0 }}
                              end={{ x: 1, y: 0 }}
                              style={styles.buttonGradient}
                            >
                              <Ionicons name="save-outline" size={22} color={Colors.text.inverted} style={styles.saveIcon} />
                              <Text style={styles.saveButtonText}>
                                Save Changes
                              </Text>
                            </LinearGradient>
                          )}
                        </TouchableOpacity>
                      </Animated.View>

                      {/* Gender Modal */}
                      <GenderModal
                        visible={genderModalVisible}
                        onClose={closeGenderModal}
                        modalScale={modalScale}
                        modalOpacity={modalOpacity}
                        selectedGender={values.gender}
                        onGenderSelect={(gender) => {
                          setFieldValue("gender", gender);
                          closeGenderModal();
                        }}
                      />

                      {/* Country Modal */}
                      <CountryModal
                        visible={countryModalVisible}
                        onClose={closeCountryModal}
                        modalScale={countryModalScale}
                        modalOpacity={countryModalOpacity}
                        selectedCountry={values.countryCode}
                        onCountrySelect={(country) => {
                          setFieldValue("countryCode", country.code);
                          setFieldValue("phoneNumber", "");
                          closeCountryModal();
                        }}
                      />
                    </View>
                  )}}
                </Formik>
              </Animated.View>
            </ScrollView>
          </Animated.View>

          {/* Success Modal */}
          <SuccessModal
            isVisible={isModalVisible}
            onClose={() => setIsModalVisible(false)}
            title="Profile Updated!"
            message={modalMessage || "Your profile has been updated successfully!"}
            redirectTo="HealthGoal"
            autoRedirectDuration={5000}
            onRedirect={handleRedirectToHealthGoal}
            showConfetti={true}
            animationSource={require('../../assets/json/Blue Checkmark.json')}
          />
        </SafeAreaView>
      </KeyboardAvoidingView>
    </Screen>
  );
};

const styles = StyleSheet.create({
  backgroundContainer: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    zIndex: -1,
  },
  floatingParticle: {
    position: 'absolute',
    borderRadius: 100,
  },
  particle1: {
    top: '15%',
    right: '10%',
  },
  particle2: {
    bottom: '25%',
    left: '15%',
  },
  header: {
    height: 120,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 25,
    paddingTop: Platform.OS === 'ios' ? 10 : 40,
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
    shadowColor: Colors.brand.primary,
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.2,
    shadowRadius: 15,
    elevation: 8,
  },
  backButton: {
    width: 50,
    height: 50,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 15,
  },
  headerTitleContainer: {
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 24,
    color: Colors.text.inverted,
    fontWeight: "bold",
    fontFamily: Platform.select({ ios: 'System', android: 'Roboto' }),
  },
  headerSubtitle: {
    fontSize: 14,
    color: "rgba(255, 255, 255, 0.8)",
    marginTop: 4,
  },
  placeholderButton: {
    width: 50,
    height: 50,
  },
  scrollContainer: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    paddingBottom: 30,
  },
  container: {
    flex: 1,
    paddingBottom: 10,
  },
  formContainer: {
    paddingHorizontal: 25,
    marginTop: 20,
  },
  profilePictureContainer: {
    alignItems: "center",
    marginVertical: 30,
  },
  profileImageWrapper: {
    position: "relative",
    marginBottom: 12,
  },
  profileImageGradient: {
    width: 140,
    height: 140,
    borderRadius: 70,
    justifyContent: "center",
    alignItems: "center",
    shadowColor: Colors.brand.primary,
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.3,
    shadowRadius: 15,
    elevation: 8,
  },
  profileImage: {
    width: '100%',
    height: '100%',
    borderRadius: 70,
  },
  profileImagePlaceholder: {
    width: '100%',
    height: '100%',
    borderRadius: 70,
    justifyContent: "center",
    alignItems: "center",
  },
  editIconOverlay: {
    position: "absolute",
    bottom: 8,
    right: 8,
    width: 36,
    height: 36,
    borderRadius: 18,
    justifyContent: "center",
    alignItems: "center",
    borderWidth: 2,
    borderColor: Colors.neutrals.white,
    shadowColor: Colors.ui.shadowDark,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
  },
  profilePictureText: {
    color: Colors.text.tertiary,
    fontSize: 14,
    fontWeight: '500',
  },
  inputGroup: {
    marginBottom: 20,
  },
  label: {
    marginBottom: 10,
    fontSize: 16,
    fontWeight: "600",
    color: Colors.text.primary,
    fontFamily: Platform.select({ ios: 'System', android: 'Roboto' }),
  },
  inputContainer: {
    flexDirection: "row",
    alignItems: "center",
    borderWidth: 2,
    borderColor: Colors.neutrals.border,
    borderRadius: 16,
    paddingHorizontal: 18,
    height: 56,
    backgroundColor: Colors.background.card,
    shadowColor: Colors.ui.shadow,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 6,
    elevation: 2,
  },
  genderInputContainer: {
    flexDirection: "row",
    alignItems: "center",
    borderWidth: 2,
    borderColor: Colors.neutrals.border,
    borderRadius: 16,
    paddingHorizontal: 18,
    height: 56,
    backgroundColor: Colors.background.card,
    shadowColor: Colors.ui.shadow,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 6,
    elevation: 2,
  },
  phoneInputContainer: {
    flexDirection: "row",
    alignItems: "center",
    borderWidth: 2,
    borderColor: Colors.neutrals.border,
    borderRadius: 16,
    height: 56,
    backgroundColor: Colors.background.card,
    shadowColor: Colors.ui.shadow,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 6,
    elevation: 2,
    overflow: 'hidden',
  },
  countryCodeSelector: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 8,
    backgroundColor: Colors.background.subtle,
    borderRightWidth: 1,
    borderRightColor: Colors.neutrals.border,
    height: '100%',
  },
  countryCodeText: {
    fontSize: 16,
    color: Colors.text.primary,
    fontWeight: '500',
    marginRight: 8,
  },
  countryDropdownIcon: {
    marginLeft: 4,
  },
  phoneNumberInput: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
  },
  phoneIcon: {
    marginRight: 12,
  },
  phoneInput: {
    flex: 1,
    height: '100%',
    color: Colors.text.primary,
    fontSize: 16,
    fontFamily: Platform.select({ ios: 'System', android: 'Roboto' }),
    fontWeight: '500',
  },
  genderTextContainer: {
    flex: 1,
    justifyContent: "center",
    height: "100%",
  },
  genderText: {
    fontSize: 16,
    color: Colors.text.primary,
    fontWeight: '500',
  },
  genderPlaceholder: {
    color: Colors.text.tertiary,
  },
  input: {
    flex: 1,
    paddingHorizontal: 12,
    height: "100%",
    color: Colors.text.primary,
    fontSize: 16,
    fontFamily: Platform.select({ ios: 'System', android: 'Roboto' }),
    fontWeight: '500',
  },
  dateTextContainer: {
    flex: 1,
    justifyContent: "center",
    height: "100%",
  },
  dateText: {
    fontSize: 16,
    color: Colors.text.primary,
    fontWeight: '500',
  },
  icon: {
    marginRight: 12,
  },
  dropdownIcon: {
    marginLeft: 8,
  },
  saveButton: {
    height: 60,
    borderRadius: 20,
    marginTop: 30,
    overflow: "hidden",
    shadowColor: Colors.brand.primary,
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.3,
    shadowRadius: 15,
    elevation: 8,
  },
  saveButtonKeyboardOpen: {
    marginBottom: 30,
  },
  buttonGradient: {
    width: "100%",
    height: "100%",
    justifyContent: "center",
    alignItems: "center",
    flexDirection: 'row',
  },
  saveIcon: {
    marginRight: 10,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: Colors.brand.primary,
  },
  loadingAnimation: {
    width: 60,
    height: 60,
  },
  saveButtonText: {
    fontSize: 18,
    color: Colors.text.inverted,
    fontWeight: "700",
    fontFamily: Platform.select({ ios: 'System', android: 'Roboto' }),
  },
  error: {
    color: Colors.status.error,
    fontSize: 13,
    marginTop: 6,
    marginLeft: 12,
    fontWeight: '500',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: Colors.ui.overlay,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  modalContainer: {
    width: '90%',
    maxWidth: 400,
    backgroundColor: Colors.background.card,
    borderRadius: 24,
    padding: 24,
    shadowColor: Colors.ui.shadowDark,
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.3,
    shadowRadius: 20,
    elevation: 10,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: Colors.text.primary,
  },
  closeButton: {
    padding: 4,
  },
  genderOptionsContainer: {
    gap: 12,
  },
  countryOptionsContainer: {
    gap: 12,
  },
  genderOption: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
    borderRadius: 16,
    backgroundColor: Colors.background.subtle,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  genderOptionSelected: {
    borderColor: Colors.brand.primary,
    backgroundColor: Colors.brand.primary + '08',
  },
  countryOption: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
    borderRadius: 16,
    backgroundColor: Colors.background.subtle,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  countryOptionSelected: {
    borderColor: Colors.brand.primary,
    backgroundColor: Colors.brand.primary + '08',
  },
  genderOptionContent: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  countryOptionContent: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  countryFlag: {
    fontSize: 24,
    marginRight: 12,
  },
  countryTextContainer: {
    flex: 1,
  },
  countryName: {
    fontSize: 16,
    color: Colors.text.primary,
    fontWeight: '500',
  },
  countryCode: {
    fontSize: 14,
    color: Colors.text.tertiary,
    marginTop: 2,
  },
  genderIconContainer: {
    width: 40,
    height: 40,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  genderOptionText: {
    fontSize: 16,
    color: Colors.text.primary,
    fontWeight: '500',
  },
  genderOptionTextSelected: {
    color: Colors.brand.primary,
    fontWeight: '600',
  },
});

export default EditProfile;