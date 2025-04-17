from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
import gym
import os
from gym import spaces

app = Flask(__name__)
CORS(app)

# Define a custom environment for RL
class ElectronicsEnv(gym.Env):
    def __init__(self, device_type):
        super(ElectronicsEnv, self).__init__()
        self.device_type = device_type

        # Define observation space based on device type
        if self.device_type == "Laptop":
            self.observation_space = spaces.Box(low=0, high=100, shape=(5,), dtype=np.float32)
        elif self.device_type == "Smartphone":
            self.observation_space = spaces.Box(low=0, high=100, shape=(4,), dtype=np.float32)
        elif self.device_type == "Tablet":
            self.observation_space = spaces.Box(low=0, high=100, shape=(5,), dtype=np.float32)
        elif self.device_type == "Desktop Computer":
            self.observation_space = spaces.Box(low=0, high=100, shape=(4,), dtype=np.float32)
        elif self.device_type == "Smartwatch":
            self.observation_space = spaces.Box(low=0, high=100, shape=(4,), dtype=np.float32)
        elif self.device_type == "E-Reader":
            self.observation_space = spaces.Box(low=0, high=100, shape=(5,), dtype=np.float32)
        elif self.device_type == "Wearable Fitness Tracker":
            self.observation_space = spaces.Box(low=0, high=100, shape=(4,), dtype=np.float32)
        elif self.device_type == "Television":
            self.observation_space = spaces.Box(low=0, high=100, shape=(4,), dtype=np.float32)
        elif self.device_type == "Digital Camera":
            self.observation_space = spaces.Box(low=0, high=100, shape=(4,), dtype=np.float32)
        elif self.device_type == "Wireless/Bluetooth Earbuds":
            self.observation_space = spaces.Box(low=0, high=100, shape=(3,), dtype=np.float32)
        elif self.device_type == "Headphones":
            self.observation_space = spaces.Box(low=0, high=100, shape=(3,), dtype=np.float32)
        elif self.device_type == "Portable Bluetooth Speaker":
            self.observation_space = spaces.Box(low=0, high=100, shape=(3,), dtype=np.float32)
        elif self.device_type == "Home Theater System":
            self.observation_space = spaces.Box(low=0, high=100, shape=(3,), dtype=np.float32)
        elif self.device_type == "Soundbar":
            self.observation_space = spaces.Box(low=0, high=100, shape=(3,), dtype=np.float32)
        elif self.device_type == "Printer":
            self.observation_space = spaces.Box(low=0, high=100, shape=(3,), dtype=np.float32)
        elif self.device_type == "Scanner":
            self.observation_space = spaces.Box(low=0, high=100, shape=(3,), dtype=np.float32)
        elif self.device_type == "Smart Home Assistant":
            self.observation_space = spaces.Box(low=0, high=100, shape=(3,), dtype=np.float32)
        else:
            raise ValueError("Unsupported device type.")

        # Define action space
        self.action_space = spaces.Discrete(3)  # 0 = reduce usage, 1 = maintenance, 2 = upgrade

        # Initial state
        self.state = None

    def reset(self):
        # Reset state based on device type
        self.state = np.random.uniform(low=self.observation_space.low, high=self.observation_space.high, size=self.observation_space.shape)
        return self.state

    def step(self, action):
        sustainability, lifespan = self.state[:2]
        if action == 0:  # Reduce usage
            sustainability += np.random.uniform(1, 5)
            lifespan += np.random.uniform(0.5, 1.5)
        elif action == 1:  # Maintenance
            sustainability += np.random.uniform(3, 8)
        elif action == 2:  # Upgrade
            lifespan += np.random.uniform(1, 3)

        sustainability = np.clip(sustainability, 0, 100)
        lifespan = np.clip(lifespan, 0, 10)  # Ensure lifespan remains in the valid range after updates

        self.state = np.clip(np.array([sustainability, lifespan] + list(self.state[2:])), self.observation_space.low, self.observation_space.high)
        reward = 0.7 * sustainability + 0.3 * lifespan  # Weighted to prioritize sustainability
        done = False
        return self.state, reward, done, {}

# Map condition to numeric value
def condition_map(condition):
    mapping = {"new": 100, "good": 75, "fair": 50, "poor": 25}
    return mapping.get(condition, 50)

def resolution_map(resolution):
    mapping = {"1080p": 50, "4k": 100}
    return mapping.get(resolution, 50)

def get_valid_input(prompt, dtype, min_val=None, max_val=None, valid_options=None):
    while True:
        user_input = input(prompt).strip()

        if valid_options:
            # Convert both input and options to lowercase for comparison
            user_input_lower = user_input.lower()
            valid_options_lower = [option.lower() for option in valid_options]  

            if user_input_lower in valid_options_lower:
                original_value = valid_options[valid_options_lower.index(user_input_lower)]  # Keep original capitalization

                # If condition mapping is needed, return its numeric equivalent
                if "condition" in prompt.lower():  
                    return condition_map(user_input_lower)

                return original_value  # Return the correctly capitalized string
                
            print(f"Invalid input! Please enter one of: {', '.join(valid_options)}")

        else:
            try:
                user_input = dtype(user_input)
                if (min_val is not None and user_input < min_val) or (max_val is not None and user_input > max_val):
                    print(f"Value out of range! Please enter a number between {min_val} and {max_val}.")
                else:
                    return user_input
            except ValueError:
                print(f"Invalid input! Please enter a valid {dtype.__name__}.")
                
device_questions = {
    "Laptop": [("Daily Usage (hours)", float), ("Condition (New/Good/Fair/Poor)", str),
               ("Battery Health (%)", float), ("RAM Size (GB)", float), ("Device Age (years)", float)],

    "Smartphone": [("Daily Usage (hours)", float), ("Condition (New/Good/Fair/Poor)", str),
                   ("Battery Health (%)", float), ("Storage Size (GB)", float)],

    "Tablet": [("Daily Usage (hours)", float), ("Condition (New/Good/Fair/Poor)", str),
               ("Battery Health (%)", float), ("Screen Size (inches)", float), ("Device Age (years)", float)],

    "Desktop Computer": [("Daily Usage (hours)", float), ("Condition (New/Good/Fair/Poor)", str),
                         ("Power Usage (Watts)", float), ("Device Age (years)", float)],

    "Smartwatch": [("Daily Usage (hours)", float), ("Condition (New/Good/Fair/Poor)", str),
                   ("Battery Health (%)", float), ("Device Age (years)", float)],

    "E-Reader": [("Daily Usage (hours)", float), ("Condition (New/Good/Fair/Poor)", str),
                 ("Battery Health (%)", float), ("Storage Size (GB)", float), ("Device Age (years)", float)],

    "Wearable Fitness Tracker": [("Daily Usage (hours)", float), ("Condition (New/Good/Fair/Poor)", str),
                                 ("Battery Health (%)", float), ("Average Daily Steps Tracked", int)],  

    "Television": [("Screen Size (inches)", float), ("Resolution (e.g., 1080p, 4K)", str),
                   ("Device Age (years)", float), ("Condition (New/Good/Fair/Poor)", str)],

    "Digital Camera": [("Megapixels", float), ("Condition (New/Good/Fair/Poor)", str),
                       ("Device Age (years)", float), ("Usage (hours per month)", float)],

    "Printer": [("Monthly Usage (pages printed)", float), ("Condition (New/Good/Fair/Poor)", str),
                ("Device Age (years)", float)],

    "Scanner": [("Monthly Usage (pages scanned)", float), ("Condition (New/Good/Fair/Poor)", str),
                ("Device Age (years)", float)],

    "Smart Home Assistant": [("Daily Usage (hours)", float), ("Condition (New/Good/Fair/Poor)", str),
                             ("Device Age (years)", float)],

    "Wireless/Bluetooth Earbuds": [("Daily Usage (hours)", float), ("Condition (New/Good/Fair/Poor)", str), 
                                    ("Battery Health (%)", float)],

    "Headphones": [("Daily Usage (hours)", float), ("Condition (New/Good/Fair/Poor)", str),
                   ("Battery Health (%)", float)],

    "Portable Bluetooth Speaker": [("Daily Usage (hours)", float), ("Condition (New/Good/Fair/Poor)", str),
                                   ("Battery Health (%)", float)],

    "Home Theater System": [("Daily Usage (hours)", float), ("Condition (New/Good/Fair/Poor)", str),
                            ("Speaker Wattage (W)", float)],

    "Soundbar": [("Daily Usage (hours)", float), ("Condition (New/Good/Fair/Poor)", str),
                 ("Speaker Wattage (W)", float)]
}

def get_device_inputs(device_type):
    if device_type not in device_questions:
        raise ValueError("Device type not recognized!")

    responses = []
    for question, dtype, *constraints in device_questions[device_type]:
        # Define constraints for specific inputs
        if "Daily Usage" in question:
            value = get_valid_input(f"{question} (0-24): ", dtype, 0, 24)
        elif "Battery Health" in question:
            value = get_valid_input(f"{question} (0-100%): ", dtype, 0, 100)
        elif "Device Age" in question:
            value = get_valid_input(f"{question} (0-20 years): ", dtype, 0, 20)
        elif "RAM Size" in question:
            value = get_valid_input(f"{question} (1-128 GB): ", dtype, 1, 128)
        elif "Storage Size" in question:
            value = get_valid_input(f"{question} (8-2048 GB): ", dtype, 8, 2048)
        elif "Screen Size" in question:
            value = get_valid_input(f"{question} (5-100 inches): ", dtype, 5, 100)
        elif "Megapixels" in question:
            value = get_valid_input(f"{question} (1-108 MP): ", dtype, 1, 108)
        elif "Condition" in question:
            value = get_valid_input(f"{question} (New/Good/Fair/Poor): ", str, valid_options=["New", "Good", "Fair", "Poor"])
            value = condition_map(value)  
        elif "Resolution" in question:
            value = get_valid_input(f"{question} (1080p/4K): ", str, valid_options=["1080p", "4K"])
            value = resolution_map(value.lower())  
        elif "Power Usage" in question:
            value = get_valid_input(f"{question} (10-1000 Watts): ", dtype, 10, 1000)
        elif "Steps" in question:
            value = get_valid_input(f"{question} (0-50000 steps): ", dtype, 0, 50000)
        elif "Pages printed" in question or "Pages scanned" in question:
            value = get_valid_input(f"{question} (0-10000 pages): ", dtype, 0, 10000)
        elif "Usage (hours per month)" in question:
            value = get_valid_input(f"{question} (0-720 hours): ", dtype, 0, 720)
        else:
            value = get_valid_input(f"{question}: ", dtype)  # Default case (no constraints)

        responses.append(value)

    return np.array(responses)


def generate_suggestions(device_type, sustainability, lifespan, user_input):
    suggestions = []
    
    if device_type == "Smartwatch":
        usage, condition, battery, age = user_input
        if battery < 50:
            suggestions.append("Consider replacing the battery to improve device performance.")
        if age > 3:
            suggestions.append("Upgrade to a newer model if the current device is slow or unsupported.")
        if usage > 16:
            suggestions.append("Reduce daily usage to extend the lifespan and improve sustainability.")
        if sustainability < 50:
            suggestions.append("Perform regular maintenance or software updates to enhance sustainability.")

    elif device_type == "Laptop":
        usage, condition, battery, ram, age = user_input
        if battery < 40:
            suggestions.append("Replace the battery to prevent frequent charging.")
        if ram < 8:
            suggestions.append("Consider upgrading the RAM for better performance.")
        if age > 5:
            suggestions.append("Evaluate if a newer model would be more energy-efficient.")
        if usage > 10:
            suggestions.append("Optimize daily usage by closing unnecessary programs or lowering screen brightness.")

    elif device_type == "Smartphone":
        usage, condition, battery, storage = user_input
        if battery < 50:
            suggestions.append("Replace the battery if the device frequently shuts down.")
        if storage < 32:
            suggestions.append("Clear unnecessary files or upgrade storage for better performance.")
        if usage > 12:
            suggestions.append("Reduce screen time to prevent overheating and extend lifespan.")
        if sustainability < 50:
            suggestions.append("Regularly update the operating system and apps for improved efficiency.")

    elif device_type == "Tablet":
        usage, condition, battery, screen_size, age = user_input
        if battery < 50:
            suggestions.append("Replace the battery to improve daily performance.")
        if screen_size > 12:
            suggestions.append("Consider using a smaller screen size to save energy.")
        if age > 4:
            suggestions.append("Upgrade to a newer model with better energy efficiency.")
        if sustainability < 50:
            suggestions.append("Use a screen protector and clean the screen regularly to maintain usability.")

    elif device_type == "Desktop Computer":
        usage, condition, power_usage, age = user_input
        if power_usage > 200:
            suggestions.append("Consider upgrading to an energy-efficient power supply unit.")
        if age > 7:
            suggestions.append("Upgrade hardware components or consider replacing the device.")
        if usage > 12:
            suggestions.append("Turn off the device when not in use to save energy.")
        if sustainability < 50:
            suggestions.append("Clean the fans and ensure proper ventilation to improve performance.")

    elif device_type == "E-Reader":
        usage, condition, battery, storage, age = user_input
        if battery < 60:
            suggestions.append("Replace the battery to ensure longer reading hours.")
        if age > 4:
            suggestions.append("Upgrade to a newer model for improved readability.")
        if sustainability < 50:
            suggestions.append("Keep the screen clean and avoid exposing it to extreme conditions.")

    elif device_type == "Wearable Fitness Tracker":
        usage, condition, battery, steps = user_input
        if battery < 50:
            suggestions.append("Replace the battery for uninterrupted tracking.")
        if steps < 5000:
            suggestions.append("Increase physical activity to make better use of the tracker.")
        if sustainability < 50:
            suggestions.append("Regularly clean the strap and ensure proper syncing with your phone.")

    elif device_type == "Television":
        screen_size, resolution, age, condition = user_input
        if age > 7:
            suggestions.append("Upgrade to a newer, energy-efficient model.")
        if resolution < 50:
            suggestions.append("Consider upgrading to a higher-resolution TV for better experience.")
        if sustainability < 50:
            suggestions.append("Clean the screen regularly and use energy-saving modes.")

    elif device_type == "Digital Camera":
        megapixels, condition, age, usage = user_input
        if megapixels < 12:
            suggestions.append("Consider upgrading to a higher-megapixel camera.")
        if age > 5:
            suggestions.append("Evaluate if a newer model with better features would suit your needs.")
        if usage > 40:
            suggestions.append("Avoid excessive use to prevent overheating and wear.")
        if sustainability < 50:
            suggestions.append("Store the camera in a dust-free environment and handle it carefully.")

    elif device_type == "Printer":
        usage, condition, age = user_input
        if usage > 1000:
            suggestions.append("Use duplex printing to save paper and reduce wear.")
        if age > 6:
            suggestions.append("Consider replacing the printer with an energy-efficient model.")
        if sustainability < 50:
            suggestions.append("Clean the ink heads and perform regular maintenance.")

    elif device_type == "Scanner":
        usage, condition, age = user_input
        if usage > 500:
            suggestions.append("Avoid scanning unnecessary documents to reduce wear.")
        if age > 5:
            suggestions.append("Upgrade to a more efficient scanner.")
        if sustainability < 50:
            suggestions.append("Ensure the scanner is properly aligned and cleaned.")

    elif device_type == "Smart Home Assistant":
        usage, condition, age = user_input
        if age > 5:
            suggestions.append("Consider upgrading to the latest version for enhanced features.")
        if sustainability < 50:
            suggestions.append("Keep the device clean and ensure software updates are installed.")
        if usage > 10:
            suggestions.append("Reduce daily usage to save energy.")

    else:
        suggestions.append("Your device seems to be in good condition. Keep up the good maintenance!")
    
    return suggestions

def save_device_data(device_type, user_input):
    folder_path = "device_data"  # Define folder name
    file_path = f"{folder_path}/{device_type}_data.xlsx"

    # Create folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Convert user input to a DataFrame row
    new_data = pd.DataFrame([user_input])

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        df = pd.concat([df, new_data], ignore_index=True)  # Append new data
    else:
        df = new_data  # Create new file if none exists

    df.to_excel(file_path, index=False)
    print(f"Data saved for {device_type} at {file_path}")

    return df


def compare_with_saved_data(device_type, user_input):
    file_path = f"device_data/{device_type}_data.xlsx"

    if not os.path.exists(file_path):
        print(f"No previous data found for {device_type}.")
        return None

    df = pd.read_excel(file_path)
    print(f"Comparing new {device_type} data with {len(df)} previous records...")

    # Compute differences with each saved device record
    comparisons = df.apply(lambda row: sum(abs(row - user_input)), axis=1)

    # Find the closest match (smallest difference)
    closest_match_index = comparisons.idxmin()
    closest_match = df.iloc[closest_match_index]

    print(f"Closest {device_type} match found:\n{closest_match}")
    return closest_match

# Main function

device_inputs = {
    "Laptop": ["Daily Usage (hours)", "Condition(New/Good/Fair/Poor)", "Battery Health (%)", "RAM Size (GB)", "Device Age (years)"],
    "Tablet": ["Daily Usage (hours)", "Condition(New/Good/Fair/Poor)", "Battery Health (%)", "Screen Size (inches)", "Device Age (years)"],
    "Smartphone": ["Daily Usage (hours)", "Condition(New/Good/Fair/Poor)", "Battery Health (%)", "Storage Size (GB)"],
    "Desktop Computer": ["Daily Usage (hours)", "Condition(New/Good/Fair/Poor)", "Power Usage (Watts)", "Device Age (years)"],
    "Smartwatch": ["Daily Usage (hours)", "Condition(New/Good/Fair/Poor)", "Battery Health (%)", "Device Age (years)"],
    "E-Reader": ["Daily Usage (hours)", "Condition(New/Good/Fair/Poor)", "Battery Health (%)", "Storage Size (GB)", "Device Age (years)"],
    "Wearable Fitness Tracker": ["Daily Usage (hours)", "Condition(New/Good/Fair/Poor)", "Battery Health (%)", "Average Daily Steps Tracked"],
    "Television": ["Screen Size (inches)", "Resolution (e.g., 1080p, 4K)", "Device Age (years)", "Condition(New/Good/Fair/Poor)"],
    "Digital Camera": ["Megapixels", "Condition (New/Good/Fair/Poor)", "Device Age (years)", "Usage (hours per month)"],
    "Printer": ["Monthly Usage (pages printed)", "Condition(New/Good/Fair/Poor)", "Device Age (years)"],
    "Scanner": ["Monthly Usage (pages scanned)", "Condition(New/Good/Fair/Poor)", "Device Age (years)"],
    "Smart Home Assistant": ["Daily Usage (hours)", "Condition(New/Good/Fair/Poor)", "Device Age (years)"],
    "Headphones": ["Daily Usage (hours)", "Condition(New/Good/Fair/Poor)", "Battery Health (%)"],
    "Wireless/Bluetooth Earbuds": ["Daily Usage (hours)", "Condition(New/Good/Fair/Poor)", "Battery Health (%)"],
    "Portable Bluetooth Speaker": ["Daily Usage (hours)", "Condition(New/Good/Fair/Poor)", "Battery Health (%)"],
    "Home Theater System": ["Daily Usage (hours)", "Condition(New/Good/Fair/Poor)", "Battery Health (%)"],
    "Soundbar": ["Daily Usage (hours)", "Condition(New/Good/Fair/Poor)", "Battery Health (%)"]
}

@app.route('/select-device', methods=['POST'])
def select_device():
    data = request.get_json()
    device_type = data.get("device_type")

    if device_type not in device_inputs:
        return jsonify({"error": "Invalid device type"}), 400

    input_fields = device_inputs[device_type]
    return jsonify({
        "device_type": device_type,
        "num_inputs": len(input_fields),
        "input_fields": input_fields
    })

def convert_input(user_input):
    valid_conditions = {"new", "good", "fair", "poor"}
    new_input = []
    
    for item in user_input:
        if isinstance(item, str) and item.lower() in valid_conditions:
            new_input.append(float(condition_map(item)))
        else:
            try:
                new_input.append(float(item))
            except ValueError:
                # fallback if something unexpected is there
                new_input.append(0.0)
    
    return new_input

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # print("Welcome to the Electronics Sustainability Predictor!")
        # print("Select your device type:")
        # device_types = [
        #     "Laptop", "Smartphone", "Tablet", "Desktop Computer", "Smartwatch", "E-Reader",
        #     "Wearable Fitness Tracker", "Television", "Digital Camera", "Wireless/Bluetooth Earbuds",
        #     "Headphones", "Portable Bluetooth Speaker", "Home Theater System", "Soundbar",
        #     "Printer", "Scanner", "Smart Home Assistant"
        # ]
        # for i, device in enumerate(device_types):
        #     print(f"{i + 1}. {device}")

        # try:
        #     choice = int(input("Enter the number corresponding to your device: ")) - 1
        #     device_type = device_types[choice]
        # except (IndexError, ValueError):
        #     print("Invalid choice!")
        #     return

        data = request.get_json()
        # print(data);
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        device_type = data.get("device_type")
        # inputs = data.get("inputs")

        # Collect user input for the selected device
        # user_input = get_device_inputs(device_type)
        user_input= data.get("inputs")
        user_input = convert_input(user_input)
        print(f"User input for {device_type}: {user_input}")
        if not user_input:
            return jsonify({"error": "No inputs provided"}), 400

        # Initialize environment and train model
        def train_or_load_model(device_type, env):
            model_path = f"saved_models/{device_type}_model.zip"

            if os.path.exists(model_path):
                print(f"Loading existing model for {device_type}...")
                model = DQN.load(model_path, env=env)  # Load model with the environment
            else:
                print(f"Training a new model for {device_type}...")
                model = DQN("MlpPolicy", env, verbose=1)
                model.learn(total_timesteps=10000)
                model.save(model_path)  # Save after training
                print(f"Model saved at {model_path}")

            return model

        # Instead of retraining every time
        env = DummyVecEnv([lambda: ElectronicsEnv(device_type)])
        model = train_or_load_model(device_type, env)

        # Compare new input with past device values
        print(f"Comparing new {device_type} data with past records...")
        compare_with_saved_data(device_type, user_input)

        # Save user input in the respective device's file
        print(f"Saving {device_type} data...")
        save_device_data(device_type, user_input)

        # Predict sustainability and lifespan
        print(f"Predicting sustainability and lifespan for {device_type}...")
        obs = np.clip(user_input, env.observation_space.low, env.observation_space.high).astype(np.float32)
        action, _ = model.predict(obs, deterministic=True)

        sustainability = obs[0] + 10 * action
        lifespan = obs[1] / 10 + 2 * action  # Dividing by 10 scales condition to a range of 0-10.

        print(f"\nPredicted Sustainability: {sustainability:.2f}")
        print(f"Predicted Lifespan: {lifespan:.2f} years")

        # Generate and display suggestions
        suggestions = generate_suggestions(device_type, sustainability, lifespan, user_input)
        if suggestions:
            print("\nSuggestions to Improve Sustainability and Lifespan:")
            for suggestion in suggestions:
                print(f"- {suggestion}")
        else:
            print("\nNo specific suggestions. Your device seems to be in good condition!")


        return jsonify({
            "device_type": device_type,
            "sustainability": round(sustainability, 2),
            "lifespan": round(lifespan, 2),
            "suggestions": suggestions
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
    # main()
