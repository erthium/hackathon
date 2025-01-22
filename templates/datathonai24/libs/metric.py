import pandas as pd
import pandas.api.types
import numpy as np

class ParticipantVisibleError(Exception):
    pass

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the Haversine distance between two points on Earth.
    
    Args:
        lat1: Latitude of first point in degrees
        lon1: Longitude of first point in degrees
        lat2: Latitude of second point in degrees
        lon2: Longitude of second point in degrees
        
    Returns:
        Distance between points in kilometers
    """
    R = 6371  # Earth's radius in kilometers

    # Convert to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Haversine formula
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    return R * c

def score(solution: pd.DataFrame, submission: pd.DataFrame, row_id_column_name: str, 
         lat_column: str = "latitude", lon_column: str = "longitude") -> float:
    """
    Calculate RMSE using Haversine distance between predicted and true coordinates.
    
    Args:
        solution: DataFrame containing true coordinates
        submission: DataFrame containing predicted coordinates
        row_id_column_name: Name of the ID column
        lat_column: Name of the latitude column (default: "latitude")
        lon_column: Name of the longitude column (default: "longitude")
        
    Returns:
        RMSE score in kilometers
        
    Example:
        >>> import pandas as pd
        >>> row_id_column_name = "id"
        >>> solution = pd.DataFrame({
        ...     "id": [0, 1],
        ...     "latitude": [40.7128, 34.0522],
        ...     "longitude": [-74.0060, -118.2437]
        ... })
        >>> submission = pd.DataFrame({
        ...     "id": [0, 1],
        ...     "latitude": [40.7128, 34.0522],
        ...     "longitude": [-74.0060, -118.2437]
        ... })
        >>> round(score(solution.copy(), submission.copy(), row_id_column_name), 6)
        0.0
    """
    # Verify both DataFrames have the required columns
    required_columns = {row_id_column_name, lat_column, lon_column}
    if not required_columns.issubset(solution.columns):
        raise ParticipantVisibleError(f"Solution must contain columns: {required_columns}")
    if not required_columns.issubset(submission.columns):
        raise ParticipantVisibleError(f"Submission must contain columns: {required_columns}")
        
    # Remove ID column as it's not needed for calculation
    del solution[row_id_column_name]
    del submission[row_id_column_name]
    
    # Verify numeric data types
    for df, name in [(submission, "Submission"), (solution, "Solution")]:
        for col in [lat_column, lon_column]:
            if not pandas.api.types.is_numeric_dtype(df[col]):
                raise ParticipantVisibleError(f"{name} column {col} must be numeric")
    
    # Verify latitude and longitude ranges
    for df, name in [(submission, "Submission"), (solution, "Solution")]:
        if (df[lat_column] < -90).any() or (df[lat_column] > 90).any():
            raise ParticipantVisibleError(f"{name} latitudes must be between -90 and 90 degrees")
        if (df[lon_column] < -180).any() or (df[lon_column] > 180).any():
            raise ParticipantVisibleError(f"{name} longitudes must be between -180 and 180 degrees")
    
    # Calculate Haversine distances between predicted and true coordinates
    distances = [
        haversine_distance(
            solution[lat_column].iloc[i],
            solution[lon_column].iloc[i],
            submission[lat_column].iloc[i],
            submission[lon_column].iloc[i]
        )
        for i in range(len(solution))
    ]
    
    # Calculate RMSE
    rmse = np.sqrt(np.mean(np.array(distances) ** 2))
    
    return float(rmse)
