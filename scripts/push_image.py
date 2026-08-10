import subprocess
import tempfile
import os

BRANCH = "feature-payment-api"
JIRA_ID = "DEVOPS-123"
COMMIT_SHA = "a81f42c"

IMAGE_TAG = f"{BRANCH}-{JIRA_ID}-{COMMIT_SHA}"

SAMPLE_IMAGES = [
    "sample-app-1",
    "sample-app-2",
]

def run_command(command):
    print(f"$ {' '.join(command)}")

    subprocess.run(
        command,
        check=True
    )

def create_sample_image(image_name):

    image_tag = f"{image_name}:{IMAGE_TAG}"

    print(f"\nCreating image: {image_tag}")

    dockerfile_content = """
FROM alpine:latest

CMD ["echo", "Hello from sample Docker image"]
"""
    with tempfile.TemporaryDirectory() as temp_dir:

        dockerfile_path = os.path.join(
            temp_dir,
            "Dockerfile"
        )

        with open(dockerfile_path, "w") as dockerfile:
            dockerfile.write(dockerfile_content)

        run_command([
            "docker",
            "build",
            "-t",
            image_tag,
            temp_dir
        ])

    print(f"Created: {image_tag}")

def main():

    print("=" * 60)
    print("Creating sample Docker images")
    print("=" * 60)

    print(f"\nImage tag format:")
    print(IMAGE_TAG)

    for image_name in SAMPLE_IMAGES:
        create_sample_image(image_name)

    print("\nAll sample images created.")

if __name__ == "__main__":
    main()