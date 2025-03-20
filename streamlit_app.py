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

    # Stat categories
    physical_stats = ["Agi", "Per", "Str", "Tou"]
    mental_stats = ["Cha", "Int", "Wil", "Wis"]
    combat_stats = ["Mel", "Ran"]

    # Initialize session state to store stat values and SRs
    if "stats" not in st.session_state:
        st.session_state.stats = {stat: {"value": 50, "SR": 5, "adjustment": 0, "total_SR": 5} for stat in physical_stats + mental_stats + combat_stats}

    # Initialize session state for roll confirmation
    if "roll_confirmation" not in st.session_state:
        st.session_state.roll_confirmation = {stat: False for stat in physical_stats + mental_stats + combat_stats}

    # Input fields for stats
    st.header("Enter Stat Values")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Physical Stats")
        for stat in physical_stats:
            # Create a row for the stat input and SR display
            row = st.columns([0.3, 0.2, 0.5])  # 30% width for input, 20% for SR, 50% for button
            with row[0]:
                # Input box for stat value (30% width)
                st.session_state.stats[stat]["value"] = st.number_input(
                    f"{stat}:", 
                    min_value=1, 
                    max_value=100, 
                    value=st.session_state.stats[stat]["value"], 
                    key=f"{stat}_value",
                    step=1,
                    label_visibility="collapsed"  # Hide the label to save space
                )
            with row[1]:
                # Display SR to the right of the input box
                st.session_state.stats[stat]["SR"] = get_SR(st.session_state.stats[stat]["value"])
                st.write(f"SR: {st.session_state.stats[stat]['SR']}")
            with row[2]:
                # Roll button next to the stat
                if st.button(f"Roll for {stat}", key=f"{stat}_button"):
                    st.session_state.roll_confirmation[stat] = True

            # Confirmation box after selecting roll method
            if st.session_state.roll_confirmation[stat]:
                st.write(f"Rolling for {stat}...")
                roll_option = st.radio(
                    f"Roll option for {stat}",
                    ["Generate Roll", "Input Roll"],
                    key=f"{stat}_roll_option"
                )
                if roll_option == "Generate Roll":
                    if st.button(f"Confirm Roll for {stat}", key=f"{stat}_confirm_generate"):
                        die_result = roll_d100()
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
                        st.session_state.roll_confirmation[stat] = False
                else:
                    die_result = st.number_input(
                        f"Enter rolled number for {stat}:",
                        min_value=1,
                        max_value=100,
                        value=50,
                        key=f"{stat}_manual_roll"
                    )
                    if st.button(f"Confirm Roll for {stat}", key=f"{stat}_confirm_input"):
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
                        st.session_state.roll_confirmation[stat] = False

    with col2:
        st.subheader("Mental Stats")
        for stat in mental_stats:
            # Create a row for the stat input and SR display
            row = st.columns([0.3, 0.2, 0.5])  # 30% width for input, 20% for SR, 50% for button
            with row[0]:
                # Input box for stat value (30% width)
                st.session_state.stats[stat]["value"] = st.number_input(
                    f"{stat}:", 
                    min_value=1, 
                    max_value=100, 
                    value=st.session_state.stats[stat]["value"], 
                    key=f"{stat}_value",
                    step=1,
                    label_visibility="collapsed"  # Hide the label to save space
                )
            with row[1]:
                # Display SR to the right of the input box
                st.session_state.stats[stat]["SR"] = get_SR(st.session_state.stats[stat]["value"])
                st.write(f"SR: {st.session_state.stats[stat]['SR']}")
            with row[2]:
                # Roll button next to the stat
                if st.button(f"Roll for {stat}", key=f"{stat}_button"):
                    st.session_state.roll_confirmation[stat] = True

            # Confirmation box after selecting roll method
            if st.session_state.roll_confirmation[stat]:
                st.write(f"Rolling for {stat}...")
                roll_option = st.radio(
                    f"Roll option for {stat}",
                    ["Generate Roll", "Input Roll"],
                    key=f"{stat}_roll_option"
                )
                if roll_option == "Generate Roll":
                    if st.button(f"Confirm Roll for {stat}", key=f"{stat}_confirm_generate"):
                        die_result = roll_d100()
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
                        st.session_state.roll_confirmation[stat] = False
                else:
                    die_result = st.number_input(
                        f"Enter rolled number for {stat}:",
                        min_value=1,
                        max_value=100,
                        value=50,
                        key=f"{stat}_manual_roll"
                    )
                    if st.button(f"Confirm Roll for {stat}", key=f"{stat}_confirm_input"):
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
                        st.session_state.roll_confirmation[stat] = False

    with col3:
        st.subheader("Combat Stats")
        for stat in combat_stats:
            # Create a row for the stat input and SR display
            row = st.columns([0.3, 0.2, 0.5])  # 30% width for input, 20% for SR, 50% for button
            with row[0]:
                # Input box for stat value (30% width)
                st.session_state.stats[stat]["value"] = st.number_input(
                    f"{stat}:", 
                    min_value=1, 
                    max_value=100, 
                    value=st.session_state.stats[stat]["value"], 
                    key=f"{stat}_value",
                    step=1,
                    label_visibility="collapsed"  # Hide the label to save space
                )
            with row[1]:
                # Display SR to the right of the input box
                st.session_state.stats[stat]["SR"] = get_SR(st.session_state.stats[stat]["value"])
                st.write(f"SR: {st.session_state.stats[stat]['SR']}")
            with row[2]:
                # Roll button next to the stat
                if st.button(f"Roll for {stat}", key=f"{stat}_button"):
                    st.session_state.roll_confirmation[stat] = True

            # Confirmation box after selecting roll method
            if st.session_state.roll_confirmation[stat]:
                st.write(f"Rolling for {stat}...")
                roll_option = st.radio(
                    f"Roll option for {stat}",
                    ["Generate Roll", "Input Roll"],
                    key=f"{stat}_roll_option"
                )
                if roll_option == "Generate Roll":
                    if st.button(f"Confirm Roll for {stat}", key=f"{stat}_confirm_generate"):
                        die_result = roll_d100()
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
                        st.session_state.roll_confirmation[stat] = False
                else:
                    die_result = st.number_input(
                        f"Enter rolled number for {stat}:",
                        min_value=1,
                        max_value=100,
                        value=50,
                        key=f"{stat}_manual_roll"
                    )
                    if st.button(f"Confirm Roll for {stat}", key=f"{stat}_confirm_input"):
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
                        st.session_state.roll_confirmation[stat] = False

    # Display the last result
    if "last_result" in st.session_state:
        st.header("Roll Result")
        st.write(f"**Stat:** {st.session_state.last_result['stat']}")
        st.write(f"**Entered Stat:** {st.session_state.last_result['entered_stat']}")
        st.write(f"**SR:** {st.session_state.last_result['SR']}")
        st.write(f"**You rolled:** {st.session_state.last_result['die_result']}")
        st.write(f"**Adjustment:** {st.session_state.last_result['adjustment']}")
        st.write(f"**Total SR:** {st.session_state.last_result['total_SR']}")

if __name__ == "__main__":
    main()
