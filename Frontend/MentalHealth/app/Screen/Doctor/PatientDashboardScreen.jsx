import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  Alert,
  RefreshControl,
  Animated,
  Dimensions,
  SafeAreaView,
  ActivityIndicator
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Colors from '../../assets/colors';
import { Fonts, FontFallbacks } from '../../assets/config/fonts';

const { width, height } = Dimensions.get('window');
const API_BASE_URL = 'http://172.26.151.96:8000';

// Safe font getter function
const getFontStyle = (fontKey) => {
  try {
    return Fonts[fontKey] || FontFallbacks[fontKey];
  } catch (error) {
    console.warn(`Font style ${fontKey} not found, using fallback`);
    return FontFallbacks[fontKey] || FontFallbacks.bodyMedium;
  }
};

const PatientDashboardScreen = ({ navigation, route }) => {
  const [appointments, setAppointments] = useState([]);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [userName, setUserName] = useState('');
  const [userId, setUserId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showDebug, setShowDebug] = useState(__DEV__);

  // Animation values
  const fadeAnim = useState(new Animated.Value(0))[0];
  const slideAnim = useState(new Animated.Value(30))[0];
  const scaleAnim = useState(new Animated.Value(0.95))[0];

  // Helper function to get avatar color
  const getAvatarColor = (index) => {
    const colors = [
      Colors.features.mindfulness,
      Colors.features.meditation,
      Colors.features.journal,
      Colors.brand.primary,
      Colors.accent.coral,
      Colors.accent.teal,
      '#7E57C2',
      '#26A69A',
    ];
    return colors[index % colors.length];
  };

  // Load user data from storage
  const loadUserData = async () => {
    try {
      const userDataString = await AsyncStorage.getItem('userData');
      if (!userDataString) {
        throw new Error('No user data found');
      }

      const userData = JSON.parse(userDataString);
      const currentUserId = userData.id || userData.user_id;
      
      if (!currentUserId) {
        throw new Error('User ID not found in storage');
      }

      setUserId(currentUserId);
      setUserName(userData.get_full_name || userData.name || userData.username || 'User');
      return currentUserId;
    } catch (error) {
      console.error('Error loading user data:', error);
      Alert.alert(
        'Authentication Required',
        'Please login to continue',
        [{ text: 'Login', onPress: () => navigation.navigate('Login') }]
      );
      return null;
    }
  };

  // Fetch appointments from backend
  const fetchAppointments = async () => {
    try {
      setLoading(true);
      setError(null);

      const currentUserId = await loadUserData();
      if (!currentUserId) return;

      console.log('Fetching appointments for user:', currentUserId);
      
      const response = await fetch(`${API_BASE_URL}/api/my-appointments/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          user_id: currentUserId
        }),
      });

      console.log('API Response status:', response.status);

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || data.detail || `HTTP error ${response.status}`);
      }

      if (data.success) {
        console.log(`✅ Found ${data.appointments?.length || 0} appointments`);
        
        const transformedAppointments = (data.appointments || []).map((appointment, index) => ({
          id: appointment.id.toString(),
          appointment_id: appointment.id,
          doctor_name: appointment.doctor_name || 'Dr. Unknown',
          doctor_specialization: appointment.doctor_specialization || 'Mental Health Specialist',
          appointment_date: appointment.appointment_date,
          appointment_time: appointment.appointment_time,
          status: (appointment.status || 'scheduled').toLowerCase(),
          symptoms: appointment.symptoms || 'Mental health consultation',
          doctor_rating: 4.8, // Default - could be added to backend
          doctor_experience: appointment.doctor_experience || '5',
          avatarColor: getAvatarColor(index),
          duration: appointment.duration || '60',
          notes: appointment.notes || '',
          doctor_qualification: appointment.doctor_qualification || '',
          created_at: appointment.created_at || new Date().toISOString(),
        }));

        setAppointments(transformedAppointments);
        
        // Animate in
        Animated.parallel([
          Animated.timing(fadeAnim, {
            toValue: 1,
            duration: 600,
            useNativeDriver: true,
          }),
          Animated.timing(slideAnim, {
            toValue: 0,
            duration: 500,
            useNativeDriver: true,
          }),
          Animated.timing(scaleAnim, {
            toValue: 1,
            duration: 500,
            useNativeDriver: true,
          })
        ]).start();
      } else {
        throw new Error(data.error || 'Failed to fetch appointments');
      }
    } catch (error) {
      console.error('Error fetching appointments:', error);
      setError(error.message);
      
      // In development, load sample data
      if (__DEV__) {
        loadSampleData();
      }
    } finally {
      setLoading(false);
    }
  };

  // Load sample data for development
  const loadSampleData = () => {
    const sampleAppointments = [
      {
        id: '1',
        appointment_id: 1,
        doctor_name: 'Dr. Sarah Johnson',
        doctor_specialization: 'Clinical Psychologist',
        appointment_date: '2024-01-20',
        appointment_time: '14:30:00',
        status: 'confirmed',
        symptoms: 'Anxiety and stress management',
        doctor_rating: 4.9,
        doctor_experience: '12',
        avatarColor: Colors.features.mindfulness,
        duration: '60',
        notes: 'Initial consultation session',
        doctor_qualification: 'PhD in Clinical Psychology',
        created_at: '2024-01-10T10:30:00Z'
      },
      {
        id: '2',
        appointment_id: 2,
        doctor_name: 'Dr. Michael Chen',
        doctor_specialization: 'Psychiatrist',
        appointment_date: '2024-01-18',
        appointment_time: '11:00:00',
        status: 'scheduled',
        symptoms: 'Depression evaluation and therapy',
        doctor_rating: 4.8,
        doctor_experience: '8',
        avatarColor: Colors.features.meditation,
        duration: '45',
        notes: '',
        doctor_qualification: 'MD, Board Certified',
        created_at: '2024-01-09T14:20:00Z'
      },
      {
        id: '3',
        appointment_id: 3,
        doctor_name: 'Dr. Emily Rodriguez',
        doctor_specialization: 'Cognitive Behavioral Therapist',
        appointment_date: '2024-01-15',
        appointment_time: '09:30:00',
        status: 'completed',
        symptoms: 'OCD treatment session',
        doctor_rating: 4.7,
        doctor_experience: '10',
        avatarColor: Colors.features.journal,
        duration: '50',
        notes: 'Follow-up session completed successfully',
        doctor_qualification: 'MSc in Psychology, CBT Certified',
        created_at: '2024-01-08T16:45:00Z'
      },
      {
        id: '4',
        appointment_id: 4,
        doctor_name: 'Dr. Robert Wilson',
        doctor_specialization: 'Trauma Specialist',
        appointment_date: '2024-01-25',
        appointment_time: '16:00:00',
        status: 'scheduled',
        symptoms: 'PTSD therapy session',
        doctor_rating: 4.9,
        doctor_experience: '15',
        avatarColor: Colors.brand.primary,
        duration: '60',
        notes: 'First session scheduled',
        doctor_qualification: 'PhD in Trauma Psychology',
        created_at: '2024-01-11T11:15:00Z'
      }
    ];

    setAppointments(sampleAppointments);
    setUserName('Demo User');
    setUserId('demo-123');
    
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 600,
        useNativeDriver: true,
      }),
      Animated.timing(slideAnim, {
        toValue: 0,
        duration: 500,
        useNativeDriver: true,
      }),
      Animated.timing(scaleAnim, {
        toValue: 1,
        duration: 500,
        useNativeDriver: true,
      })
    ]).start();
  };

  // Initial load
  useEffect(() => {
    fetchAppointments();
  }, []);

  // Handle refresh
  const onRefresh = useCallback(async () => {
    setRefreshing(true);
    await fetchAppointments();
    setRefreshing(false);
  }, []);

  // Check if can join video call
  const canJoinCall = (appointment) => {
    try {
      const appointmentDateTime = new Date(`${appointment.appointment_date}T${appointment.appointment_time}`);
      const now = new Date();
      const timeDiff = appointmentDateTime.getTime() - now.getTime();
      const hoursDiff = timeDiff / (1000 * 60 * 60);
      
      return appointment.status === 'confirmed' && hoursDiff >= -0.5 && hoursDiff <= 1;
    } catch (error) {
      return false;
    }
  };

  // Get appointment statistics
  const getStats = () => {
    const upcoming = appointments.filter(apt => 
      apt.status === 'scheduled' || apt.status === 'confirmed'
    ).length;
    const completed = appointments.filter(apt => 
      apt.status === 'completed'
    ).length;
    const cancelled = appointments.filter(apt => 
      apt.status === 'cancelled'
    ).length;

    return {
      upcoming,
      completed,
      cancelled,
      total: appointments.length,
    };
  };

  // Filter appointments based on selected filter
  const filteredAppointments = appointments.filter(appointment => {
    if (selectedFilter === 'all') return true;
    return appointment.status === selectedFilter;
  });

  // Format date
  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { 
        weekday: 'short',
        month: 'short', 
        day: 'numeric',
        year: 'numeric'
      });
    } catch (error) {
      return dateString;
    }
  };

  // Format time
  const formatTime = (timeString) => {
    try {
      const time = timeString.includes('T') 
        ? new Date(timeString)
        : new Date(`2000-01-01T${timeString}`);
      
      return time.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
      });
    } catch (error) {
      return timeString;
    }
  };

  // Get status color
  const getStatusColor = (status) => {
    const colors = {
      scheduled: Colors.status.warning,
      confirmed: Colors.status.success,
      completed: Colors.brand.primary,
      cancelled: Colors.status.error,
      pending: Colors.text.tertiary,
    };
    return colors[status] || Colors.text.tertiary;
  };

  // Get status display text
  const getStatusDisplay = (status) => {
    const displays = {
      scheduled: 'SCHEDULED',
      confirmed: 'CONFIRMED',
      completed: 'COMPLETED',
      cancelled: 'CANCELLED',
      pending: 'PENDING',
    };
    return displays[status] || status.toUpperCase();
  };

  // Render each appointment card
  const renderAppointment = ({ item, index }) => (
    <Animated.View
      style={[
        styles.appointmentCard,
        {
          opacity: fadeAnim,
          transform: [
            { translateY: slideAnim },
            { scale: scaleAnim }
          ]
        }
      ]}
    >
      <View style={styles.cardHeader}>
        <View style={styles.doctorInfo}>
          <LinearGradient
            colors={[item.avatarColor, Colors.ui.overlay]}
            style={styles.avatar}
          >
            <Text style={styles.avatarText}>
              {item.doctor_name
                .split(' ')
                .slice(1, 3)
                .map(n => n[0])
                .join('')
                .toUpperCase()}
            </Text>
          </LinearGradient>
          <View style={styles.doctorDetails}>
            <Text style={styles.doctorName} numberOfLines={1}>
              {item.doctor_name}
            </Text>
            <Text style={styles.specialization}>
              {item.doctor_specialization}
            </Text>
            <View style={styles.ratingContainer}>
              <Ionicons name="star" size={14} color={Colors.accent.coral} />
              <Text style={styles.ratingText}>
                {item.doctor_rating} • {item.doctor_experience} years exp
              </Text>
            </View>
          </View>
        </View>
        <View style={[styles.statusBadge, { backgroundColor: getStatusColor(item.status) }]}>
          <Text style={styles.statusText}>{getStatusDisplay(item.status)}</Text>
        </View>
      </View>

      <View style={styles.cardBody}>
        <Text style={styles.symptoms} numberOfLines={2}>
          {item.symptoms}
        </Text>

        <View style={styles.appointmentDetails}>
          <View style={styles.detailRow}>
            <Ionicons name="calendar-outline" size={16} color={Colors.text.tertiary} />
            <Text style={styles.detailText}>
              {formatDate(item.appointment_date)}
            </Text>
          </View>

          <View style={styles.detailRow}>
            <Ionicons name="time-outline" size={16} color={Colors.text.tertiary} />
            <Text style={styles.detailText}>
              {formatTime(item.appointment_time)}
            </Text>
            {item.duration && (
              <Text style={styles.durationText}> • {item.duration} mins</Text>
            )}
          </View>
        </View>
      </View>

      <View style={styles.cardFooter}>
        {canJoinCall(item) ? (
          <View style={styles.primaryActions}>
            <TouchableOpacity 
              style={styles.joinButton}
              onPress={() => navigation.navigate('VideoCall', { 
                appointmentId: item.appointment_id,
                doctorName: item.doctor_name 
              })}
            >
              <LinearGradient
                colors={Colors.gradients.primary}
                style={styles.joinButtonGradient}
              >
                <Ionicons name="videocam" size={18} color={Colors.text.inverted} />
                <Text style={styles.joinButtonText}>Join Session</Text>
              </LinearGradient>
            </TouchableOpacity>
            
            <TouchableOpacity 
              style={styles.chatButton}
              onPress={() => navigation.navigate('Chat', { 
                appointmentId: item.appointment_id,
                doctorName: item.doctor_name 
              })}
            >
              <Ionicons name="chatbubble-ellipses" size={18} color={Colors.brand.primary} />
              <Text style={styles.chatButtonText}>Message</Text>
            </TouchableOpacity>
          </View>
        ) : item.status === 'scheduled' ? (
          <TouchableOpacity 
            style={styles.secondaryButton}
            onPress={() => navigation.navigate('Reschedule', { appointmentId: item.appointment_id })}
          >
            <Ionicons name="calendar" size={16} color={Colors.brand.primary} />
            <Text style={styles.secondaryButtonText}>Reschedule</Text>
          </TouchableOpacity>
        ) : item.status === 'completed' && item.notes ? (
          <TouchableOpacity 
            style={styles.secondaryButton}
            onPress={() => navigation.navigate('AppointmentDetail', { appointment: item })}
          >
            <Ionicons name="document-text" size={16} color={Colors.brand.primary} />
            <Text style={styles.secondaryButtonText}>View Session Notes</Text>
          </TouchableOpacity>
        ) : item.status === 'cancelled' ? (
          <TouchableOpacity 
            style={[styles.secondaryButton, { borderColor: Colors.status.error }]}
            onPress={() => {}}
          >
            <Ionicons name="close-circle" size={16} color={Colors.status.error} />
            <Text style={[styles.secondaryButtonText, { color: Colors.status.error }]}>
              Cancelled
            </Text>
          </TouchableOpacity>
        ) : null}
      </View>
    </Animated.View>
  );

  // Handle logout
  const handleLogout = async () => {
    Alert.alert(
      'Logout',
      'Are you sure you want to logout?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Logout',
          style: 'destructive',
          onPress: async () => {
            try {
              await AsyncStorage.removeItem('userData');
              navigation.reset({
                index: 0,
                routes: [{ name: 'Login' }],
              });
            } catch (error) {
              console.error('Logout error:', error);
            }
          }
        }
      ]
    );
  };

  // Handle find therapists
  const handleFindTherapists = () => {
    navigation.navigate('SearchTherapists');
  };

  // Stats
  const stats = getStats();

  // Render loading state
  if (loading && appointments.length === 0) {
    return (
      <SafeAreaView style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={Colors.brand.primary} />
        <Text style={styles.loadingText}>Loading your appointments...</Text>
      </SafeAreaView>
    );
  }

  // Render error state
  if (error && appointments.length === 0) {
    return (
      <SafeAreaView style={styles.errorContainer}>
        <Ionicons name="warning-outline" size={64} color={Colors.status.error} />
        <Text style={styles.errorTitle}>Unable to Load Appointments</Text>
        <Text style={styles.errorText}>{error}</Text>
        <TouchableOpacity 
          style={styles.retryButton}
          onPress={fetchAppointments}
        >
          <Text style={styles.retryButtonText}>Try Again</Text>
        </TouchableOpacity>
        {__DEV__ && (
          <TouchableOpacity 
            style={[styles.retryButton, { marginTop: 12, backgroundColor: Colors.brand.primary }]}
            onPress={loadSampleData}
          >
            <Text style={styles.retryButtonText}>Use Sample Data</Text>
          </TouchableOpacity>
        )}
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <LinearGradient
        colors={Colors.gradients.primary}
        style={styles.header}
      >
        <View style={styles.headerTop}>
          <View>
            <Text style={styles.greeting}>Welcome back, {userName}!</Text>
            <Text style={styles.subGreeting}>Your mental health journey matters</Text>
          </View>
          <TouchableOpacity onPress={handleLogout} style={styles.logoutButton}>
            <Ionicons name="log-out-outline" size={22} color={Colors.text.inverted} />
          </TouchableOpacity>
        </View>

        <View style={styles.statsOverview}>
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>{stats.upcoming}</Text>
            <Text style={styles.statLabel}>Upcoming</Text>
          </View>
          <View style={styles.statDivider} />
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>{stats.completed}</Text>
            <Text style={styles.statLabel}>Completed</Text>
          </View>
          <View style={styles.statDivider} />
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>{stats.total}</Text>
            <Text style={styles.statLabel}>Total</Text>
          </View>
        </View>
      </LinearGradient>

      {/* Filter Tabs */}
      <View style={styles.filterContainer}>
        <FlatList
          horizontal
          showsHorizontalScrollIndicator={false}
          data={[
            { key: 'all', label: 'All Sessions' },
            { key: 'scheduled', label: 'Scheduled' },
            { key: 'confirmed', label: 'Confirmed' },
            { key: 'completed', label: 'Completed' },
            { key: 'cancelled', label: 'Cancelled' },
          ]}
          renderItem={({ item }) => (
            <TouchableOpacity
              style={[
                styles.filterTab,
                selectedFilter === item.key && styles.filterTabActive
              ]}
              onPress={() => setSelectedFilter(item.key)}
            >
              <Text style={[
                styles.filterText,
                selectedFilter === item.key && styles.filterTextActive
              ]}>
                {item.label}
              </Text>
            </TouchableOpacity>
          )}
          keyExtractor={(item) => item.key}
          contentContainerStyle={styles.filterList}
        />
      </View>

      {/* Appointments List */}
      <View style={styles.listContainer}>
        <View style={styles.listHeader}>
          <Text style={styles.sectionTitle}>Your Therapy Sessions</Text>
          <Text style={styles.sectionSubtitle}>
            {filteredAppointments.length} session{filteredAppointments.length !== 1 ? 's' : ''}
          </Text>
        </View>

        <FlatList
          data={filteredAppointments}
          renderItem={renderAppointment}
          keyExtractor={(item) => `${item.id}-${item.status}`}
          refreshControl={
            <RefreshControl 
              refreshing={refreshing} 
              onRefresh={onRefresh}
              colors={[Colors.brand.primary]}
              tintColor={Colors.brand.primary}
              progressBackgroundColor={Colors.neutrals.background}
            />
          }
          showsVerticalScrollIndicator={false}
          contentContainerStyle={styles.listContent}
          ListEmptyComponent={
            <View style={styles.emptyState}>
              <Ionicons name="calendar-outline" size={64} color={Colors.text.tertiary} />
              <Text style={styles.emptyText}>No sessions found</Text>
              <Text style={styles.emptySubtext}>
                {selectedFilter === 'all' 
                  ? "Take the first step towards better mental health" 
                  : `No ${selectedFilter} sessions found`
                }
              </Text>
              <TouchableOpacity 
                style={styles.findTherapistsButton}
                onPress={handleFindTherapists}
              >
                <LinearGradient
                  colors={Colors.gradients.primary}
                  style={styles.findTherapistsGradient}
                >
                  <Ionicons name="search" size={20} color={Colors.text.inverted} />
                  <Text style={styles.findTherapistsText}>Find Therapists</Text>
                </LinearGradient>
              </TouchableOpacity>
            </View>
          }
        />
      </View>

      {/* Floating Action Button */}
      <TouchableOpacity 
        style={styles.floatingButton}
        onPress={handleFindTherapists}
        activeOpacity={0.8}
      >
        <LinearGradient
          colors={Colors.gradients.primary}
          style={styles.floatingButtonGradient}
        >
          <Ionicons name="add" size={28} color={Colors.text.inverted} />
        </LinearGradient>
      </TouchableOpacity>

      {/* Debug Info (Development Only) */}
      {__DEV__ && showDebug && (
        <TouchableOpacity 
          style={styles.debugPanel}
          onPress={() => setShowDebug(false)}
          activeOpacity={0.8}
        >
          <View style={styles.debugContent}>
            <Text style={styles.debugTitle}>Debug Info</Text>
            <Text style={styles.debugText}>User ID: {userId}</Text>
            <Text style={styles.debugText}>API: {API_BASE_URL}</Text>
            <Text style={styles.debugText}>Appointments: {appointments.length}</Text>
            <Text style={styles.debugText}>Status: {loading ? 'Loading' : error ? 'Error' : 'Ready'}</Text>
          </View>
        </TouchableOpacity>
      )}

      {/* Show Debug Button (Development Only) */}
      {__DEV__ && !showDebug && (
        <TouchableOpacity 
          style={styles.showDebugButton}
          onPress={() => setShowDebug(true)}
        >
          <Text style={styles.showDebugText}>Debug</Text>
        </TouchableOpacity>
      )}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.neutrals.background,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: Colors.neutrals.background,
  },
  loadingText: {
    ...getFontStyle('bodyLarge'),
    color: Colors.text.secondary,
    marginTop: 16,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: Colors.neutrals.background,
    padding: 20,
  },
  errorTitle: {
    ...getFontStyle('heading2'),
    color: Colors.text.primary,
    marginTop: 16,
    marginBottom: 8,
  },
  errorText: {
    ...getFontStyle('bodyMedium'),
    color: Colors.text.secondary,
    textAlign: 'center',
    marginBottom: 24,
  },
  retryButton: {
    backgroundColor: Colors.status.error,
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 12,
  },
  retryButtonText: {
    ...getFontStyle('buttonPrimary'),
    color: Colors.text.inverted,
  },
  header: {
    paddingTop: 60,
    paddingBottom: 24,
    paddingHorizontal: 20,
    borderBottomLeftRadius: 24,
    borderBottomRightRadius: 24,
  },
  headerTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 24,
  },
  greeting: {
    ...getFontStyle('heading2'),
    color: Colors.text.inverted,
    marginBottom: 4,
  },
  subGreeting: {
    ...getFontStyle('bodyLarge'),
    color: Colors.neutrals.white,
    opacity: 0.9,
  },
  logoutButton: {
    padding: 8,
    borderRadius: 8,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
  },
  statsOverview: {
    flexDirection: 'row',
    backgroundColor: Colors.ui.overlay,
    borderRadius: 20,
    padding: 16,
    width: '100%',
    justifyContent: 'space-around',
  },
  statItem: {
    alignItems: 'center',
    flex: 1,
  },
  statNumber: {
    ...getFontStyle('heading2'),
    color: Colors.text.inverted,
    marginBottom: 4,
  },
  statLabel: {
    ...getFontStyle('bodySmall'),
    color: Colors.text.inverted,
    opacity: 0.9,
  },
  statDivider: {
    width: 1,
    backgroundColor: 'rgba(255,255,255,0.3)',
  },
  filterContainer: {
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: Colors.neutrals.border,
  },
  filterList: {
    paddingHorizontal: 20,
  },
  filterTab: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    marginRight: 8,
    backgroundColor: Colors.neutrals.surfaceLow,
  },
  filterTabActive: {
    backgroundColor: Colors.brand.primary,
  },
  filterText: {
    ...getFontStyle('bodySmall'),
    color: Colors.text.tertiary,
    fontWeight: '500',
  },
  filterTextActive: {
    color: Colors.text.inverted,
  },
  listContainer: {
    flex: 1,
  },
  listHeader: {
    paddingHorizontal: 20,
    paddingVertical: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  sectionTitle: {
    ...getFontStyle('heading2'),
    color: Colors.text.primary,
  },
  sectionSubtitle: {
    ...getFontStyle('bodyMedium'),
    color: Colors.text.tertiary,
  },
  listContent: {
    paddingHorizontal: 20,
    paddingBottom: 100,
  },
  appointmentCard: {
    backgroundColor: Colors.neutrals.surface,
    borderRadius: 20,
    padding: 20,
    marginBottom: 16,
    shadowColor: Colors.ui.shadowDark,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 5,
    borderWidth: 1,
    borderColor: Colors.neutrals.border,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  doctorInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  avatar: {
    width: 56,
    height: 56,
    borderRadius: 28,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  avatarText: {
    color: Colors.text.inverted,
    ...getFontStyle('heading3'),
    fontWeight: 'bold',
  },
  doctorDetails: {
    flex: 1,
  },
  doctorName: {
    ...getFontStyle('heading3'),
    color: Colors.text.primary,
    marginBottom: 2,
  },
  specialization: {
    ...getFontStyle('bodySmall'),
    color: Colors.text.secondary,
    marginBottom: 6,
  },
  ratingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  ratingText: {
    ...getFontStyle('bodySmall'),
    color: Colors.text.tertiary,
    marginLeft: 4,
  },
  statusBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    minWidth: 90,
    alignItems: 'center',
  },
  statusText: {
    color: Colors.text.inverted,
    fontSize: 10,
    ...getFontStyle('bodySmall'),
    fontWeight: 'bold',
    letterSpacing: 0.5,
  },
  cardBody: {
    marginBottom: 16,
  },
  symptoms: {
    ...getFontStyle('bodyLarge'),
    color: Colors.text.secondary,
    marginBottom: 16,
    lineHeight: 22,
  },
  appointmentDetails: {
    backgroundColor: Colors.neutrals.surfaceLow,
    borderRadius: 12,
    padding: 12,
  },
  detailRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  detailText: {
    ...getFontStyle('bodyMedium'),
    color: Colors.text.secondary,
    marginLeft: 8,
    flex: 1,
  },
  durationText: {
    ...getFontStyle('bodyMedium'),
    color: Colors.text.tertiary,
  },
  cardFooter: {
    marginTop: 4,
  },
  primaryActions: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 8,
  },
  joinButton: {
    flex: 2,
    borderRadius: 12,
    overflow: 'hidden',
  },
  joinButtonGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
  },
  joinButtonText: {
    ...getFontStyle('buttonPrimary'),
    marginLeft: 8,
  },
  chatButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    borderWidth: 1,
    borderColor: Colors.neutrals.border,
    borderRadius: 12,
    backgroundColor: Colors.neutrals.surface,
  },
  chatButtonText: {
    ...getFontStyle('buttonSecondary'),
    color: Colors.brand.primary,
    marginLeft: 6,
  },
  secondaryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    borderWidth: 1,
    borderColor: Colors.neutrals.border,
    borderRadius: 12,
    backgroundColor: Colors.neutrals.surface,
  },
  secondaryButtonText: {
    ...getFontStyle('buttonSecondary'),
    color: Colors.brand.primary,
    marginLeft: 6,
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 80,
    paddingHorizontal: 40,
  },
  emptyText: {
    ...getFontStyle('heading2'),
    color: Colors.text.secondary,
    marginTop: 24,
    marginBottom: 8,
  },
  emptySubtext: {
    ...getFontStyle('bodyLarge'),
    color: Colors.text.tertiary,
    textAlign: 'center',
    marginBottom: 32,
    lineHeight: 22,
  },
  findTherapistsButton: {
    borderRadius: 16,
    overflow: 'hidden',
    width: '100%',
    maxWidth: 280,
  },
  findTherapistsGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 24,
    paddingVertical: 18,
  },
  findTherapistsText: {
    ...getFontStyle('buttonPrimary'),
    marginLeft: 10,
  },
  floatingButton: {
    position: 'absolute',
    right: 20,
    bottom: 30,
    borderRadius: 30,
    overflow: 'hidden',
    shadowColor: Colors.ui.shadowDark,
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.3,
    shadowRadius: 12,
    elevation: 10,
  },
  floatingButtonGradient: {
    width: 64,
    height: 64,
    borderRadius: 32,
    justifyContent: 'center',
    alignItems: 'center',
  },
  debugPanel: {
    position: 'absolute',
    top: 100,
    left: 20,
    right: 20,
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    borderRadius: 12,
    padding: 16,
  },
  debugContent: {
    backgroundColor: 'transparent',
  },
  debugTitle: {
    color: Colors.text.inverted,
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  debugText: {
    color: Colors.text.inverted,
    fontSize: 12,
    marginBottom: 4,
  },
  showDebugButton: {
    position: 'absolute',
    top: 100,
    left: 20,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  showDebugText: {
    color: Colors.text.inverted,
    fontSize: 12,
    fontWeight: '500',
  },
});

export default PatientDashboardScreen;