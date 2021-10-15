import csv
import os


def validate_supported_types(results, data_file="data/supported_file_types.csv"):
    validation_dataset = {}
    data_file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), data_file
    )
    with open(data_file_path, "r") as csvfile:
        validation_reader = csv.DictReader(csvfile)
        for row in validation_reader:
            validation_dataset[row["file_extension"]] = row
    for result in results:
        extension = result[0].split(".")[-1]
        assert validation_dataset[extension]
        # File type classification (e.g. audio, image)
        assert validation_dataset[extension]["file_category"] == result[1]
        # Final status (e.g. ok, manual_review)
        assert validation_dataset[extension]["final_status"] in set(
            [result[2], "uploaded", "ok"]
        )
        if validation_dataset[extension]["final_status"] == "ok":
            # File conversions (e.g. html,pdfa,txt)
            assert validation_dataset[extension]["conversions"] == result[3]
