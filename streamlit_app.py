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

    # Initialize session state to store skills
    if "skills" not in st.session_state:
        st.session_state.skills = []

    # Create a three-column layout
    col1, col2, col3 = st.columns([0.3, 0.4, 0.3])  # Left: Roll Confirmation/Results, Middle: Stats, Right: Skills

    with col2:
        # Input fields for stats
        st.header("Enter Stat Values")

        # Physical Stats
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
                    # Store the selected stat in session state
                    st.session_state.selected_stat = stat
                    # Reset the roll confirmation flag
                    st.session_state.roll_confirmed = False
                    # Reset the roll result flag
                    st.session_state.show_result = False

        # Mental Stats
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
                    # Store the selected stat in session state
                    st.session_state.selected_stat = stat
                    # Reset the roll confirmation flag
                    st.session_state.roll_confirmed = False
                    # Reset the roll result flag
                    st.session_state.show_result = False

        # Combat Stats
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
                    # Store the selected stat in session state
                    st.session_state.selected_stat = stat
                    # Reset the roll confirmation flag
                    st.session_state.roll_confirmed = False
                    # Reset the roll result flag
                    st.session_state.show_result = False

    with col1:
        # Roll Confirmation or Roll Result
        if "selected_stat" in st.session_state:
            stat = st.session_state.selected_stat
            if not st.session_state.get("roll_confirmed", False):
                # Show Roll Confirmation
                st.header("Roll Confirmation")
                st.write(f"You are rolling for **{stat}**.")
                
                # Option to input or generate rolled number
                roll_option = st.radio(
                    f"Roll option for {stat}",
                    ["Generate Roll", "Input Roll"],
                    key=f"{stat}_roll_option"
                )
                
                if roll_option == "Generate Roll":
                    if st.button("Confirm Roll", key=f"{stat}_confirm_generate"):
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
                        # Set roll confirmation flag
                        st.session_state.roll_confirmed = True
                        # Set show result flag
                        st.session_state.show_result = True
                else:
                    die_result = st.number_input(
                        f"Enter rolled number for {stat}:",
                        min_value=1,
                        max_value=100,
                        value=50,
                        key=f"{stat}_manual_roll"
                    )
                    if st.button("Confirm Roll", key=f"{stat}_confirm_input"):
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
                        # Set roll confirmation flag
                        st.session_state.roll_confirmed = True
                        # Set show result flag
                        st.session_state.show_result = True

            # Show Roll Result
            if st.session_state.get("show_result", False):
                st.header("Roll Result")
                st.write(f"**Stat:** {st.session_state.last_result['stat']}")
                st.write(f"**Entered Stat:** {st.session_state.last_result['entered_stat']}")
                st.write(f"**SR:** {st.session_state.last_result['SR']}")
                st.write(f"**You rolled:** {st.session_state.last_result['die_result']}")
                st.write(f"**Adjustment:** {st.session_state.last_result['adjustment']}")
                st.write(f"**Total SR:** {st.session_state.last_result['total_SR']}")

    with col3:
        # Skills Section
        st.header("Skills")

        # Input for Skill Name
        skill_name = st.text_input("Skill Name", key="skill_name")

        # Dropdown to select a stat
        selected_stat = st.selectbox(
            "Select Stat",
            physical_stats + mental_stats + combat_stats,
            key="selected_stat_skill"
        )

        # Skill Level Selection
        skill_level = st.radio(
            "Skill Level",
            ["Novice (+2)", "Expert (+4)", "Master (+6)"],
            key="skill_level"
        )

        # Misc Value Input
        misc_value = st.number_input(
            "Misc Value",
            min_value=0,
            value=0,
            key="misc_value"
        )

        # Calculate Skill SR
        if selected_stat and skill_level and misc_value is not None:
            # Get the selected stat's SR
            stat_SR = st.session_state.stats[selected_stat]["SR"]
            # Get the skill level bonus
            skill_level_bonus = int(skill_level.split("+")[1].replace(")", ""))
            # Calculate Skill SR
            skill_SR = stat_SR + skill_level_bonus + misc_value

            # Display Skill SR
            st.write(f"**Skill SR:** {skill_SR}")

            # Save the skill to session state
            if st.button("Save Skill", key="save_skill"):
                st.session_state.skills.append({
                    "name": skill_name,
                    "stat": selected_stat,
                    "level": skill_level,
                    "misc": misc_value,
                    "SR": skill_SR
                })

        # Display Saved Skills
        if st.session_state.skills:
            st.subheader("Saved Skills")
            for skill in st.session_state.skills:
                st.write(f"**{skill['name']}** (Stat: {skill['stat']}, Level: {skill['level']}, Misc: {skill['misc']}, SR: {skill['SR']})")

if __name__ == "__main__":
    main()
