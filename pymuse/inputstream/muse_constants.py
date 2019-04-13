MUSE_EEG_ACQUISITION_FREQUENCY = 256
MUSE_ACCELEROMETER_ACQUISITION_FREQUENCY = 52
MUSE_GYROSCOPE_ACQUISITION_FREQUENCY = 52
MUSE_BAND_POWER_ACQUISITION_FREQUENCY = 10
MUSE_HEADBAND_STATUS_ACQUISITION_FREQUENCY = 10
MUSE_MUSCLE_MOVEMENT_ACQUISITION_FREQUENCY = 10
MUSE_BATT_ACQUISITION_FREQUENCY = 10

MUSE_OSC_PATH = {
    'eeg':                  '/*eeg',
    'notch_filtered_eeg':   '/*notch_filtered_eeg',
    'eeg_quantization':     '/*eeg/quantization',

    'acc':                  '/*acc',
    'gyro':                 '/*gyro',

    'delta_absolute':       '/*elements/delta_absolute',
    'theta_absolute':       '/*elements/theta_absolute',
    'alpha_absolute':       '/*elements/alpha_absolute',
    'beta_absolute':        '/*elements/beta_absolute',
    'gamma_absolute':       '/*elements/gamma_absolute',

    'delta_relative':       '/*elements/delta_relative',
    'theta_relative':       '/*elements/theta_relative',
    'alpha_relative':       '/*elements/alpha_relative',
    'beta_relative':        '/*elements/beta_relative',
    'gamma_relative':       '/*elements/gamma_relative',

    'delta_session_score':  '/*elements/delta_session_score',
    'theta_session_score':  '/*elements/theta_session_score',
    'alpha_session_score':  '/*elements/alpha_session_score',
    'beta_session_score':   '/*elements/beta_session_score',
    'gamma_session_score':  '/*elements/gamma_session_score',

    'touching_forehead':    '/*elements/touching_forehead',
    'horseshoe':            '/*elements/horseshoe',
    'is_good':              '/*elements/is_good',

    'blink':                '/*elements/blink',
    'jaw_clench':           '/*elements/jaw_clench',

    'batt':                 '/*batt',
    'drlref':               '/*drlref',
}

MUSE_ACQUISITION_FREQUENCIES = {
    'eeg':                  MUSE_EEG_ACQUISITION_FREQUENCY,
    'notch_filtered_eeg':   MUSE_EEG_ACQUISITION_FREQUENCY,
    'eeg_quantization':     MUSE_EEG_ACQUISITION_FREQUENCY,

    'acc':                  MUSE_ACCELEROMETER_ACQUISITION_FREQUENCY,
    'gyro':                 MUSE_GYROSCOPE_ACQUISITION_FREQUENCY,

    'delta_absolute':       MUSE_BAND_POWER_ACQUISITION_FREQUENCY,
    'theta_absolute':       MUSE_BAND_POWER_ACQUISITION_FREQUENCY,
    'alpha_absolute':       MUSE_BAND_POWER_ACQUISITION_FREQUENCY,
    'beta_absolute':        MUSE_BAND_POWER_ACQUISITION_FREQUENCY,
    'gamma_absolute':       MUSE_BAND_POWER_ACQUISITION_FREQUENCY,

    'delta_relative':       MUSE_BAND_POWER_ACQUISITION_FREQUENCY,
    'theta_relative':       MUSE_BAND_POWER_ACQUISITION_FREQUENCY,
    'alpha_relative':       MUSE_BAND_POWER_ACQUISITION_FREQUENCY,
    'beta_relative':        MUSE_BAND_POWER_ACQUISITION_FREQUENCY,
    'gamma_relative':       MUSE_BAND_POWER_ACQUISITION_FREQUENCY,

    'delta_session_score':  MUSE_BAND_POWER_ACQUISITION_FREQUENCY,
    'theta_session_score':  MUSE_BAND_POWER_ACQUISITION_FREQUENCY,
    'alpha_session_score':  MUSE_BAND_POWER_ACQUISITION_FREQUENCY,
    'beta_session_score':   MUSE_BAND_POWER_ACQUISITION_FREQUENCY,
    'gamma_session_score':  MUSE_BAND_POWER_ACQUISITION_FREQUENCY,

    'touching_forehead':    MUSE_HEADBAND_STATUS_ACQUISITION_FREQUENCY,
    'horseshoe':            MUSE_HEADBAND_STATUS_ACQUISITION_FREQUENCY,
    'is_good':              MUSE_HEADBAND_STATUS_ACQUISITION_FREQUENCY,

    'blink':                MUSE_MUSCLE_MOVEMENT_ACQUISITION_FREQUENCY,
    'jaw_clench':           MUSE_MUSCLE_MOVEMENT_ACQUISITION_FREQUENCY,

    'batt':                 MUSE_BATT_ACQUISITION_FREQUENCY,
    'drlref':               MUSE_EEG_ACQUISITION_FREQUENCY,
}
