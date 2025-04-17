# Device Sustainability and Lifespan Prediction Using Reinforcement Learning  

## Overview  
This project uses **Reinforcement Learning (RL)** to predict the **sustainability** and **lifespan** of electronic devices. By analyzing user-provided data, the system generates a sustainability score, estimates device lifespan, and provides actionable suggestions to enhance the device's performance and longevity.  

The goal is to empower users to make eco-conscious decisions, reduce e-waste, and maximize their device's efficiency.  

---

## Features  
- **Customizable User Inputs:** Supports multiple device types (e.g., Laptops, Smartphones, Smartwatches), each with tailored input fields.  
- **Reinforcement Learning Model:** Utilizes Deep Q-Learning (DQN) to predict optimal actions based on the device's current state.  
- **Actionable Insights:** Offers personalized suggestions for improving device sustainability and performance.  
- **Interactive Design:** Easy-to-use prompts ensure non-technical users can interact with the system seamlessly.  

---

## System Workflow  

1. **User Input:**  
   - Users provide details about their device (e.g., age, usage hours, condition, battery health).  
   - Input validation ensures accurate and error-free data collection.  

2. **Reinforcement Learning:**  
   - A custom environment simulates device behavior using a defined **observation space** and **action space**.  
   - The RL model predicts the optimal action to improve the device's condition.  

3. **Output:**  
   - **Sustainability Score:** Indicates environmental and operational efficiency.  
   - **Lifespan Estimate:** Predicts the remaining years of functionality.  
   - **Suggestions:** Provides actionable advice (e.g., reducing usage, upgrading hardware, or performing maintenance).  

---

## Installation  

### Prerequisites  
- Python 3.8 or later  
- Virtual Environment (optional but recommended)  

### Required Libraries  
Install the required dependencies using the following command:  
    pip install numpy pandas matplotlib stable-baselines3 gym openpyxl

### Example Case
Input:
    Device Type: Laptop
    Age: 3 years
    Daily Usage: 6 hours
    Condition: Good (mapped to a numerical value internally)
    Battery Health: 70%
Output:
    Sustainability Score: 85/100
    Estimated Lifespan: 4 years
Suggestions:
    Consider upgrading the battery if performance declines.
    Limit daily usage to under 8 hours for optimal performance.

---

