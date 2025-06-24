import os
from typing import List
import pandas as pd

from libs.metric import score
from libs.utils import directory_checks, get_predict_from_repo


# Constants
TEMPLATE_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(TEMPLATE_ROOT_DIR, "dataset")
TEST_DATASET_DIR = os.path.join(DATA_DIR, "") # for testing purposes, data is directly in the dataset directory
SOLUTIONS_CSV_PATH = os.path.join(TEST_DATASET_DIR, "solutions.csv")


def get_solutions() -> pd.DataFrame:
  return pd.read_csv(SOLUTIONS_CSV_PATH)


def validate_predictions(predictions: pd.DataFrame, solutions: pd.DataFrame) -> bool:
  # Check if the predictions have the right columns, apart from the last 'Usage' column
  if len(predictions.columns) != len(solutions.columns) - 1:
    return False
  
  # Check if the predictions have the right column names, apart from the last 'Usage' column
  if not all(predictions.columns == solutions.columns[:-1]):
    return False
  
  # Check if the predictions have the right data types, apart from the last 'Usage' column
  if not all(predictions.dtypes == solutions.iloc[:, :-1].dtypes):
    return False
  
  # Check if the predictions have the same number of rows as the solutions
  if len(predictions) != len(solutions):
    return False


def get_score(predictions: pd.DataFrame, solutions: pd.DataFrame) -> float:
  """
  This functions used to separate the public and private scores, using the last 'Usage' column in the solutions DataFrame.
  """
  public_solutions = solutions[solutions["Usage"] == "Public"]
  private_solutions = solutions[solutions["Usage"] == "Private"]

  public_predictions = predictions.loc[public_solutions.index]
  private_predictions = predictions.loc[private_solutions.index]

  public_score = score(public_solutions, public_predictions, "filename")
  private_score = score(private_solutions, private_predictions, "filename")

  return public_score, private_score


def evaluate_predictions(repository_path: str):
  # Get the user predictions
  predict: callable = get_predict_from_repo(repository_path)
  predictions: pd.DataFrame = predict(TEST_DATASET_DIR)

  solutions = get_solutions()

  # Validate the predictions
  if not validate_predictions(predictions, solutions):
    raise ValueError("Predictions are not valid")

  # Evaluate the predictions
  public_score, private_score = get_score(predictions, solutions)

  print(f"Public score: {public_score}")
  print(f"Private score: {private_score}")


def main():
  import argparse
  parser = argparse.ArgumentParser()
  parser = argparse.ArgumentParser()
  parser.add_argument("--repo", type=str, required=True)
  args = parser.parse_args()
  repository_path = args.repo

  directory_checks(repository_path)
  evaluate_predictions(repository_path)
