from functools import wraps
from collections import defaultdict
from pandas import DataFrame


def limit_by_brand_decorator(max_per_brand=2, top_n=5, brand_col="brand", pid_col="pid"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            df = func(*args, **kwargs)
            if not isinstance(df, DataFrame):
                return df

            brand_counter = defaultdict(int)
            result = []

            for _, row in df.iterrows():
                brand = row[brand_col]
                pid = row[pid_col]

                if brand_counter[brand] < max_per_brand:
                    result.append(pid)
                    brand_counter[brand] += 1

                if len(result) == top_n:
                    break

            return result
        return wrapper
    return decorator
