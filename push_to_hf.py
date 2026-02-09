"""Push phase-2 backend to HuggingFace Space."""
import os
from huggingface_hub import HfApi, login

# Get HF token from environment
hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    print("HF_TOKEN not set. Please set HF_TOKEN environment variable.")
    print("You can get your token from: https://huggingface.co/settings/tokens")
    exit(1)

# Strip any whitespace from token
hf_token = hf_token.strip()

# Login to HuggingFace
login(token=hf_token)

# Initialize HF API
api = HfApi()

# Space name and repo_id
space_name = "todo-backend"
repo_id = f"amnaaplus/{space_name}"

print(f"Pushing phase-2/backend to https://huggingface.co/spaces/{repo_id}")

# Files to upload from phase-2/backend
files_to_upload = [
    "main.py",
    "middleware/jwt_auth.py",
    "middleware/__init__.py",
    "routes/tasks.py",
    "routes/__init__.py",
    "models/task.py",
    "models/__init__.py",
    "database.py",
    "requirements.txt",
    "Dockerfile",
]

# Upload each file
for filepath in files_to_upload:
    full_path = f"phase-2/backend/{filepath}"
    if os.path.exists(full_path):
        print(f"Uploading {filepath}...")
        api.upload_file(
            path_or_fileobj=full_path,
            path_in_repo=filepath,
            repo_id=repo_id,
            repo_type="space",
            commit_message=f"Update {filepath}"
        )
        print(f"  ✓ {filepath} uploaded")
    else:
        print(f"  ✗ {filepath} not found")

print("\nDone! The Space should rebuild automatically.")
print(f"Check: https://huggingface.co/spaces/{repo_id}")
