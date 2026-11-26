import unicodedata

from app.sample.restaurants import SAMPLE_RESTAURANTS


def _contains_thai_letters_or_digits(text):
    return any(
        unicodedata.name(character, "").startswith(
            ("THAI CHARACTER", "THAI DIGIT")
        )
        for character in text
    )


def test_sample_dataset_is_complete_and_english():
    assert len(SAMPLE_RESTAURANTS) == 19
    assert sum(len(restaurant["menu"]) for restaurant in SAMPLE_RESTAURANTS) == 266

    content = [restaurant["name"] for restaurant in SAMPLE_RESTAURANTS]
    content.extend(
        dish["dish"]
        for restaurant in SAMPLE_RESTAURANTS
        for dish in restaurant["menu"]
    )

    assert not any(_contains_thai_letters_or_digits(text) for text in content)
