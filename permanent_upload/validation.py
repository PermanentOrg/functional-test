import csv
import os


def _load_validation_dataset(data_file="data/supported_file_types.csv"):
    dataset = {}
    data_file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), data_file
    )
    with open(data_file_path, "r") as csvfile:
        for row in csv.DictReader(csvfile):
            dataset[row["file_extension"]] = row
    return dataset


def load_expected_formats(data_file="data/supported_file_types.csv"):
    return {
        ext: set(row["conversions"].split(","))
        for ext, row in _load_validation_dataset(data_file).items()
    }


def validate_supported_types(results, data_file="data/supported_file_types.csv"):
    validation_dataset = _load_validation_dataset(data_file)
    for result in results:
        extension = result[0].split(".")[-1]
        assert validation_dataset[extension]
        # File type classification (e.g. audio, image)
        assert result[1] == validation_dataset[extension]["file_category"]
        # Final status (e.g. ok, manual_review)
        assert result[2] in set(
            [validation_dataset[extension]["final_status"], "uploaded", "ok"]
        )
        if result[2] == "ok":
            # File conversions (e.g. html,pdfa,txt)
            assert set(result[3]) >= set(validation_dataset[extension]["conversions"])
