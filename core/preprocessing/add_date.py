import pandas as pd


def add_date_to_data(
    data: pd.DataFrame, date_column_name: str | None = None
) -> pd.DataFrame:
    df = data.copy()
    date_column = df[date_column_name] if date_column_name else df.index

    # Convert to days starting on Sunday
    df["date"] = pd.to_datetime(date_column, unit="D", origin=3)

    # Convert to weekday (1=Sunday, 7=Saturday)
    df["day"] = (df["date"].dt.day_of_week + 1) % 7 + 1
    df["week"] = df["date"].dt.isocalendar().week
    return df
