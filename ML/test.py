from score import init, run

# Initialize the model
init()

# Path to your CSV file
csv_file_path = "jobtitles_test.csv"

# Call the 'run' function with the CSV file path
result = run(csv_file_path)

# Print the predictions
if "error" in result:
    print(f"Error: {result['error']}")
else:
    print("Predictions:")
    for prediction in result["predictions"]:
        print(prediction)