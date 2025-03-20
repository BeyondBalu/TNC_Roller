import streamlit as st
import random

def roll_d100():
    """Simulate rolling a 100-sided die."""
    return random.randint(1, 100)

def calculate_final_result(die_result, entered_stat):
    """Calculate the adjustment based on the difference between the die result and the entered stat."""
    difference = die_result - entered_stat
    final_result = 0
    
    if difference < -10:
        # For every full 10 below the entered stat, increase final result by +1
        final_result = abs(difference) // 10
    elif difference > 10:
        # For every full 10 above the entered stat, decrease final result by -1
        final_result = -(difference // 10)
    
    return final_result

def get_SR(entered_stat):
    """Calculate the SR (Skill Rating) as the tens digit of the entered stat."""
    return (entered_stat // 10) % 10

def main():
    st.title("Stat Roller with SR Adjustment")

    # Initialize session state to store results
    if "last_result" not in st.session_state:
        st.session_state.last_result = None

    # Initialize session state for rolling methodology
    if "roll_method" not in st.session_state:
        st.session_state.roll_method = "Generated Roll"  # Default to Generated Roll

    # Initialize session state for manual roll input
    if "manual_roll" not in st.session_state:
        st.session_state.manual_roll = 50  # Default value for manual roll

    # Stat categories
    stats = {
        "Physical Stats": ["Agi", "Per", "Str", "Tou"],
        "Mental Stats": ["Cha", "Int", "Wil", "Wis"],
        "Combat Stats": ["Mel", "Ran"],
    }

    # Initialize session state to store stat values and SRs
    if "stats" not in st.session_state:
        st.session_state.stats = {stat: {"value": 50, "SR": 5} for category in stats.values() for stat in category}

    # Left column for stat inputs and results
    with st.sidebar:
        st.header("Results")
        if st.session_state.last_result:
            st.write(f"**Stat:** {st.session_state.last_result['stat']}")
            st.write(f"**Entered Stat:** {st.session_state.last_result['entered_stat']}")
            st.write(f"**SR:** {st.session_state.last_result['SR']}")
            st.write(f"**You rolled:** {st.session_state.last_result['die_result']}")
            st.write(f"**Adjustment:** {st.session_state.last_result['adjustment']}")
            st.write(f"**Total SR:** {st.session_state.last_result['total_SR']}")
        else:
            st.write("No roll results yet. Roll for a stat to see the results here.")

    # Main content area for stat inputs
    st.header("Enter Stat Values")

    # Rolling methodology section
    st.subheader("Rolling Methodology")
    st.session_state.roll_method = st.radio(
        "Select rolling method:",
        ["Generated Roll", "Input Roll"],
        key="roll_method"
    )

    # If "Input Roll" is selected, show a field box for entering the rolled number
    if st.session_state.roll_method == "Input Roll":
        st.session_state.manual_roll = st.number_input(
            "Enter rolled number:",
            min_value=1,
            max_value=100,
            value=st.session_state.manual_roll,
            key="manual_roll"
        )

    # Display stat inputs with SR values and roll buttons
    for category, stat_list in stats.items():
        st.subheader(category)
        for stat in stat_list:
            col1, col2, col3 = st.columns([0.2, 0.6, 0.2])  # 20% width for SR, 60% for input, 20% for button
            with col1:
                # Display SR to the left of the input box
                st.session_state.stats[stat]["SR"] = get_SR(st.session_state.stats[stat]["value"])
                st.write(f"**SR:** {st.session_state.stats[stat]['SR']}")
            with col2:
                # Input box for stat value
                st.session_state.stats[stat]["value"] = st.number_input(
                    f"{stat}:", 
                    min_value=1, 
                    max_value=100, 
                    value=st.session_state.stats[stat]["value"], 
                    key=f"{stat}_value",
                    step=1,
                    label_visibility="visible"  # Show the label
                )
            with col3:
                # Roll button for the stat
                if st.button(f"Roll for {stat}", key=f"{stat}_button"):
                    if st.session_state.roll_method == "Generated Roll":
                        die_result = roll_d100()
                    else:
                        die_result = st.session_state.manual_roll
                    # Calculate adjustment
                    adjustment = calculate_final_result(die_result, st.session_state.stats[stat]["value"])
                    # Update adjustment and total SR
                    st.session_state.stats[stat]["adjustment"] = adjustment
                    st.session_state.stats[stat]["total_SR"] = st.session_state.stats[stat]["SR"] + adjustment
                    # Store the result for display
                    st.session_state.last_result = {
                        "stat": stat,
                        "entered_stat": st.session_state.stats[stat]["value"],
                        "SR": st.session_state.stats[stat]["SR"],
                        "die_result": die_result,
                        "adjustment": adjustment,
                        "total_SR": st.session_state.stats[stat]["total_SR"]
                    }

if __name__ == "__main__":
    main()
