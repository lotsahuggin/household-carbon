import streamlit as st
import pandas as pd
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
if "original_total_emissions" not in st.session_state:
    original_total_emissions = 0

uk_average_emissions = 500  # Replace with actual average monthly household emissions in kg CO2e
original_total_emissions = 0 # Initialise to avoid error in sharing section
new_total_emissions = 0
colors = [ "#2364aa", "#17c3b2", "#ffcb77", "#fef9ef", "#ff6b6b", "#a4243b", "#041b15", "#00ff00"]


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

st.subheader("Home Energy", divider="blue")

# Manual or estimated heating and electricity consumption

home_energy_type = st.selectbox("Do you know your gas and electricity consumption in kWh?", ["Yes", "No"])

if home_energy_type == "Yes":
    gas = st.number_input("Enter your annual gas consumption in kWh:", min_value = 1, value = 7500) / 12
    electricity = st.number_input("Enter your annual electricity consumption in kWh:", min_value=1, value = 1800) / 12
    check_solar_panels = st.checkbox("Do you have solar panels that offset some of your electricity consumption?")
    if check_solar_panels:
        solar_panel_modifier = st.slider("How much do solar panels offset your electricity consumption figure above by:", 0, 100, 10, 5)
        electricity = electricity * (1 - solar_panel_modifier / 100)

else:

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


st.subheader("Travel", divider="green")

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

car_type_2 = st.selectbox("Select your second car type:", ["None", "Petrol", "Diesel", "Electric", "Hybrid"])

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
    car_mileage_2 *= 0.621371
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

st.subheader("Food", divider="orange")

# Number of people in the house
num_people = st.number_input("Enter the number of people in your household:", min_value=1, value=1)
num_kids = st.number_input("Of those, how many are children under 12 years old (to work out impact of food choices):", min_value = 0, value = 0)

# Diet type
diet_type = st.selectbox("Select your diet type:", ["Meat-heavy", "Average", "Vegetarian", "Vegan"])
diet_original = diet_type

# Food waste
food_waste = st.slider("Estimate the percentage of food you waste:", 0, 100, 25, 5)

st.subheader("Household Waste", divider="orange")

# Household waste

bin_bags = st.number_input("How many large bin bags of unrecycled household waste per week:", min_value=0, value=1)

st.subheader("Pets", divider = "blue")

# Pets

num_small_pets = 0
num_medium_pets = 0
num_large_pets = 0
pets_check = st.checkbox("Do you own any pets?")

if pets_check:
    num_small_pets = st.number_input("How many cats or small dogs (or equivalent)?", min_value = 0, value = 1)
    num_medium_pets = st.number_input("How many medium-sized dogs (or equivalent)?", min_value = 0, value = 0)
    num_large_pets = st.number_input("How many large dogs (or equivalent)?", min_value = 0, value = 0)

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
SMALL_PETS = 300 # kg per animal https://academic.oup.com/bioscience/article/69/6/467/5486563?login=false]
MEDIUM_PETS = 900
LARGE_PETS = 1400

# UK averages (from https://energyguide.org.uk/average-carbon-footprint-uk/)
ELECTRICITY_UK = 1100 / 12
GAS_UK = 2200 / 12
CAR_UK = 1700 / 12
PUBLIC_TRANSPORT_UK =  "unknown"
AIR_UK = "unknown"
FOOD_UK = AVERAGE_DIET_FACTOR / 12 * (num_people - num_kids / 2) # Assumes children under 12 eat half that of an adult


def calculate_carbon_footprint(electricity, gas, car_type, car_mileage, car_type_2, car_mileage_2, rail_transport, bus_transport, air_travel, diet_type, food_waste, bin_bags, num_small_pets, num_medium_pets, num_large_pets):
    """Calculates the household carbon footprint based on user inputs."""

    # Calculate home energy emissions
    electricity_emissions = electricity * ELECTRICITY_FACTOR
    gas_emissions = gas * GAS_FACTOR

    # Calculate travel emissions
    ELECTRIC_CAR_FACTOR = 0
    ELECTRIC_CAR_FACTOR_2 = 0
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
    
    car_emissions = 0
    if car_type == "Petrol":
        car_emissions = car_mileage * PETROL_FACTOR
    elif car_type == "Diesel":
        car_emissions = car_mileage * DIESEL_FACTOR
    elif car_type == "Electric":
        car_emissions = car_mileage * ELECTRIC_CAR_FACTOR
    elif car_type == "Hybrid":
        car_emissions = car_mileage * HYBRID_CAR_FACTOR
    elif car_type == "None":
        car_emissions = 0

    if car_size_2 == "Small":
        PETROL_FACTOR_2 = 0.14
        DIESEL_FACTOR_2 = 0.23
        HYBRID_CAR_FACTOR_2 = 0.18
    elif car_size_2 == "Large":
        PETROL_FACTOR_2 = 0.43
        DIESEL_FACTOR_2 = 0.33
        HYBRID_CAR_FACTOR_2 = 0.25
    else:
        PETROL_FACTOR_2 = 0.25  # kg CO2e per mile, 2024 emissions factor for medium car
        DIESEL_FACTOR_2 = 0.29  # kg CO2e per mile, 2024 emissions factor for medium car
        ELECTRIC_CAR_FACTOR_2 = 0.07  # kg CO2e per mile, 2024 emissions factor for medium car
        HYBRID_CAR_FACTOR_2 = 0.18  # kg CO2e per mile, 2024 emissions factor for medium car
    
    if car_type_2 == "Petrol":
        car_emissions += car_mileage_2 * PETROL_FACTOR_2
    elif car_type_2 == "Diesel":
        car_emissions += car_mileage_2 * DIESEL_FACTOR_2
    elif car_type_2 == "Electric":
        car_emissions += car_mileage_2 * ELECTRIC_CAR_FACTOR_2
    elif car_type_2 == "Hybrid":
        car_emissions += car_mileage_2 * HYBRID_CAR_FACTOR_2

    if air_travel_class == "Premium Economy":
        AIR_TRAVEL_FACTOR = 0.32 # long-haul, to/from UK
    elif air_travel_class == "Business":
        AIR_TRAVEL_FACTOR = 0.58 # long-haul, to/from UK
    elif air_travel_class == "First Class":
        AIR_TRAVEL_FACTOR = 0.80 # long-haul, to/from UK
    else:
        AIR_TRAVEL_FACTOR = 0.18  # kg CO2e per mile, 2024 emissions factor for average economy class domestic flight

    air_travel_emissions = air_travel * AIR_TRAVEL_FACTOR * num_people

    public_transport_emissions = rail_transport * RAIL_FACTOR * num_people + bus_transport * BUS_FACTOR * num_people

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
    food_emissions *= (num_people - num_kids / 2)

    # Calculate household waste

    household_waste_emissions = HOUSEHOLD_WASTE_FACTOR * 0.01 * bin_bags * 4.2 # 10kg per bag, 4.2 weeks per month

    # Calculate pet emissions

    pet_emissions = (num_small_pets * SMALL_PETS + num_medium_pets * MEDIUM_PETS + num_large_pets * LARGE_PETS) / 12

    # Calculate total emissions
    total_emissions = (
        electricity_emissions
        + gas_emissions
        + car_emissions
        + public_transport_emissions
        + air_travel_emissions
        + food_emissions
        + household_waste_emissions
        + pet_emissions
    )

    return total_emissions, electricity_emissions, gas_emissions, car_emissions, public_transport_emissions, air_travel_emissions, food_emissions, household_waste_emissions, pet_emissions

# Calculate and display results when the button is clicked
if calculate_button:

    total_emissions, electricity_emissions, gas_emissions, car_emissions, public_transport_emissions, air_travel_emissions, food_emissions, household_waste_emissions, pet_emissions = calculate_carbon_footprint(
        electricity, gas, car_type, car_mileage, car_type_2, car_mileage_2, rail_transport, bus_transport, air_travel, diet_type, food_waste, bin_bags, num_small_pets, num_medium_pets, num_large_pets
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
    st.session_state.original_pet_emissions = pet_emissions

    st.write("## Your estimated monthly carbon footprint is:", round(total_emissions, 2), "kg CO2e")

    # Create pie chart
    fig, ax = plt.subplots(figsize=(8, 6))
    labels = ["Electricity", "Gas", "Car", "Public Transport", "Air Travel", "Food", "Household Waste", "Pets"]
    sizes = [
        st.session_state.original_electricity_emissions,
        st.session_state.original_gas_emissions,
        st.session_state.original_car_emissions,
        st.session_state.original_public_transport_emissions,
        st.session_state.original_air_travel_emissions,
        st.session_state.original_food_emissions,
        st.session_state.original_household_waste_emissions,
        st.session_state.original_pet_emissions
    ]
    ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=140)  # Adjust start angle for better layout
    ax.axis("equal")  # Ensure the pie is drawn as a circle
    ax.set_title("Carbon Footprint Breakdown")
    st.pyplot(fig)

    # Data table. UK averages from https://energyguide.org.uk/average-carbon-footprint-uk/

    ELECTRICITY_PERCENT = st.session_state.original_electricity_emissions / ELECTRICITY_UK
    GAS_PERCENT = st.session_state.original_gas_emissions / GAS_UK
    CAR_PERCENT = st.session_state.original_car_emissions / CAR_UK
    PUBLIC_TRANSPORT_PERCENT = "unknown"
    AIR_PERCENT = "unknown"
    FOOD_PERCENT = st.session_state.original_food_emissions / FOOD_UK

    data = {
        "Category": ["Electricity", "Gas", "Car", "Public Transport", "Air", "Food", "Household Waste", "Pets"],  # Use a list for consistency
        "UK Average (kgCO2e/mth)": [f"{round(ELECTRICITY_UK, 2)}", f"{round(GAS_UK, 2)}", f"{round(CAR_UK, 2)}", f"{PUBLIC_TRANSPORT_UK}", f"{AIR_UK}", f"{round(FOOD_UK, 2)}", "unknown", "unknown"],
        "Your Result (kgCO2e/mth)": [f"{round(st.session_state.original_electricity_emissions, 2)}", f"{round(st.session_state.original_gas_emissions, 2)}", f"{round(st.session_state.original_car_emissions, 2)}", f"{round(st.session_state.original_public_transport_emissions, 2)}", f"{round(st.session_state.original_air_travel_emissions, 2)}", f"{round(st.session_state.original_food_emissions, 2)}", f"{round(st.session_state.original_household_waste_emissions, 2)}", f"{round(st.session_state.original_pet_emissions, 2)}"],
        "Percent of UK Average": [f"{round(100*ELECTRICITY_PERCENT, 2)}%", f"{round(100*GAS_PERCENT, 2)}%", f"{round(100*CAR_PERCENT, 2)}%", f"{PUBLIC_TRANSPORT_PERCENT}%", f"{AIR_PERCENT}%", f"{round(100*FOOD_PERCENT, 2)}%", "unknown", "unknown"],  # Add '%' symbol
    }

    # Create a Pandas DataFrame
    df = pd.DataFrame(data)

    # Display the DataFrame with styling
    st.dataframe(df.style.set_properties(**{
        'text-align': 'center',  # Center align the text
    }).hide(axis="index"))  # Hide the index column

    st.write("Most averages from [Energy Guide](https://energyguide.org.uk/average-carbon-footprint-uk/). Some averages are quite hard to come by - advice welcome!")

st.header("Take Action to Reduce Your Footprint", anchor="take-action")

st.write("Explore how changes in your behaviour can impact your carbon footprint:")

# --- Home Energy ---
st.subheader("Home Energy")
reduce_electricity = st.checkbox("Reduce electricity consumption (e.g., switch to energy-efficient appliances, use less lighting)")
if reduce_electricity:
    electricity_reduction = st.slider("Estimated reduction in electricity consumption (%)", 0, 100, 10, 5)

green_electricity = st.checkbox("Buy your electricity from a green tariff")    

reduce_gas = st.checkbox("Reduce gas consumption (e.g., improve insulation, lower thermostat)")
if reduce_gas:
    gas_reduction = st.slider("Estimated reduction in gas consumption (%)", 0, 100, 10, 5)

# --- Travel ---
st.subheader("Travel")
reduce_car = st.checkbox("Reduce car usage (e.g., walk, cycle, use public transport)")
if reduce_car:
    car_reduction = st.slider("Estimated reduction in car mileage (%)", 0, 100, 10, 5)

diff_first_car = False
if car_type != "None":
    diff_first_car = st.checkbox("Drive a smaller or different type of car")
    if diff_first_car:
        new_car_1_type = st.selectbox("Select your new car type:", ["None", "Petrol", "Diesel", "Electric", "Hybrid"])
        if new_car_1_type != "None":
            new_car_1_size = st.selectbox("Select your new car size:", ["Large","Medium", "Small"])
        else:
            new_car_1_size = "Small"

diff_second_car = False
if car_type_2 != "None":
    diff_second_car = st.checkbox("Drive a smaller or different second car")
    if diff_second_car:
        new_car_2_type = st.selectbox("Select your new second car type:", ["None", "Petrol", "Diesel", "Electric", "Hybrid"])
        if new_car_2_type != "None":
            new_car_2_size = st.selectbox("Select your new second car size:", ["Large","Medium", "Small"])
        else:
            new_car_2_size = "Small"

reduce_flights = st.checkbox("Reduce air travel")
if reduce_flights:
    flights_reduction = st.slider("Estimated reduction in air travel mileage (%)", 0, 100, 10, 5)

# --- Food ---
st.subheader("Food")
improve_diet = st.checkbox("Improve diet (e.g., reduce meat consumption, eat more plant-based foods)")
if improve_diet:
    diet_improvement = st.selectbox("Select your new diet type:", ["Average", "Vegetarian", "Vegan"])

reduce_food_waste = st.checkbox("Reduce food waste (e.g., plan meals, store food properly)")
if reduce_food_waste:
    food_waste_reduction = st.slider("Estimated reduction in food waste (%)", 0, 100, 10, 5)

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
        car_mileage_2 *= (1 - car_reduction / 100)
    if diff_second_car:
        car_size_2 = new_car_2_size
        car_type_2 = new_car_2_type
    if diff_first_car:
        car_size = new_car_1_size
        car_type = new_car_1_type
    if reduce_flights:
        air_travel *= (1 - flights_reduction / 100)
    if improve_diet:
        diet_original = diet_type
        diet_type = diet_improvement
    if reduce_food_waste:
        food_waste *= (1 - food_waste_reduction / 100)

    # Recalculate footprint
    new_total_emissions, new_electricity_emissions, new_gas_emissions, new_car_emissions, new_public_transport_emissions, new_air_travel_emissions, new_food_emissions, new_household_waste_emissions, new_pet_emissions = calculate_carbon_footprint(
        electricity, gas, car_type, car_mileage, car_type_2, car_mileage_2, rail_transport, bus_transport, air_travel, diet_type, food_waste, bin_bags, num_small_pets, num_medium_pets, num_large_pets
    )

    st.write("## Your new estimated monthly carbon footprint is:", round(new_total_emissions, 2), "kg CO2e")


    # Create comparison bar chart
    electricity_ch = {
        "Original": st.session_state.original_electricity_emissions,
        "Revised": new_electricity_emissions,
    }
    gas_ch = {
        "Original": st.session_state.original_gas_emissions,
        "Revised": new_gas_emissions,
    }
    car_ch = {
        "Original": st.session_state.original_car_emissions,
        "Revised": new_car_emissions,
    }
    pt_ch = {
        "Original": st.session_state.original_public_transport_emissions,
        "Revised": new_public_transport_emissions,
    }
    air_ch = {
        "Original": st.session_state.original_air_travel_emissions,
        "Revised": new_air_travel_emissions,
    }
    food_ch = {
        "Original": st.session_state.original_food_emissions,
        "Revised": new_food_emissions,
    }
    waste_ch = {
        "Original": st.session_state.original_household_waste_emissions,
        "Revised": new_household_waste_emissions,
    }
    pets_ch = {
        "Original": st.session_state.original_pet_emissions,
        "Revised": new_pet_emissions,
    }

    # Create a stacked bar chart
    st.bar_chart({
        "Electricity": electricity_ch,
        "Gas": gas_ch,
        "Car": car_ch,
        "Public Transport": pt_ch,
        "Air Travel": air_ch,
        "Food": food_ch,
        "Household Waste": waste_ch,
        "Pets": pets_ch,
    },
    color=colors
    )
    
    # Table

    data = {
        "Category": ["Electricity", "Gas", "Car", "Public Transport", "Air", "Food", "Pets"],  # Use a list for consistency
        "Your Original Result (kgCO2e/mth)": [f"{round(st.session_state.original_electricity_emissions, 2)}", f"{round(st.session_state.original_gas_emissions, 2)}", f"{round(st.session_state.original_car_emissions, 2)}", f"{round(st.session_state.original_public_transport_emissions, 2)}", f"{round(st.session_state.original_air_travel_emissions, 2)}", f"{round(st.session_state.original_food_emissions, 2)}", f"{round(st.session_state.original_pet_emissions, 2)}"],
        "Your New Carbon Footprint (kgCO2e/mth)": [f"{round(new_electricity_emissions, 2)}", f"{round(new_gas_emissions, 2)}", f"{round(new_car_emissions, 2)}", f"{round(new_public_transport_emissions, 2)}", f"{round(new_air_travel_emissions, 2)}", f"{round(new_food_emissions, 2)}", f"{round(new_pet_emissions, 2)}"],
    }

    # Create a Pandas DataFrame
    df = pd.DataFrame(data)

    # Display the DataFrame with styling
    st.dataframe(df.style.set_properties(**{
        'text-align': 'center',  # Center align the text
    }).hide(axis="index"))  # Hide the index column

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
if diff_first_car:
    if new_car_1_type == "None":
        st.write("* I will no longer drive a car.")
    else:
        st.write("* I will instead drive a ", new_car_1_size, new_car_1_type, "vehicle as my main car.")
if diff_second_car:
    if new_car_2_type == "None":
        st.write("* I will no longer use a second car.")
    else:
        st.write("I will instead drive a", new_car_2_size, new_car_2_type, "vehicle as my second car.")
if reduce_flights:
    st.write("* I will go", round(flights_reduction, 2), "percent less far on flights. Your next step might be to explore the website [Flight Free](https://flightfree.co.uk/)")

if improve_diet:
    st.write("* I will go from a", diet_original, "diet to a ", diet_improvement, "diet. Your next step might be to explore low-meat or vegetarian cookbooks for interesting and tasty new recipes (it's not all bland tofu and self-righteousness from here on out) e.g. [Food For Life](https://thehappyfoodie.co.uk/books/the-food-for-life-cookbook-100-recipes-created-with-zoe/)")
if reduce_food_waste:
    st.write("* I will reduce my food waste by ", food_waste_reduction, "percent")

# --- Social Sharing ---
st.header("Share Your Results", anchor="share")

st.write("Do it. You know you want to.")

# Offsetting
st.header("Offset the rest?", anchor="offset")

st.write("""

Carbon offsetting is a way to compensate for emissions that are difficult or impossible to avoid, by funding an equivalent carbon dioxide saving elsewhere. For example, if you take a long-haul flight, you can pay to plant trees that will absorb the same amount of carbon dioxide as your flight emitted. Offsetting is a practical way to take responsibility for unavoidable emissions while supporting projects that actively combat climate change. It's important to understand the concept of additionality in carbon offsetting. Additionality ensures that the projects being funded would not have happened anyway, meaning that your investment directly contributes to new emissions reductions or removals.

When considering carbon offsetting, it's helpful to be aware of the concept of "vintage."  Vintage refers to the year in which the emissions reduction or removal occurred. Newer vintages are generally preferred, as they reflect more recent climate action. Another important concept is the distinction between Pending Issuance Units (PIUs) and verified units. PIUs represent future emissions reductions or removals that are expected to be generated by a project, while verified units represent emissions reductions or removals that have already been achieved and verified.

Several companies in the UK offer carbon offsetting services to individuals. These companies typically provide a range of offsetting projects, with a focus on forestry, renewable energy, and community development projects. Some of the most well-known companies include:

* [Find out more here](https://www.professionalenergy.co.uk/carbon-offsetting-schemes/).
* One example of an offsetting company for individuals is [CarbonClick](https://www.carbonclick.com/solutions/individuals)

""")