import streamlit as st
import random

# Set page config
st.set_page_config(page_title="3-Digit Number Guessing Game", page_icon="🎲")

# Initialize session state variables
if 'secret_number' not in st.session_state:
    # Generate a random 3-digit number
    st.session_state.secret_number = str(random.randint(100, 999))
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'guess_history' not in st.session_state:
    st.session_state.guess_history = []

def check_guess(guess, secret):
    feedback = []
    # First pass: mark correct positions
    for i in range(3):
        if guess[i] == secret[i]:
            feedback.append('👌')
        else:
            feedback.append('')
    
    # Second pass: mark correct numbers in wrong positions
    for i in range(3):
        if feedback[i] == '':  # Only check positions not already marked as correct
            if guess[i] in secret:
                # Count how many times this digit appears in the secret number
                secret_count = secret.count(guess[i])
                # Count how many times this digit appears in the feedback
                feedback_count = feedback.count('👍')
                if feedback_count < secret_count:
                    feedback[i] = '👍'
                else:
                    feedback[i] = '❌'
            else:
                feedback[i] = '❌'
    
    return ''.join(feedback)

# Title and instructions
st.title("🎲 3-Digit Number Guessing Game")
st.write("I'm thinking of a 3-digit number. Can you guess it?")
st.write("❌ = Wrong number")
st.write("👍 = Correct number, wrong position")
st.write("👌 = Correct number and position")
st.write("You have 10 attempts to guess the number!")

# Display number of attempts and remaining attempts
remaining_attempts = 10 - st.session_state.attempts
st.write(f"Attempts: {st.session_state.attempts}/10 (Remaining: {remaining_attempts})")

# Create input field for user's guess
user_guess = st.text_input("Enter your guess (3 digits):", max_chars=3)

# Create a button to submit guess
if st.button("Submit Guess"):
    if st.session_state.attempts >= 10:
        st.error("Game Over! You've used all 10 attempts.")
        st.write(f"The secret number was: {st.session_state.secret_number}")
        st.session_state.game_over = True
    elif not user_guess.isdigit() or len(user_guess) != 3:
        st.error("Please enter a valid 3-digit number!")
    else:
        st.session_state.attempts += 1
        feedback = check_guess(user_guess, st.session_state.secret_number)
        
        # Add guess to history
        st.session_state.guess_history.append((user_guess, feedback))
        
        if feedback == '👌👌👌':
            st.success(f"🎉 Congratulations! You found the number in {st.session_state.attempts} attempts!")
            st.session_state.game_over = True
            st.balloons()
        elif st.session_state.attempts >= 10:
            st.error("Game Over! You've used all 10 attempts.")
            st.write(f"The secret number was: {st.session_state.secret_number}")
            st.session_state.game_over = True
        
        # Display guess history
        st.write("Guess History:")
        for guess, result in st.session_state.guess_history:
            st.write(f"{guess} → {result}")

# Add a reset button
if st.button("Reset Game"):
    st.session_state.secret_number = str(random.randint(100, 999))
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.guess_history = []
    st.rerun()