import time
import random
import streamlit as st
import pandas as pd
import altair as alt

# Paragraphs for the typing test
paragraphs = [
    "In today’s rapidly evolving world, technology continues to advance at an astonishing pace.",
    "The concept of artificial intelligence has long been a topic of intrigue and fascination.",
    "The issue of climate change remains one of the most pressing challenges of our time.",
    "Education has always been a cornerstone of human development, but in the 21st century, the role of education is rapidly shifting.",
    "The field of space exploration has entered an exciting new era."
]

# Streamlit App
st.title("Typing Speed Test")

# Initialize session state for paragraph and timing
if "paragraph" not in st.session_state:
    st.session_state["paragraph"] = None
if "start_time" not in st.session_state:
    st.session_state["start_time"] = None
if "submitted" not in st.session_state:
    st.session_state["submitted"] = False

# Start Typing Test Button
if not st.session_state["paragraph"]:
    if st.button("Start Typing"):
        st.session_state["paragraph"] = random.choice(paragraphs)
        st.session_state["start_time"] = time.time()
        st.session_state["submitted"] = False

# Display paragraph and input text area after starting the test
if st.session_state["paragraph"]:
    st.subheader("Type the following paragraph:")
    st.write(f"> {st.session_state['paragraph']}")
    
    user_input = st.text_area("Start typing below:", height=150)

    # Submit Button
    if st.button("Submit") and not st.session_state["submitted"]:
        st.session_state["submitted"] = True
        end_time = time.time()

        # Calculate results
        time_taken = end_time - st.session_state["start_time"]
        words_typed = len(user_input.split())
        wpm = (words_typed / time_taken) * 60 if time_taken > 0 else 0
        original_text = st.session_state["paragraph"]
        total_characters = len(original_text)
        correct_characters = sum(1 for o, t in zip(original_text, user_input) if o == t)
        accuracy = (correct_characters / total_characters) * 100 if total_characters > 0 else 0

        # Feedback with color-coded text (character by character)
        feedback = []
        for i, char in enumerate(original_text):
            if i < len(user_input):
                if char == user_input[i]:
                    feedback.append(f"<span style='color:green'>{char}</span>")
                else:
                    feedback.append(f"<span style='color:red'>{char}</span>")
            else:
                feedback.append(f"<span style='color:gray'>{char}</span>")
        feedback_text = "".join(feedback)

        # Display results
        st.success(f"Typing Speed: {wpm:.2f} WPM")
        st.info(f"Time Taken: {time_taken:.2f} seconds")
        st.warning(f"Accuracy: {accuracy:.2f}%")

        # Feedback section
        st.subheader("Your Typed Text with Feedback:")
        st.markdown(f"<p style='line-height:1.6'>{feedback_text}</p>", unsafe_allow_html=True)

        # Charts
        st.subheader("Performance Charts")

        # Bar chart for WPM and Accuracy
        performance_data = pd.DataFrame({
            "Metric": ["WPM", "Accuracy"],
            "Value": [wpm, accuracy]
        })
        st.bar_chart(performance_data.set_index("Metric"))

        # Line chart for typing speed over time (simulated for now)
        simulated_speed = [wpm * (i / 10) for i in range(1, 11)]
        st.line_chart(pd.DataFrame({
            "Time Interval": [f"{i * time_taken / 10:.1f}s" for i in range(1, 11)],
            "WPM": simulated_speed
        }).set_index("Time Interval"))

        # Pie chart for character correctness
        character_data = pd.DataFrame({
            "Category": ["Correct Characters", "Incorrect Characters", "Missing Characters"],
            "Count": [
                correct_characters,
                sum(1 for o, t in zip(original_text, user_input) if o != t),
                max(0, total_characters - len(user_input))
            ]
        })

        # Render pie chart
        pie_chart = alt.Chart(character_data).mark_arc().encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(field="Category", type="nominal"),
            tooltip=["Category", "Count"]
        )
        st.altair_chart(pie_chart, use_container_width=True)
