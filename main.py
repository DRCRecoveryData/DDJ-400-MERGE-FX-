#include <Control_Surface.h>

// Instantiate a USBMIDI_Interface object
USBMIDI_Interface midi;

// Instantiate an AbsoluteEncoderWithButton object for the MERGE FX PARAMETER L knob and button
AbsoluteEncoderWithButton mergeFXParamL{36, MIDI_CHANNEL_1, AbsoluteEncoder::RelativeCC, 61, MIDI_CHANNEL_1};

// Instantiate a RingLEDs object for the LED ring around the MERGE FX PARAMETER L knob
RingLEDs<12> mergeFXParamLLEDs{
  {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}, // LED pins
  MIDI_CHANNEL_1, // MIDI channel number
  0, // Minimum LED value
  127, // Maximum LED value
  RingLEDs<12>::Clockwise, // LED direction (clockwise)
  false, // Use linear brightness (false for logarithmic brightness)
  false // Invert LED brightness (false for normal brightness)
};

// Pin number for the button connected to the MERGE FX PRESET L button
const int MERGE_FX_PRESET_L_BUTTON_PIN = 2;

void setup() {
  // Begin MIDI communication
  Control_Surface.begin();

  // Turn on all LED segments when power is turned on
  for (int i = 0; i < 12; i++) {
    mergeFXParamLLEDs.set(i, 127);
  }
}

void loop() {
  // Update the state of the MERGE FX PARAMETER L knob, button, and LED ring
  mergeFXParamL.update();
  mergeFXParamLLEDs.update();

  // Send MIDI message and set LED feedback when knob is turned
  int knobPosition = mergeFXParamL.getPosition();
  midi.sendControlChange(36, knobPosition, MIDI_CHANNEL_1);
  for (int i = 0; i < 12; i++) {
    int LEDValue = map(knobPosition, -8192, 8191, 0, 127); // Map knob position to LED value (range -8192 to 8191)
    mergeFXParamLLEDs.set(i, LEDValue); // Set LED segment brightness
  }

  // Toggle slow/fast adjustment mode when button is pressed
  if (mergeFXParamL.buttonFell()) {
    midi.sendNoteOn(97, 127, MIDI_CHANNEL_1); // Button pressed, send MIDI Note On message
  }
  if (mergeFXParamL.buttonRose()) {
    midi.sendNoteOff(97, 127, MIDI_CHANNEL_1); // Button released, send MIDI Note Off message
  }

  // Flash LED ring slowly or quickly when knob is turned
  int flashSpeed = map(knobPosition, -8192, 8191, 127, 0); // Map knob position to LED flash speed (range -8192 to 8191)
  mergeFXParamLLEDs.setBrightness(0, flashSpeed); // Set LED segment brightness to flash speed
  for (int i = 1; i < 12; i++) {
    mergeFXParamLLEDs.setBrightness(i, 0); // Turn off all other LED segments
  }

  // Detect button press and send MIDI Note On message for MERGE FX PRESET L button
  if (digitalRead(MERGE_FX_PRESET_L_BUTTON_PIN) == HIGH) {
    midi.sendNoteOn(86, 127, MIDI_CHANNEL_
