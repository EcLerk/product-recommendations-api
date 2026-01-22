def test_existing_user_gets_recommendations(recommendations_service):
    result = recommendations_service.get_user_recommendations(user_id=1)

    assert isinstance(result, list)
    assert len(result) <= 5
    assert result == [101, 103]


def test_purchased_products_are_excluded(recommendations_service):
    result = recommendations_service.get_user_recommendations(user_id=1)

    assert 102 not in result


def test_new_user_gets_popular_products(recommendations_service):
    result = recommendations_service.get_user_recommendations(user_id=999)

    assert isinstance(result, list)
    assert len(result) <= 5
    assert result == [105, 101, 102, 104, 103]


def test_brand_limit(sample_df, recommendations_service):
    result = recommendations_service.get_user_recommendations(user_id=999)

    pid_to_brand = (
        sample_df
        .drop_duplicates("pid")
        .set_index("pid")["brand"]
        .to_dict()
    )

    brand_counts = {}
    for pid in result:
        brand = pid_to_brand[pid]
        brand_counts[brand] = brand_counts.get(brand, 0) + 1

    assert all(count <= 2 for count in brand_counts.values())
