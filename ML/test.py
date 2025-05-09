import pandas as pd
from score import init, run

# Initialize the model
init()

# Prompt the user to enter a job title
job_title = input("\nEnter job title: \n")

# Call the 'run' function with the provided job title
result = run(job_title)

# Print the prediction
if "error" in result:
    print(f"Error: {result['error']}")
else:
    print("\nPredictions:\n")
    for prediction in result["predictions"]:
        print(prediction)
    print()  