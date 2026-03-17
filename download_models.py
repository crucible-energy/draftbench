#!/usr/bin/env python3
"""
Download LLM models for benchmarking using huggingface_hub
"""
import os
from huggingface_hub import hf_hub_download, login
from pathlib import Path

def download_model(repo_id, filename, local_dir):
    """Download a model file from HuggingFace"""
    try:
        print(f"Downloading {filename} from {repo_id}...")
        file_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=local_dir,
            local_dir_use_symlinks=False
        )
        print(f"✅ Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")
        return None

def main():
    models_dir = Path("/Users/sam/Documents/git/crucible/draftbench/models")
    models_dir.mkdir(exist_ok=True)
    
    # Models to download
    models = [
        # Qwen 3.5 Coder models
        {
            "repo_id": "bartowski/Qwen3.5-Coder-7B-Instruct-GGUF",
            "filename": "Qwen3.5-Coder-7B-Instruct-Q4_K_M.gguf",
            "local_name": "qwen3.5-coder-7b-instruct-q4_k_m.gguf"
        },
        {
            "repo_id": "bartowski/Qwen3.5-Coder-1.8B-Instruct-GGUF", 
            "filename": "Qwen3.5-Coder-1.8B-Instruct-Q4_K_M.gguf",
            "local_name": "qwen3.5-coder-1.8b-instruct-q4_k_m.gguf"
        },
        
        # Nemotron models (if available)
        {
            "repo_id": "nvidia/Nemotron-3-100B-Instruct-GGUF",
            "filename": "Nemotron-3-100B-Instruct-Q4_K_M.gguf", 
            "local_name": "nemotron-3-100b-instruct-q4_k_m.gguf"
        },
        {
            "repo_id": "nvidia/Nemotron-3-8B-Instruct-GGUF",
            "filename": "Nemotron-3-8B-Instruct-Q4_K_M.gguf",
            "local_name": "nemotron-3-8b-instruct-q4_k_m.gguf"
        }
    ]
    
    print("🚀 Starting model downloads...")
    print(f"📁 Download directory: {models_dir}")
    
    downloaded = []
    for model in models:
        file_path = download_model(
            model["repo_id"], 
            model["filename"], 
            str(models_dir)
        )
        if file_path:
            # Rename to our preferred naming
            new_path = models_dir / model["local_name"]
            if Path(file_path) != new_path:
                Path(file_path).rename(new_path)
                print(f"📝 Renamed to: {new_path}")
            downloaded.append(model["local_name"])
    
    print(f"\n✨ Download complete! Downloaded {len(downloaded)} models:")
    for model in downloaded:
        print(f"  📄 {model}")
    
    # Update the comprehensive benchmark config
    config_path = Path("/Users/sam/Documents/git/crucible/draftbench/draftbench/configs/comprehensive-benchmark.json")
    if downloaded:
        print(f"\n📝 Updating config file: {config_path}")
        # You can manually update the config paths now

if __name__ == "__main__":
    main()
