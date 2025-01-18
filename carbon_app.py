import streamlit as st
import matplotlib.pyplot as plt

if "total_emissions" not in st.session_state:
    total_emissions = 0
if "electricity_emissions" not in st.session_state:
    electricity_emissions = 0
if "gas_emissions" not in st.session_state:
    gas_emissions = 0
if "car_emissions" not in st.session_state:
    car_emissions = 0
if "public_transport_emissions" not in st.session_state:
    public_transport_emissions = 0
if "air_travel_emissions" not in st.session_state:
    air_travel_emissions = 0
if "food_emissions" not in st.session_state:
    food_emissions = 0
if "household_waste_emissions" not in st.session_state:
    household_waste_emissions = 0

uk_average_emissions = 500  # Replace with actual average monthly household emissions in kg CO2e

st.title("Household Carbon Footprint Calculator")

st.write("This app helps you calculate your household's carbon footprint.")

# --- Navigation ---
st.header("Navigation")
st.markdown("<a href='#calculate-footprint'>Calculate Your Carbon Footprint</a>", unsafe_allow_html=True)
st.markdown("<a href='#take-action'>Take Action to Reduce Your Footprint</a>", unsafe_allow_html=True)
st.markdown("<a href='#my-actions'>My actions</a>", unsafe_allow_html=True)
st.markdown("<a href='#share'>Share Your Results</a>", unsafe_allow_html=True)
st.markdown("<a href='#offset'>Offset The Rest?</a>", unsafe_allow_html=True)

st.header("Calculate Footprint", anchor="calculate-footprint")

st.subheader("Home Energy")


# Number of bedrooms
num_bedrooms = st.number_input("Enter the number of bedrooms in your house:", min_value=1, value=1)

# Insulation level
insulation_level = st.selectbox("Select your home's insulation level:", ["Well Insulated", "Average Home", "Poorly Insulated"])

# Estimated electricity and gas consumption based on bedrooms, insulation, and heating source
# From https://www.ofgem.gov.uk/average-gas-and-electricity-usage

# Base consumption values
base_electricity_consumption = {
    "Well Insulated": [1800/12, 2700/12, 4100/12],
    "Average Home": [1800/12, 2700/12, 4100/12],
    "Poorly Insulated": [1800/12, 2700/12, 4100/12],
}

base_gas_consumption = {
    "Well Insulated": [7500/12*0.8, 11500/12*0.8, 17000/12*0.8],
    "Average Home": [7500/12, 11500/12, 17000/12],
    "Poorly Insulated": [7500/12*1.2, 11500/12*1.2, 17000/12*1.2],
}

# Adjust consumption based on heating source
electricity = base_electricity_consumption[insulation_level][min(num_bedrooms - 1, 2)]
gas = base_gas_consumption[insulation_level][min(num_bedrooms - 1, 2)]


st.subheader("Travel")

# Distance unit selection
distance_unit = st.radio("Select your preferred distance unit:", ["Kilometers", "Miles"])

# Car usage
car_type = st.selectbox("Select your car type:", ["Petrol", "Diesel", "Electric", "Hybrid", "None"])

if car_type != "None":
    car_size = st.selectbox("Select your car size:", ["Small", "Medium ", "Large"])
    car_mileage = st.number_input(f"Enter your average monthly car distance ({distance_unit.lower()}):", min_value=0)
    
else:
    car_mileage = 0
    car_size = "Small"

car_type_2 = st.selectbox("Select your second car type:", ["Petrol", "Diesel", "Electric", "Hybrid", "None"])

if car_type_2 != "None":
    car_size_2 = st.selectbox("Select your second car size:", ["Small", "Medium ", "Large"])
    car_mileage_2 = st.number_input(f"Enter your second car average monthly car distance ({distance_unit.lower()}):", min_value=0)

else:
    car_mileage_2 = 0
    car_size_2 = "Small"

# Public transport
rail_transport = st.number_input(f"Enter your average monthly rail distance per-person ({distance_unit.lower()}) :", min_value=0)
bus_transport = st.number_input(f"Enter your average monthly bus distance per-person ({distance_unit.lower()}) :", min_value=0)

# Air travel
air_travel = st.number_input(f"Enter your average monthly air travel distance per-person ({distance_unit.lower()}):", min_value=0)
air_travel_class = st.selectbox("Select your air travel class", ["Economy", "Premium Economy", "Business", "First Class"])

# Adjust mileage based on the selected unit
if distance_unit == "Kilometers":
    car_mileage *= 0.621371  # Convert kilometers to miles
    rail_transport *= 0.621371
    bus_transport *= 0.621371
    air_travel *= 0.621371

    st.write("""
    The emission factors are based on the Department for Energy Security and Net Zero 2024 emissions factors. These are predominantly used by 
    corporations to calculate their employee's carbon emissions to disclose in their annual reports. Overall, these factors are well suited to 
    the UK and, probably, your situation.

    Unsurprisingly, there is a big difference between a small, economical car and and large gas-guzzler. And the gulf is even bigger if you
    decide to travel first-class to the Maldives rather than economy to Aberdeen.
""")

st.subheader("Food")

# Number of people in the house
num_people = st.number_input("Enter the number of people in your household:", min_value=1, value=1)

# Diet type
diet_type = st.selectbox("Select your diet type:", ["Meat-heavy", "Average", "Vegetarian", "Vegan"])

# Food waste
food_waste = st.slider("Estimate the percentage of food you waste:", 0, 100, 25, 5)

st.subheader("Household Waste")

# Household waste

bin_bags = st.number_input("How many large bin bags of unrecycled household waste per week:", min_value=0, value=1)

# Initialize total_emissions in session state

calculate_button = st.button("Calculate Carbon Footprint")


# Emission factors (approximate values based on UK government guidelines)
ELECTRICITY_FACTOR = 0.20  # kg CO2e per kWh, 2024 emissions factor
GAS_FACTOR = 0.18  # kg CO2e per kWh, 2024 emissions factor
RAIL_FACTOR = 0.04*1.6  # kg CO2e per mile, national rail, 2024 emissions factor
BUS_FACTOR = 0.1*1.6 # kg CO2e per mile, average local bus, 2024 emissions factor
MEAT_HEAVY_FACTOR = 2600  # kg CO2e per year, from https://www.ethicalconsumer.org/food-drink/climate-impact-meat-vegetarian-vegan-diets
AVERAGE_DIET_FACTOR = 2000  # kg CO2e per year, from https://www.ethicalconsumer.org/food-drink/climate-impact-meat-vegetarian-vegan-diets
VEGETARIAN_FACTOR = 1390  # kg CO2e per year, from https://www.ethicalconsumer.org/food-drink/climate-impact-meat-vegetarian-vegan-diets
VEGAN_FACTOR = 1000  # kg CO2e per year, from https://www.ethicalconsumer.org/food-drink/climate-impact-meat-vegetarian-vegan-diets
HOUSEHOLD_WASTE_FACTOR = 497 # kg CO2e per tonne, 2024 emissions factor



def calculate_carbon_footprint(electricity, gas, car_type, car_mileage, car_type_2, car_mileage_2, rail_transport, bus_transport, air_travel, diet_type, food_waste, bin_bags):
    """Calculates the household carbon footprint based on user inputs."""

    # Calculate home energy emissions
    electricity_emissions = electricity * ELECTRICITY_FACTOR
    gas_emissions = gas * GAS_FACTOR

    # Calculate travel emissions
    if car_size == "Small":
        PETROL_FACTOR = 0.14
        DIESEL_FACTOR = 0.23
        HYBRID_CAR_FACTOR = 0.18
    elif car_size == "Large":
        PETROL_FACTOR = 0.43
        DIESEL_FACTOR = 0.33
        HYBRID_CAR_FACTOR = 0.25
    else:
        PETROL_FACTOR = 0.25  # kg CO2e per mile, 2024 emissions factor for medium car
        DIESEL_FACTOR = 0.29  # kg CO2e per mile, 2024 emissions factor for medium car
        ELECTRIC_CAR_FACTOR = 0.07  # kg CO2e per mile, 2024 emissions factor for medium car
        HYBRID_CAR_FACTOR = 0.18  # kg CO2e per mile, 2024 emissions factor for medium car
    
    if car_type == "Petrol":
        car_emissions = car_mileage_2 * PETROL_FACTOR
    elif car_type == "Diesel":
        car_emissions = car_mileage_2 * DIESEL_FACTOR
    elif car_type == "Electric":
        car_emissions = car_mileage_2 * ELECTRIC_CAR_FACTOR
    elif car_type == "Hybrid":
        car_emissions = car_mileage_2 * HYBRID_CAR_FACTOR
    else:
        car_emissions = 0

    if car_size_2 == "Small":
        PETROL_FACTOR = 0.14
        DIESEL_FACTOR = 0.23
        HYBRID_CAR_FACTOR = 0.18
    elif car_size_2 == "Large":
        PETROL_FACTOR = 0.43
        DIESEL_FACTOR = 0.33
        HYBRID_CAR_FACTOR = 0.25
    else:
        PETROL_FACTOR = 0.25  # kg CO2e per mile, 2024 emissions factor for medium car
        DIESEL_FACTOR = 0.29  # kg CO2e per mile, 2024 emissions factor for medium car
        ELECTRIC_CAR_FACTOR = 0.07  # kg CO2e per mile, 2024 emissions factor for medium car
        HYBRID_CAR_FACTOR = 0.18  # kg CO2e per mile, 2024 emissions factor for medium car
    
    if car_type_2 == "Petrol":
        car_emissions += car_mileage_2 * PETROL_FACTOR
    elif car_type_2 == "Diesel":
        car_emissions += car_mileage_2 * DIESEL_FACTOR
    elif car_type_2 == "Electric":
        car_emissions += car_mileage_2 * ELECTRIC_CAR_FACTOR
    elif car_type_2 == "Hybrid":
        car_emissions += car_mileage_2 * HYBRID_CAR_FACTOR

    if air_travel_class == "Premium Economy":
        AIR_TRAVEL_FACTOR = 0.32 # long-haul, to/from UK
    elif air_travel_class == "Business":
        AIR_TRAVEL_FACTOR = 0.58 # long-haul, to/from UK
    elif air_travel_class == "First Class":
        AIR_TRAVEL_FACTOR = 0.80 # long-haul, to/from UK
    else:
        AIR_TRAVEL_FACTOR = 0.18  # kg CO2e per mile, 2024 emissions factor for average economy class domestic flight

    air_travel_emissions = air_travel * AIR_TRAVEL_FACTOR * num_people

    public_transport_emissions = rail_transport * RAIL_FACTOR + bus_transport * BUS_FACTOR

    # Calculate food emissions
    if diet_type == "Meat-heavy":
        food_emissions = MEAT_HEAVY_FACTOR / 12  # Monthly emissions
    elif diet_type == "Average":
        food_emissions = AVERAGE_DIET_FACTOR / 12
    elif diet_type == "Vegetarian":
        food_emissions = VEGETARIAN_FACTOR / 12
    else:
        food_emissions = VEGAN_FACTOR / 12

    # Adjust food emissions for waste
    food_emissions *= (1 + food_waste / 100)
    food_emissions *= num_people

    # Calculate household waste

    household_waste_emissions = HOUSEHOLD_WASTE_FACTOR * 0.01 * bin_bags * 4.2 # 10kg per bag, 4.2 weeks per month

    # Calculate total emissions
    total_emissions = (
        electricity_emissions
        + gas_emissions
        + car_emissions
        + public_transport_emissions
        + air_travel_emissions
        + food_emissions
        + household_waste_emissions
    )

    return total_emissions, electricity_emissions, gas_emissions, car_emissions, public_transport_emissions, air_travel_emissions, food_emissions, household_waste_emissions

# Calculate and display results when the button is clicked
if calculate_button:

    total_emissions, electricity_emissions, gas_emissions, car_emissions, public_transport_emissions, air_travel_emissions, food_emissions, household_waste_emissions = calculate_carbon_footprint(
        electricity, gas, car_type, car_mileage, car_type_2, car_mileage_2, rail_transport, bus_transport, air_travel, diet_type, food_waste, bin_bags
    )

    # Set original emissions calculation to original variables
    st.session_state.original_total_emissions = total_emissions
    st.session_state.original_electricity_emissions = electricity_emissions
    st.session_state.original_gas_emissions = gas_emissions
    st.session_state.original_car_emissions = car_emissions
    st.session_state.original_public_transport_emissions = public_transport_emissions
    st.session_state.original_air_travel_emissions = air_travel_emissions
    st.session_state.original_food_emissions = food_emissions
    st.session_state.original_household_waste_emissions = household_waste_emissions

    st.write("## Your estimated monthly carbon footprint is:", round(total_emissions, 2), "kg CO2e")

    # Display a breakdown of emissions by category
    st.write("**Breakdown by category:**")
    st.write("- Home energy:", round(electricity_emissions + gas_emissions, 2), "kg CO2e")
    st.write("- Travel:", round(car_emissions + public_transport_emissions + air_travel_emissions, 2), "kg CO2e")
    st.write("- Food:", round(food_emissions, 2), "kg CO2e")
    st.write("- Household waste:", round(household_waste_emissions, 2), "kg CO2e")

    # Compare to UK average
    st.write("**Comparison to UK average:**")
    st.write(
        "Your estimated carbon footprint is",
        round(total_emissions / uk_average_emissions * 100, 2),
        "% of the UK average monthly household emissions.",
    )

    # Create a bar chart
    fig, ax = plt.subplots(figsize=(8, 6))  # Adjust figure size
    bars = ax.bar(["Your Household", "UK Average"], [total_emissions, uk_average_emissions], color=["skyblue", "lightgray"])  # Add colors
    
    # Add data labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}', 
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    ax.set_ylabel("Monthly CO2e Emissions (kg)", fontsize=12)
    ax.set_title("Carbon Footprint Comparison", fontsize=14)
    ax.tick_params(axis='x', labelsize=10)  # Adjust x-axis tick label size
    ax.spines['top'].set_visible(False)  # Remove top spine
    ax.spines['right'].set_visible(False)  # Remove right spine
    st.pyplot(fig)

    st.info("""
    **Note:** The emission factors and average household emissions used in this calculator are based on approximate values and publicly available data. 
    For the most accurate and up-to-date information, please refer to the official UK government websites 
    (Department for Energy Security and Net Zero, BEIS, DEFRA) and reputable research publications.
""")



st.header("Take Action to Reduce Your Footprint", anchor="take-action")

st.write("Explore how changes in your behavior can impact your carbon footprint:")

# --- Home Energy ---
st.subheader("Home Energy")
reduce_electricity = st.checkbox("Reduce electricity consumption (e.g., switch to energy-efficient appliances, use less lighting)")
if reduce_electricity:
    electricity_reduction = st.slider("Estimated reduction in electricity consumption (%)", 0, 100, 10)

green_electricity = st.checkbox("Buy your electricity from a green tariff")    

reduce_gas = st.checkbox("Reduce gas consumption (e.g., improve insulation, lower thermostat)")
if reduce_gas:
    gas_reduction = st.slider("Estimated reduction in gas consumption (%)", 0, 100, 10)

# --- Travel ---
st.subheader("Travel")
reduce_car = st.checkbox("Reduce car usage (e.g., walk, cycle, use public transport)")
if reduce_car:
    car_reduction = st.slider("Estimated reduction in car mileage (%)", 0, 100, 10)

reduce_flights = st.checkbox("Reduce air travel")
if reduce_flights:
    flights_reduction = st.slider("Estimated reduction in air travel mileage (%)", 0, 100, 10)

# --- Food ---
st.subheader("Food")
improve_diet = st.checkbox("Improve diet (e.g., reduce meat consumption, eat more plant-based foods)")
if improve_diet:
    diet_improvement = st.selectbox("Select your new diet type:", ["Meat-heavy", "Average", "Vegetarian", "Vegan"])

reduce_food_waste = st.checkbox("Reduce food waste (e.g., plan meals, store food properly)")
if reduce_food_waste:
    food_waste_reduction = st.slider("Estimated reduction in food waste (%)", 0, 100, 10)

# --- Calculate new footprint ---
if st.button("Calculate New Carbon Footprint"):

    # Adjust input values based on selected actions
    if reduce_electricity:
        electricity *= (1 - electricity_reduction / 100)
    if green_electricity:
        electricity = 0
    if reduce_gas:
        gas *= (1 - gas_reduction / 100)
    if reduce_car:
        car_mileage *= (1 - car_reduction / 100)
    if reduce_flights:
        air_travel *= (1 - flights_reduction / 100)
    if improve_diet:
        diet_original = diet_type
        diet_type = diet_improvement
    if reduce_food_waste:
        food_waste *= (1 - food_waste_reduction / 100)

    # Recalculate footprint
    new_total_emissions, new_electricity_emissions, new_gas_emissions, new_car_emissions, new_public_transport_emissions, new_air_travel_emissions, new_food_emissions, new_household_waste_emissions = calculate_carbon_footprint(
        electricity, gas, car_type, car_mileage, car_type_2, car_mileage_2, rail_transport, bus_transport, air_travel, diet_type, food_waste, bin_bags
    )

    st.write("## Your new estimated monthly carbon footprint is:", round(new_total_emissions, 2), "kg CO2e")

    # Display a breakdown of emissions by category
    st.write("**Breakdown by category:**")
    st.write("- Home energy:", round(new_electricity_emissions + new_gas_emissions, 2), "kg CO2e. Originally:", round(st.session_state.original_electricity_emissions + st.session_state.original_gas_emissions, 2), "kg CO2e")
    st.write("- Travel:", round(new_car_emissions + new_public_transport_emissions + air_travel_emissions, 2), "kg CO2e")
    st.write("- Food:", round(new_food_emissions, 2), "kg CO2e")
    st.write("- Household waste:", round(new_household_waste_emissions, 2), "kg CO2e")

    # Compare to UK average
    st.write("**Comparison to UK average:**")
    st.write(
        "Your estimated carbon footprint is",
        round(new_total_emissions / uk_average_emissions * 100, 2),
        "% of the UK average monthly household emissions.",
    )

    # Create comparison bar chart
    # Create a bar chart
    fig, ax = plt.subplots(figsize=(8, 6))  # Adjust figure size

    # Define category labels and colors
    categories = ["Home Energy", "Travel", "Food", "Waste"]
    colors = ["skyblue", "lightgreen", "lightcoral", "gold"]

    # Stacked bar for original emissions
    ax.bar(
        "Original",
        st.session_state.original_electricity_emissions + st.session_state.original_gas_emissions,
        label=categories[0],
        color=colors[0],
    )
    ax.bar(
        "Original",
        st.session_state.original_car_emissions + st.session_state.original_public_transport_emissions + st.session_state.original_air_travel_emissions,
        bottom=st.session_state.original_electricity_emissions + st.session_state.original_gas_emissions,
        label=categories[1],
        color=colors[1],
    )
    ax.bar(
        "Original",
        st.session_state.original_food_emissions,
        bottom=st.session_state.original_electricity_emissions
        + st.session_state.original_gas_emissions
        + st.session_state.original_car_emissions
        + st.session_state.original_public_transport_emissions
        + st.session_state.original_air_travel_emissions,
        label=categories[2],
        color=colors[2],
    )

    ax.bar(
        "Reduced",
        new_electricity_emissions + new_gas_emissions,
        color=colors[0],
    )
    ax.bar(
        "Reduced",
        new_car_emissions + new_public_transport_emissions + new_air_travel_emissions,
        bottom=new_electricity_emissions + new_gas_emissions,
         color=colors[1],
    )
    ax.bar(
        "Reduced",
        new_food_emissions,
        bottom=new_electricity_emissions
        + new_gas_emissions
        + new_car_emissions
        + new_public_transport_emissions
        + new_air_travel_emissions,
        color=colors[2],
    )
    
    # Add data labels on top of bars
    ax.set_ylabel("Monthly CO2e Emissions (kg)", fontsize=12)
    ax.set_title("Comparison of Original vs. Reduced Footprint", fontsize=14)
    ax.legend()
    ax.tick_params(axis='x', labelsize=10)  # Adjust x-axis tick label size
    ax.spines['top'].set_visible(False)  # Remove top spine
    ax.spines['right'].set_visible(False)  # Remove right spine
    st.pyplot(fig)

# --- Make note of your actions
st.header("Take note of your actions", anchor="my-actions")

st.write("My actions to reduce my carbon emissions are:-")

if reduce_electricity:
    st.write("* I will reduce my electricity usage by ", round(electricity_reduction, 2), "percent. Your next step might be to see what the [Energy Saving Trust](https://energysavingtrust.org.uk/hub/quick-tips-to-save-energy/) has as quick tips and pointers to get you started.")
if reduce_gas:
    st.write("* I will reduce my gas usage by ", round(gas_reduction, 2), "percent")
if green_electricity:
    st.write("* I will move to a 100 percent green electricity provider or tariff. Your next step might be to find the best green electricity provider according to [Which](https://www.which.co.uk/reviews/energy-companies/article/energy-companies/which-energy-survey-results-ajqM43e6ycY8)")
if reduce_car:
    st.write("* I will use my car", round(car_reduction, 2), "percent less. Your next step might be to ask if your company offers a cycle to work scheme. This will reduce the cost of buying a bike, which can either get you to work (and, bonus, it's great for body and mind) or to the nearest public transport. Consider also lift-sharing with your colleague to make the commute more fun and save you money.")
if reduce_flights:
    st.write("* I will go", round(flights_reduction, 2), "percent less far on flights. Your next step might be to explore the website [Flight Free](https://flightfree.co.uk/)")

if improve_diet:
    st.write("* I will go from a", diet_original, "diet to a ", diet_improvement, "diet. Your next step might be to explore low-meat or vegetarian cookbooks for interesting and tasty new recipes (it's not all bland tofu and self-righteousness from here on out) e.g. [Food For Life](https://thehappyfoodie.co.uk/books/the-food-for-life-cookbook-100-recipes-created-with-zoe/)")
if reduce_food_waste:
    st.write("* I will reduce my food waste by ", food_waste_reduction, "percent")

# --- Social Sharing ---
st.header("Share Your Results", anchor="share")

# Construct the message to share
message = f"I've worked out how to reduce my carbon footprint from {round(st.session_state.original_total_emissions, 2)} kg CO2e to just {round(new_total_emissions, 2)} kg CO2e! Check out this app to calculate yours and learn how to reduce it:"

# Twitter share link
twitter_link = f"https://twitter.com/intent/tweet?text={message}%20%23carbonfootprint%20%23sustainability"
st.markdown(f"[Share on Twitter]({twitter_link})")

# Instagram share link (Note: This will only work if the user is on a mobile device)
instagram_link = f"https://www.instagram.com/?url=YOUR_APP_URL&text={message}"  # Replace YOUR_APP_URL with the actual URL of your app
st.markdown(f"[Share on Instagram]({instagram_link})")

# Facebook share link
facebook_link = f"https://www.facebook.com/sharer/sharer.php?u=YOUR_APP_URL&quote={message}"  # Replace YOUR_APP_URL with the actual URL of your app
st.markdown(f"[Share on Facebook]({facebook_link})")