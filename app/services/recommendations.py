import os

from pandas import read_csv, DataFrame
from app.services.utils.utils import limit_by_brand_decorator


class RecommendationsService:
    def __init__(self):
        self._csv_path = None
        self._click_weight = 1
        self._cart_weight = 2
        self._purchase_weight = 3

    def _load_data(self) -> DataFrame:
        if self._csv_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.csv_path = os.path.join(base_dir, "..", "test.csv")

        df = read_csv(self.csv_path)

        df["uid"] = df["uid"].astype(int)
        df["pid"] = df["pid"].astype(int)

        if "Unnamed: 0" in df.columns:
            df = df.drop(columns=["Unnamed: 0"])

        return df

    def get_user_recommendations(self, user_id: int) -> list[int]:
        df = self._load_data()

        if user_id in df["uid"].values:
            return self._recommend_for_existing_user(df=df, user_id=user_id)
        else:
            return self._recommend_for_new_user(df=df)

    @limit_by_brand_decorator()
    def _recommend_for_existing_user(self, df: DataFrame, user_id: int) -> list[int]:
        user_df = df[df["uid"] == user_id]

        if user_df.empty:
            return []

        purchased_pids = user_df.loc[user_df["purchase"] > 0, "pid"].unique()

        scored = (
            user_df[~user_df["pid"].isin(purchased_pids)]
            .assign(
                interest_score=lambda x: x["click"] * self._click_weight + x["add_to_cart"] * self._cart_weight
            )
            .groupby(["pid", "brand"], as_index=False)["interest_score"]
            .sum()
            .sort_values(by="interest_score", ascending=False)
        )

        return scored

    @limit_by_brand_decorator()
    def _recommend_for_new_user(self, df: DataFrame) -> list[int]:
        scored = (
            df.assign(
                popularity_score=lambda x: (
                        x["click"] * self._click_weight +
                        x["add_to_cart"] * self._cart_weight +
                        x["purchase"] * self._purchase_weight
                )
            )
            .groupby(["pid", "brand"], as_index=False)["popularity_score"]
            .sum()
            .sort_values(by="popularity_score", ascending=False)
        )

        return scored




