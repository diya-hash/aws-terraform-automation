import subprocess
import tempfile
import os
from pathlib import Path

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

def get_ecr_url():
    script_dir = Path(__file__).resolve().parent

    project_root = script_dir.parent

    terraform_dir = project_root / "ecr"

    result = subprocess.run(
        [
            "terraform",
            f"-chdir={terraform_dir}",
            "output",
            "-raw",
            "ecr_repository_url"
        ],
        capture_output=True,
        text=True,
        check=True
    )

    return result.stdout.strip()

def login_to_ecr(ecr_url):

    registry = ecr_url.split("/")[0]

    print(f"\nLogging into ECR registry: {registry}")

    password = subprocess.run(
        [
            "aws",
            "ecr",
            "get-login-password",
            "--region",
            "us-east-1"
        ],
        capture_output=True,
        text=True,
        check=True
    )

    subprocess.run(
        [
            "docker",
            "login",
            "--username",
            "AWS",
            "--password-stdin",
            registry
        ],
        input=password.stdout,
        text=True,
        check=True
    )

    print("Successfully logged into ECR.")

def push_image(ecr_url, image_name):

    local_image = f"{image_name}:{IMAGE_TAG}"

    ecr_image = f"{ecr_url}:{image_name}-{IMAGE_TAG}"

    print(f"\nTagging image:")
    print(f"  Local: {local_image}")
    print(f"  ECR:   {ecr_image}")

    subprocess.run(
        [
            "docker",
            "tag",
            local_image,
            ecr_image
        ],
        check=True
    )

    print(f"\nPushing image:")
    print(f"  {ecr_image}")

    subprocess.run(
        [
            "docker",
            "push",
            ecr_image
        ],
        check=True
    )

    print(f"\nSuccessfully pushed: {ecr_image}")

def main():

    print("=" * 60)
    print("Docker → ECR Automation")
    print("=" * 60)


    print("\nPART 1: Creating sample images")

    for image_name in SAMPLE_IMAGES:
        create_sample_image(image_name)

    print("\nPART 2: Getting ECR URL")

    ecr_url = get_ecr_url()

    print(f"ECR URL: {ecr_url}")

    print("\nPART 3: Pushing images to ECR")

    login_to_ecr(ecr_url)

    for image_name in SAMPLE_IMAGES:
        push_image(ecr_url, image_name)

    print("\nAll images pushed successfully!")


if __name__ == "__main__":
    main()