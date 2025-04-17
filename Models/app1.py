from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
import gym
from gym import spaces
import json
import os

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes

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


# User input system
def get_device_inputs(device_type):
    if device_type == "Laptop":
        print("Please provide the following details for your Laptop:")
        usage = float(input("Daily Usage (hours): "))
        condition = input("Condition (New/Good/Fair/Poor): ").lower()
        battery = float(input("Battery Health (%): "))
        ram = float(input("RAM Size (GB): "))
        age = float(input("Device Age (years): "))
        return np.array([usage, condition_map(condition), battery, ram, age])

    elif device_type == "Tablet":
        print("Please provide the following details for your Tablet:")
        usage = float(input("Daily Usage (hours): "))
        condition = input("Condition (New/Good/Fair/Poor): ").lower()
        battery = float(input("Battery Health (%): "))
        screen_size = float(input("Screen Size (inches): "))
        age = float(input("Device Age (years): "))
        return np.array([usage, condition_map(condition), battery, screen_size, age])

    elif device_type == "Smartphone":
        print("Please provide the following details for your Smartphone:")
        usage = float(input("Daily Usage (hours): "))
        condition = input("Condition (New/Good/Fair/Poor): ").lower()
        battery = float(input("Battery Health (%): "))
        storage = float(input("Storage Size (GB): "))
        return np.array([usage, condition_map(condition), battery, storage])

    elif device_type == "Desktop Computer":
        print("Please provide the following details for your Desktop Computer:")
        usage = float(input("Daily Usage (hours): "))
        condition = input("Condition (New/Good/Fair/Poor): ").lower()
        power_usage = float(input("Power Usage (Watts): "))
        age = float(input("Device Age (years): "))
        return np.array([usage, condition_map(condition), power_usage, age])

    elif device_type == "Smartwatch":
        print("Please provide the following details for your Smartwatch:")
        usage = float(input("Daily Usage (hours): "))
        condition = input("Condition (New/Good/Fair/Poor): ").lower()
        battery = float(input("Battery Health (%): "))
        age = float(input("Device Age (years): "))
        return np.array([usage, condition_map(condition), battery, age])

    elif device_type == "E-Reader":
        print("Please provide the following details for your E-Reader:")
        usage = float(input("Daily Usage (hours): "))
        condition = input("Condition (New/Good/Fair/Poor): ").lower()
        battery = float(input("Battery Health (%): "))
        storage = float(input("Storage Size (GB): "))
        age = float(input("Device Age (years): "))
        return np.array([usage, condition_map(condition), battery, storage, age])

    elif device_type == "Wearable Fitness Tracker":
        print("Please provide the following details for your Wearable Fitness Tracker:")
        usage = float(input("Daily Usage (hours): "))
        condition = input("Condition (New/Good/Fair/Poor): ").lower()
        battery = float(input("Battery Health (%): "))
        steps = int(input("Average Daily Steps Tracked: "))
        return np.array([usage, condition_map(condition), battery, steps])

    elif device_type == "Television":
        print("Please provide the following details for your Television:")
        screen_size = float(input("Screen Size (inches): "))
        resolution = input("Resolution (e.g., 1080p, 4K): ").lower()
        age = float(input("Device Age (years): "))
        condition = input("Condition (New/Good/Fair/Poor): ").lower()
        return np.array([screen_size, resolution_map(resolution), age, condition_map(condition)])

    elif device_type == "Digital Camera":
        print("Please provide the following details for your Digital Camera:")
        megapixels = float(input("Megapixels: "))
        condition = input("Condition (New/Good/Fair/Poor): ").lower()
        age = float(input("Device Age (years): "))
        usage = float(input("Usage (hours per month): "))
        return np.array([megapixels, condition_map(condition), age, usage])

    elif device_type == "Printer":
        print("Please provide the following details for your Printer:")
        usage = float(input("Monthly Usage (pages printed): "))
        condition = input("Condition (New/Good/Fair/Poor): ").lower()
        age = float(input("Device Age (years): "))
        return np.array([usage, condition_map(condition), age])

    elif device_type == "Scanner":
        print("Please provide the following details for your Scanner:")
        usage = float(input("Monthly Usage (pages scanned): "))
        condition = input("Condition (New/Good/Fair/Poor): ").lower()
        age = float(input("Device Age (years): "))
        return np.array([usage, condition_map(condition), age])

    elif device_type == "Smart Home Assistant":
        print("Please provide the following details for your Smart Home Assistant:")
        usage = float(input("Daily Usage (hours): "))
        condition = input("Condition (New/Good/Fair/Poor): ").lower()
        age = float(input("Device Age (years): "))
        return np.array([usage, condition_map(condition), age])


    else:
        raise ValueError("Device type not recognized!")


# Map condition to numeric value
def condition_map(condition):
    mapping = {"new": 100, "good": 75, "fair": 50, "poor": 25}
    return mapping.get(condition, 50)  # Default to 50 if condition is not recognized

def resolution_map(resolution):
    mapping = {"1080p": 50, "4k": 100}
    return mapping.get(resolution, 50)  # Default to 50 if resolution is not recognized


def generate_suggestions(device_type, sustainability, lifespan, user_input):
    suggestions = []
    
    # Extract values safely
    try:
        if device_type == "Smartwatch":
            # usage, condition, battery, age = user_input
            usage=user_input[0]
            condition=user_input[1]
            battery=user_input[2]
            age=user_input[3]
            if battery < 50:
                suggestions.append("Consider replacing the battery to improve device performance.")
            if age > 3:
                suggestions.append("Upgrade to a newer model if the current device is slow or unsupported.")
            if usage > 16:
                suggestions.append("Reduce daily usage to extend lifespan and improve sustainability.")
            if sustainability < 50:
                suggestions.append("Perform regular maintenance or software updates to enhance sustainability.")

        elif device_type == "Laptop":
            # usage, condition, battery, ram, age = user_input
            usage=user_input[0]
            condition=user_input[1]
            battery=user_input[2]
            ram=user_input[3]
            age=user_input[4]
            if battery < 40:
                suggestions.append("Replace the battery to prevent frequent charging.")
            if ram < 8:
                suggestions.append("Consider upgrading the RAM for better performance.")
            if age > 5:
                suggestions.append("Evaluate if a newer model would be more energy-efficient.")
            if usage > 10:
                suggestions.append("Optimize daily usage by closing unnecessary programs or lowering screen brightness.")

        elif device_type == "Smartphone":
            # usage, condition, battery, storage = user_input
            usage=user_input[0]
            condition=user_input[1]
            battery=user_input[2]
            storage=user_input[3]
            if battery < 50:
                suggestions.append("Replace the battery if the device frequently shuts down.")
            if storage < 32:
                suggestions.append("Clear unnecessary files or upgrade storage for better performance.")
            if usage > 12:
                suggestions.append("Reduce screen time to prevent overheating and extend lifespan.")
            if sustainability < 50:
                suggestions.append("Regularly update the operating system and apps for improved efficiency.")

        elif device_type == "Tablet":
            # usage, condition, battery, screen_size, age = user_input
            usage=user_input[0]
            condition=user_input[1]
            battery=user_input[2]
            screen_size=user_input[3]
            age=user_input[4]
            if battery < 50:
                suggestions.append("Replace the battery to improve daily performance.")
            if screen_size > 12:
                suggestions.append("Consider using a smaller screen size to save energy.")
            if age > 4:
                suggestions.append("Upgrade to a newer model with better energy efficiency.")
            if sustainability < 50:
                suggestions.append("Use a screen protector and clean the screen regularly to maintain usability.")

        elif device_type == "Desktop Computer":
            # usage, condition, power_usage, age = user_input
            usage=user_input[0]
            condition=user_input[1]
            power_usage=user_input[2]
            age=user_input[3]
            if power_usage > 200:
                suggestions.append("Consider upgrading to an energy-efficient power supply unit.")
            if age > 7:
                suggestions.append("Upgrade hardware components or consider replacing the device.")
            if usage > 12:
                suggestions.append("Turn off the device when not in use to save energy.")
            if sustainability < 50:
                suggestions.append("Clean the fans and ensure proper ventilation to improve performance.")

        elif device_type == "E-Reader":
            # usage, condition, battery, storage, age = user_input
            usage=user_input[0]
            condition=user_input[1]
            battery=user_input[2]
            storage=user_input[3]
            age=user_input[4]
            if battery < 60:
                suggestions.append("Replace the battery to ensure longer reading hours.")
            if age > 4:
                suggestions.append("Upgrade to a newer model for improved readability.")
            if sustainability < 50:
                suggestions.append("Keep the screen clean and avoid exposing it to extreme conditions.")

        elif device_type == "Wearable Fitness Tracker":
            # usage, condition, battery, steps = user_input
            usage=user_input[0]
            condition=user_input[1]
            battery=user_input[2]
            steps=user_input[3]
            if battery < 50:
                suggestions.append("Replace the battery for uninterrupted tracking.")
            if steps < 5000:
                suggestions.append("Increase physical activity to make better use of the tracker.")
            if sustainability < 50:
                suggestions.append("Regularly clean the strap and ensure proper syncing with your phone.")

        elif device_type == "Television":
            # screen_size, resolution, age, condition = user_input
            screen_size=user_input[0]
            resolution=user_input[1]
            age=user_input[2]
            condition=user_input[3]
            if age > 7:
                suggestions.append("Upgrade to a newer, energy-efficient model.")
            if resolution < 50:
                suggestions.append("Consider upgrading to a higher-resolution TV for a better experience.")
            if sustainability < 50:
                suggestions.append("Clean the screen regularly and use energy-saving modes.")

        elif device_type == "Digital Camera":
            # megapixels, condition, age, usage = user_input
            megapixels=user_input[0]
            condition=user_input[1]
            age=user_input[2]
            usage=user_input[3]
            if megapixels < 12:
                suggestions.append("Consider upgrading to a higher-megapixel camera.")
            if age > 5:
                suggestions.append("Evaluate if a newer model with better features would suit your needs.")
            if usage > 40:
                suggestions.append("Avoid excessive use to prevent overheating and wear.")
            if sustainability < 50:
                suggestions.append("Store the camera in a dust-free environment and handle it carefully.")

        elif device_type == "Printer":
            # usage, condition, age = user_input
            usage=user_input[0]
            condition=user_input[1]
            age=user_input[2]
            if usage > 1000:
                suggestions.append("Use duplex printing to save paper and reduce wear.")
            if age > 6:
                suggestions.append("Consider replacing the printer with an energy-efficient model.")
            if sustainability < 50:
                suggestions.append("Clean the ink heads and perform regular maintenance.")

        elif device_type == "Scanner":
            # usage, condition, age = user_input
            usage=user_input[0]
            condition=user_input[1]
            age=user_input[2]
            if usage > 500:
                suggestions.append("Avoid scanning unnecessary documents to reduce wear.")
            if age > 5:
                suggestions.append("Upgrade to a more efficient scanner.")
            if sustainability < 50:
                suggestions.append("Ensure the scanner is properly aligned and cleaned.")

        elif device_type == "Smart Home Assistant":
            # usage, condition, age = user_input
            usage=user_input[0]
            condition=user_input[1]
            age=user_input[2]
            if age > 5:
                suggestions.append("Consider upgrading to the latest version for enhanced features.")
            if sustainability < 50:
                suggestions.append("Keep the device clean and ensure software updates are installed.")
            if usage > 10:
                suggestions.append("Reduce daily usage to save energy.")

        else:
            suggestions.append("Your device seems to be in good condition. Keep up the good maintenance!")

    except ValueError as e:
        suggestions.append(f"Error processing device inputs: {str(e)}")

    return suggestions


condition_map = {
    "new": 4.0,
    "good": 3.0,
    "fair": 2.0,
    "poor": 1.0
}

# Mapping for resolution (for Television)
resolution_map = {
    "720p": 1.0,
    "1080p": 2.0,
    "4k": 3.0,
    "8k": 4.0
}

# Device input configurations
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


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        # print(data);
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        device_type = data.get("device_type")
        inputs = data.get("inputs")
        # print(type(inputs[0]));
        def convert_value(value):
            if isinstance(value, str):  
                if value.isdigit():  # Check if the string is a number
                    return int(value)  
                try:
                    return float(value)  # Convert decimal numbers properly
                except ValueError:
                    return value  # Keep text strings unchanged
            return value  # If it's already a number, keep it as is

        inputs = [convert_value(val) for val in inputs]
        if not device_type or device_type not in device_inputs:
            return jsonify({"error": "Invalid or missing device type"}), 400
        
        if inputs is None:
            return jsonify({"error": "Inputs cannot be None"}), 400

        required_inputs = device_inputs[device_type]

        if len(inputs) != len(required_inputs):
            return jsonify({
                "error": f"Expected {len(required_inputs)} inputs, but got {len(inputs)}"
            }), 400
        # Convert categorical values using mappings
        user_input_dict =inputs
        for i, field in enumerate(required_inputs):
            if "Condition" in field:
                # user_input_dict["Condition"] = inputs[i]
                inputs[i] = condition_map.get(str(inputs[i]).lower(), 1.0)
            elif "Resolution" in field:
                # user_input_dict["Resolution"] = inputs[i]
                inputs[i] = resolution_map.get(str(inputs[i]).lower(), 1.0)
        print(type(user_input_dict))
        inputs = np.array(inputs, dtype=np.float32)

        # Dummy prediction logic (replace with actual model prediction)
        sustainability = float(np.mean(inputs) + np.random.uniform(5, 10))
        lifespan = float(np.mean(inputs) / 10 + np.random.uniform(2, 5))

        print(inputs)

        # Generate suggestions
        # print(inputs)
        suggestions = generate_suggestions(device_type, sustainability, lifespan, user_input_dict)

        return jsonify({
            "device_type": device_type,
            "sustainability": round(sustainability, 2),
            "lifespan": round(lifespan, 2),
            "suggestions": suggestions
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



FEEDBACK_FILE = "feedback.json"

@app.route("/feedback", methods=["POST"])
def feedback():
    try:
        data = request.get_json()

        # Extract all fields from request data
        name = data.get("name", "")
        email = data.get("email", "")
        description = data.get("description", "")
        rating = data.get("rating", 5)
        suggestions = data.get("suggestions", "")

        # Ensure required fields are present
        if not description:
            return jsonify({"error": "Description is required"}), 400

        # Load existing feedback data or initialize empty list if file doesn't exist
        feedback_list = []
        if os.path.exists(FEEDBACK_FILE):
            try:
                with open(FEEDBACK_FILE, "r") as f:
                    feedback_list = json.load(f)
            except json.JSONDecodeError:
                feedback_list = []  # If JSON is corrupt, reset it

        # Append new feedback
        feedback_list.append({
            "name": name,
            "email": email,
            "description": description,
            "rating": rating,
            "suggestions": suggestions
        })

        # Save updated feedback list back to file
        with open(FEEDBACK_FILE, "w") as f:
            json.dump(feedback_list, f, indent=4)

        return jsonify({"message": "Feedback saved successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_feedback", methods=["GET"])
def get_feedback():
    try:
        if not os.path.exists(FEEDBACK_FILE):
            return jsonify({"feedbacks": []}), 200  # Return empty list if file is missing

        with open(FEEDBACK_FILE, "r") as f:
            feedback_list = json.load(f)

        return jsonify({"feedbacks": feedback_list}), 200

    except json.JSONDecodeError:
        return jsonify({"feedbacks": []}), 200  # Return empty list if file is corrupt

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
    # main()
