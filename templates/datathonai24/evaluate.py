import os
import sys

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIRECTORY)

LIBS_DIRECTORY = os.path.join(SCRIPT_DIRECTORY, "libs")
sys.path.append(LIBS_DIRECTORY)

from typing import List, Optional
import pandas as pd

from libs.metric import score
from libs.utils import directory_checks, get_predict_from_repo, write_command_result


# Constants
TEMPLATE_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(TEMPLATE_ROOT_DIR, "dataset")
TEST_DATASET_DIR = os.path.join(DATA_DIR, "") # for testing purposes, data is directly in the dataset directory
SOLUTIONS_CSV_PATH = os.path.join(TEST_DATASET_DIR, "solutions.csv")


def get_solutions() -> pd.DataFrame:
  return pd.read_csv(
    SOLUTIONS_CSV_PATH,
    dtype={
      "filename": str,
      "latitude": float,
      "longitude": float,
      "Usage": str,
    },
    sep=";",
  )


def validate_predictions(predictions: pd.DataFrame, solutions: pd.DataFrame) -> bool:
  # Check if the predictions have the right columns, apart from the last 'Usage' column
  if len(predictions.columns) != len(solutions.columns) - 1:
    print(f"Predictions does not have the right number of columns: {len(predictions.columns)} != {len(solutions.columns) - 1}")
    return False
  
  # Check if the predictions have the right column names, apart from the last 'Usage' column
  if not all(predictions.columns == solutions.columns[:-1]):
    print(f"Predictions does not have the right column names: {predictions.columns} != {solutions.columns[:-1]}")
    return False
  
  # Check if the predictions have the right data types, apart from the last 'Usage' column
  if not all(predictions.dtypes == solutions.iloc[:, :-1].dtypes):
    print(f"Predictions does not have the right data types: {predictions.dtypes} != {solutions.iloc[:, :-1].dtypes}")
    return False
  
  # Check if the predictions have the same number of rows as the solutions
  if len(predictions) != len(solutions):
    print(f"Predictions does not have the same number of rows as the solutions: {len(predictions)} != {len(solutions)}")
    return False

  return True


def get_score(predictions: pd.DataFrame, solutions: pd.DataFrame) -> float:
  """
  This functions used to separate the public and private scores, using the last 'Usage' column in the solutions DataFrame.
  """
  public_solutions = solutions[solutions["Usage"] == "Public"]
  private_solutions = solutions[solutions["Usage"] == "Private"]

  print(f"Public solutions: {len(public_solutions)}")
  for index, row in public_solutions.iterrows():
    print(f"Public solution {index}: {row['filename']}")
  print(f"Private solutions: {len(private_solutions)}")
  for index, row in private_solutions.iterrows():
    print(f"Private solution {index}: {row['filename']}")

  public_predictions = predictions.loc[public_solutions.index]
  private_predictions = predictions.loc[private_solutions.index]

  public_score = score(public_solutions, public_predictions, "filename")
  private_score = score(private_solutions, private_predictions, "filename")

  return public_score, private_score


def evaluate_predictions(repository_path: str):
  # Get the user predictions
  data = {
    "success": False,
    "error": None,
    "scores": [],
  }
  
  predict: callable = get_predict_from_repo(repository_path)
  try:
    predictions: pd.DataFrame = predict(TEST_DATASET_DIR)
  except Exception as e:
    data["error"] = str(e)
    write_command_result(data)
    raise e

  if not isinstance(predictions, pd.DataFrame):
    data["error"] = "Predictions are not a DataFrame"
    write_command_result(data)
    raise TypeError("Predictions are not a DataFrame")

  solutions = get_solutions()

  # print the first few rows of the predictions and solutions for debugging
  print("Predictions:")
  print(predictions.head())
  print("Solutions:")
  print(solutions.head())

  # Validate the predictions
  if not validate_predictions(predictions, solutions):
    data["error"] = "Predictions are not valid"
    write_command_result(data)
    raise ValueError("Predictions are not valid")

  # Evaluate the predictions
  public_score, private_score = get_score(predictions, solutions)

  print(f"Public score: {public_score}")
  print(f"Private score: {private_score}")
  data["success"] = True
  data["scores"] = [public_score, private_score]
  write_command_result(data)


def main():
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("repository_path", type=str, help="Path to the repository to evaluate")
  args = parser.parse_args()
  repository_path: str = args.repository_path
  
  directory_checks(repository_path)
  evaluate_predictions(repository_path)


if __name__ == "__main__":
  main()
