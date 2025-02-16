import RPi.GPIO as GPIO
import pygame
import time
import openai
import os

# ---------------------
# CONFIGURATION
# ---------------------

# GPIO pin setup for the 5 push buttons (Binary Input)
BUTTON_PINS = [26, 19, 13, 6, 5]  # Corrected button GPIOs

# GPIO pin setup for Joystick (Directional Controls)
JOYSTICK_LEFT = 16    # Backspace
JOYSTICK_RIGHT = 20   # Confirm Character (Action)
JOYSTICK_UP = 21      # Toggle Keyboard Mode (Alphabet <-> Numbers)
JOYSTICK_DOWN = 19    # New Line
JOYSTICK_PRESS = 13   # Enter (Speak text)

# Speaker Output
SPEAKER_PIN = 12  # For future external audio handling

# ---------------------
# CHARACTER MAPS
# ---------------------

# Alphabet Mode (Default)
ALPHABET_MODE = {
    0b00001: 'A', 0b00010: 'B', 0b00011: 'C', 0b00100: 'D',
    0b00101: 'E', 0b00110: 'F', 0b00111: 'G', 0b01000: 'H',
    0b01001: 'I', 0b01010: 'J', 0b01011: 'K', 0b01100: 'L',
    0b01101: 'M', 0b01110: 'N', 0b01111: 'O', 0b10000: 'P',
    0b10001: 'Q', 0b10010: 'R', 0b10011: 'S', 0b10100: 'T',
    0b10101: 'U', 0b10110: 'V', 0b10111: 'W', 0b11000: 'X',
    0b11001: 'Y', 0b11010: 'Z', 0b11011: ' ',  # Space
}

# Number Mode
NUMBER_MODE = {
    0b00001: '1', 0b00010: '2', 0b00011: '3', 0b00100: '4',
    0b00101: '5', 0b00110: '6', 0b00111: '7', 0b01000: '8',
    0b01001: '9', 0b01010: '0', 0b01011: '.', 0b01100: ',',
    0b01101: '?', 0b01110: '!', 0b01111: '-', 0b10000: '+',
    0b10001: '=', 0b10010: '*', 0b10011: '/', 0b10100: '@',
    0b10101: '#', 0b10110: '&', 0b10111: '(', 0b11000: ')',
    0b11001: '%', 0b11010: '$', 0b11011: ' ',  # Space
}

# Default keyboard mode (Starts in Alphabet Mode)
current_keyboard = ALPHABET_MODE

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
for pin in BUTTON_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for pin in [JOYSTICK_LEFT, JOYSTICK_RIGHT, JOYSTICK_UP, JOYSTICK_DOWN, JOYSTICK_PRESS]:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(SPEAKER_PIN, GPIO.OUT)

# ---------------------
# DISPLAY SETUP (LCD)
# ---------------------
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 320  # Adjust for your LCD size
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font(None, 40)

typed_text = ""  # Stores user input
current_char = ""  # Stores the selected character before confirmation
uppercase_mode = False  # Toggle Upper/Lowercase

# ---------------------
# FUNCTION TO READ BINARY INPUT
# ---------------------
def read_binary_input():
    """Reads the state of all 5 buttons and converts it into a 5-bit binary number."""
    binary_value = 0
    for i, pin in enumerate(BUTTON_PINS):
        if GPIO.input(pin) == GPIO.HIGH:
            binary_value |= (1 << i)
    return binary_value

# ---------------------
# FUNCTION TO DISPLAY TEXT ON LCD
# ---------------------
def update_display():
    """Updates the LCD screen with the current typed text and preview character."""
    screen.fill((0, 0, 0))  # Clear screen
    preview_text = f"Current: {current_char}" if current_char else "No Input"
    keyboard_mode_text = "Mode: Alphabet" if current_keyboard == ALPHABET_MODE else "Mode: Numbers"
    
    typed_text_display = font.render(typed_text, True, (255, 255, 255))
    preview_display = font.render(preview_text, True, (200, 200, 200))
    mode_display = font.render(keyboard_mode_text, True, (100, 200, 100))

    screen.blit(typed_text_display, (10, 100))
    screen.blit(preview_display, (10, 150))
    screen.blit(mode_display, (10, 200))
    pygame.display.flip()

# ---------------------
# FUNCTION TO CONVERT TEXT TO SPEECH
# ---------------------
def speak_text(text):
    """Converts text to speech using OpenAI API."""
    try:
        openai.api_key = "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"
        response = openai.Audio.create(model="tts-1", text=text, voice="alloy")
        with open("output.mp3", "wb") as f:
            f.write(response["audio"])
        os.system(f"mpg321 -a {SPEAKER_PIN} output.mp3")  # Play audio
    except Exception as e:
        print(f"TTS Error: {e}")

# ---------------------
# MAIN LOOP
# ---------------------
try:
    while True:
        binary_value = read_binary_input()
        
        # Declare global variables inside the loop
        typed_text, current_char, uppercase_mode, current_keyboard

        # If binary value matches a character, store it in the preview area
        if binary_value in current_keyboard:
            current_char = current_keyboard[binary_value]
            if uppercase_mode:
                current_char = current_char.upper()  # Apply uppercase if active
            update_display()

        # Joystick Right (Confirm & Add Character)
        if GPIO.input(JOYSTICK_RIGHT) == GPIO.HIGH and current_char:
            typed_text += current_char
            current_char = ""  # Reset preview
            update_display()
            time.sleep(0.2)  # Debounce

        # Joystick Left (Backspace)
        if GPIO.input(JOYSTICK_LEFT) == GPIO.HIGH and typed_text:
            typed_text = typed_text[:-1]
            update_display()
            time.sleep(0.2)  # Debounce

        # Joystick Up (Toggle Keyboard Mode)
        if GPIO.input(JOYSTICK_UP) == GPIO.HIGH:
            current_keyboard = ALPHABET_MODE if current_keyboard == NUMBER_MODE else NUMBER_MODE
            update_display()
            time.sleep(0.2)  # Debounce

        # Joystick Down (New Line)
        if GPIO.input(JOYSTICK_DOWN) == GPIO.HIGH:
            typed_text += "\n"
            update_display()
            time.sleep(0.2)  # Debounce

        # Joystick Press (Enter - Speak Text)
        if GPIO.input(JOYSTICK_PRESS) == GPIO.HIGH and typed_text:
            speak_text(typed_text)
            time.sleep(0.5)  # Prevent accidental repeat

        time.sleep(0.1)  # Prevent rapid input detection

except KeyboardInterrupt:
    print("Shutting down...")
    GPIO.cleanup()
