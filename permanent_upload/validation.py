import csv
import os


def validate_supported_types(results, data_file="data/supported_file_types.csv"):
    validation_dataset = {}
    data_file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), data_file
    )
    with open(data_file_path, "r") as csvfile:
        validation_reader = csv.reader(csvfile)
        for row in validation_reader:
            validation_dataset[row[0]] = row[1:]
    for result in results:
        extension = result[0].split(".")[1]
        assert validation_dataset[extension]
        # File type classification (e.g. audio, image)
        assert validation_dataset[extension][0] == result[1]
        # Final status (e.g. ok, manual_review)
        assert validation_dataset[extension][1] == result[2]
        # File conversions (e.g. html,pdfa,txt)
        assert validation_dataset[extension][2] == result[3]
        # Conversion don't take longer than 60 seconds
        assert result[4] < 60
