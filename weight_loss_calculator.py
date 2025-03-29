def calculate_bmr(weight, height, age, gender):
     #Mifflin-St Jeor Equation.

    if gender.lower() == "male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    elif gender.lower() == "female":
        return 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Invalid gender. Please specify 'male' or 'female'.")


def calculate_tdee(bmr, activity_level):

    activity_factors = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extra active": 1.9,
    }
    if activity_level not in activity_factors:
        raise ValueError("Invalid activity level. Choose from: " + ", ".join(activity_factors.keys()))
    return bmr * activity_factors[activity_level]


def weight_loss_prediction(weight, height, age, gender, activity_level, calorie_deficit, duration_weeks):
    """
    Predict weight loss based on inputs.
    """
    # Calculate BMR and TDEE
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity_level)

    # Calorie deficit per week and weight loss
    weekly_deficit = calorie_deficit * 7  # Calories per week
    weight_loss_per_week = weekly_deficit / 7700
    # Predict total weight loss over the duration
    total_weight_loss = weight_loss_per_week * duration_weeks

    # Final weight prediction
    final_weight = weight - total_weight_loss
    return {
        "initial_weight": weight,
        "final_weight": final_weight,
        "total_weight_loss": total_weight_loss,
        "tdee": tdee,
        "bmr": bmr,
    }


# Example input
if __name__ == "__main__":
    print("Weight Loss Prediction Calculator\n")

    try:
        # User inputs
        weight = float(input("Enter your weight in kg: "))
        height = float(input("Enter your height in cm: "))
        age = int(input("Enter your age in years: "))
        gender = input("Enter your gender (male/female): ").strip().lower()
        activity_level = input(
            "Enter your activity level (sedentary, lightly active, moderately active, very active, extra active): "
        ).strip().lower()
        calorie_deficit = float(input("Enter your daily calorie deficit (e.g., 500 for 500 kcal/day): "))
        duration_weeks = int(input("Enter the duration of the weight loss plan in weeks: "))

        # Calculate weight loss prediction
        result = weight_loss_prediction(weight, height, age, gender, activity_level, calorie_deficit, duration_weeks)

        # Output results
        print("\n--- Weight Loss Prediction ---")
        print(f"Initial Weight: {result['initial_weight']} kg")
        print(f"Final Weight: {result['final_weight']:.2f} kg")
        print(f"Total Weight Loss: {result['total_weight_loss']:.2f} kg")
        print(f"Basal Metabolic Rate (BMR): {result['bmr']:.2f} kcal/day")
        print(f"Total Daily Energy Expenditure (TDEE): {result['tdee']:.2f} kcal/day")
    except ValueError as e:
        print(f"Error: {e}")
