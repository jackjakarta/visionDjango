import base64


# Moved to utils.validators (don't delete because of migration file)
def validate_video_extension():
    pass


def image_to_base64(img_path: str) -> str:
    with open(img_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    return base64_image
