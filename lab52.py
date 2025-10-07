import RPi.GPIO as GPIO
import time
import math

# --- Configuration ---
# List of GPIO pin numbers for the 12 LEDs (BCM numbering)
# NOTE: Adjust these pin numbers to match your actual hardware setup
LED_PINS = [17, 27, 22, 10, 9, 11, 5, 6, 13, 19] 

PWM_FREQUENCY = 500  # Base PWM frequency in Hz
SINE_FREQUENCY = 0.2 # f in the equation, 0.2 Hz
PHASE_STEP = math.pi / 11 # Phase lag increment (ϕ) between successive LEDs

# --- Setup ---
GPIO.setmode(GPIO.BCM)

# 1. Initialize PWM objects for all LEDs
pwm_leds = []
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, PWM_FREQUENCY)
    pwm.start(0)  # Start with 0% duty cycle
    pwm_leds.append(pwm)

# Get the start time for the phase calculation
start_time = time.time()

print(f"Starting 12-LED travelling wave fade with f={SINE_FREQUENCY} Hz and phase step={PHASE_STEP:.4f} rad.")
print("Press Ctrl+C to stop.")

# --- Main Loop ---
try:
    while True:
        # 1. Get current system time and elapsed time (t)
        current_time = time.time()
        t = current_time - start_time
        
        # 2. Iterate through all 12 LEDs
        for k, pwm_led in enumerate(pwm_leds):
            # Calculate the total phase lag (ϕ_k) for the current LED (k)
            # k=0 is the first LED (ϕ_0 = 0)
            # k=1 is the second LED (ϕ_1 = π/11)
            # ...
            # k=11 is the last LED (ϕ_11 = 11 * π/11 = π)
            phase_lag = k * PHASE_STEP
            
            # 3. Calculate the argument of the sine function: (2πft - ϕ_k)
            sine_argument = (2 * math.pi * SINE_FREQUENCY * t) - phase_lag
            
            # 4. Calculate brightness (B_k) based on B = (sin(argument))²
            # B_k ranges from 0.0 to 1.0
            brightness_ratio = math.sin(sine_argument) ** 2
            
            # 5. Convert brightness ratio (0.0 - 1.0) to PWM Duty Cycle (0 - 100)
            duty_cycle = brightness_ratio * 100
            
            # 6. Update the PWM duty cycle for the current LED
            pwm_led.ChangeDutyCycle(duty_cycle)

        # The loop runs as fast as possible, updating all 12 LEDs non-blockingly.

except KeyboardInterrupt:
    # Stop all PWM objects and clean up GPIO settings on exit
    print("\nStopping LED wave and cleaning up.")
    for pwm in pwm_leds:
        pwm.stop()
    GPIO.cleanup()
