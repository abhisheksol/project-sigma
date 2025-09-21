import json
import uuid

# Input file (original fixture)
INPUT_FILE = "input_fixture.json"
# Output file (transformed fixture)
OUTPUT_FILE = "mapped_fixture.json"
# Template ID to map
TEMPLATE_ID = "863b3570-4700-4a78-a340-9d343718f150"  # <-- replace as needed


def transform_fixture(input_file: str, output_file: str, template_id: str):
    with open(input_file, "r") as f:
        data = json.load(f)

    transformed: list = []
    for entry in data:
        model = entry.get("model")
        fields = entry.get("fields", {})

        # Assign new UUID if pk missing or looks invalid
        pk = entry.get("pk")
        if not pk:
            pk = str(uuid.uuid4())

        # Force template mapping only for ProcessTemplateFieldMappingModel
        if model == "template_config.processtemplatefieldmappingmodel":
            fields["template"] = template_id

        transformed.append(
            {
                "model": model,
                "pk": pk,
                "fields": fields,
            }
        )

    with open(output_file, "w") as f:
        json.dump(transformed, f, indent=2)

    print(f"✅ Transformed fixture saved → {output_file}")


if __name__ == "__main__":
    transform_fixture(INPUT_FILE, OUTPUT_FILE, TEMPLATE_ID)
