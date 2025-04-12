import pandas as pd

def hf(data, threshold=1000):
    def human_format(num):
        if isinstance(num, int) and abs(num) < threshold:
            return num
        if not isinstance(num, (int, float)):
            return num
        magnitude = 0
        while abs(num) >= 1000 and magnitude < 4:
            magnitude += 1
            num /= 1000.0
        return f'{num:.1f}{" KMBT"[magnitude]}'.strip()
    
    if isinstance(data, (int, float)):
        return human_format(data)
    
    if isinstance(data, pd.DataFrame):
        df_copy = data.copy()
        for col in df_copy.select_dtypes(include=['int64', 'float64']):
            df_copy[col] = df_copy[col].apply(human_format)
        return df_copy

    return data  # If it's some other type, return as-is

def add_recursive_cols(df, row_fn):
    df = df.copy()
    results = {col: [] for col in row_fn(df.iloc[0], None).keys()}

    prev = None
    for i in range(len(df)):
        curr = df.iloc[i]
        new_vals = row_fn(curr, prev)
        for k, v in new_vals.items():
            results[k].append(v)
        prev = curr.to_dict() | new_vals  # merged state for the next row

    for col, vals in results.items():
        df[col] = vals

    return df
