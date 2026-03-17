
from huggingface_hub import snapshot_download
from pathlib import Path

def download_draft_model():
    repo_id = "Qwen/Qwen2.5-0.5B-Instruct"
    local_dir = Path("/Users/sam/Documents/git/crucible/draftbench/models")
    
    print(f"🚀 Downloading {repo_id} to {local_dir}...")
    
    path = snapshot_download(
        repo_id=repo_id,
        local_dir=local_dir / f"models--{repo_id.replace('/', '--')}",
        local_dir_use_symlinks=False
    )
    
    print(f"✅ Downloaded to: {path}")

if __name__ == "__main__":
    download_draft_model()
