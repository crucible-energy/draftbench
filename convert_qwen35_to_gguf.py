#!/usr/bin/env python3
"""
Convert Qwen 3.5 models from HuggingFace to GGUF format
"""
import os
import subprocess
import sys
from pathlib import Path

def convert_model_to_gguf(model_name, output_dir, quantization="q4_k_m"):
    """Convert a HuggingFace model to GGUF"""
    
    print(f"🔄 Converting {model_name} to GGUF ({quantization})")
    print("=" * 60)
    
    # Paths
    neural_llama_dir = Path("/Users/sam/Documents/git/crucible/neural-llama")
    convert_script = neural_llama_dir / "convert_hf_to_gguf.py"
    models_dir = Path("/Users/sam/Documents/git/crucible/draftbench/models")
    
    # Check if model exists
    model_dir = models_dir / f"models--{model_name.replace('/', '--')}"
    if not model_dir.exists():
        print(f"❌ Model directory not found: {model_dir}")
        return False
    
    # Resolve snapshot if it's an HF cache directory
    snapshots_dir = model_dir / "snapshots"
    if snapshots_dir.exists():
        snapshots = sorted(list(snapshots_dir.iterdir()))
        if snapshots:
            model_dir = snapshots[-1]
            print(f"📂 Found snapshot: {model_dir}")
    
    # Convert to GGUF
    output_file = output_dir / f"{model_name.split('/')[-1]}-{quantization}.gguf"
    
    convert_cmd = [
        sys.executable,
        str(convert_script),
        str(model_dir),
        "--outfile", str(output_file),
        "--outtype", "f16" if quantization == "f16" else quantization,
    ]
    
    print(f"🔧 Running conversion:")
    print(f"   {' '.join(convert_cmd)}")
    
    try:
        result = subprocess.run(convert_cmd, check=True, capture_output=True, text=True, cwd=neural_llama_dir)
        
        if output_file.exists():
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"✅ Conversion successful!")
            print(f"📄 Output: {output_file}")
            print(f"📊 Size: {size_mb:.1f} MB")
            return str(output_file)
        else:
            print(f"❌ Conversion failed - output file not created")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Conversion failed: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def main():
    """Main conversion function"""
    
    # Models to convert
    models_to_convert = [
        ("Qwen/Qwen3.5-9B", "f16"),
        ("Qwen/Qwen3.5-27B", "f16"),
        ("Qwen/Qwen3.5-35B-A3B", "f16"),
    ]
    
    # Output directory
    output_dir = Path("/Users/sam/Documents/git/crucible/draftbench/models")
    output_dir.mkdir(exist_ok=True)
    
    print("🚀 Qwen 3.5 to GGUF Conversion Suite")
    print("=" * 60)
    
    converted_files = []
    
    for model_name, quantization in models_to_convert:
        # Skip larger models for now to avoid memory issues
        if "27B" in model_name or "35B" in model_name:
            print(f"⚠️  Skipping {model_name} - too large for initial conversion")
            continue
        
        output_file = convert_model_to_gguf(model_name, output_dir, quantization)
        if output_file:
            converted_files.append(output_file)
    
    # Summary
    print(f"\n🎉 Conversion Summary")
    print("=" * 60)
    
    if converted_files:
        print(f"✅ Successfully converted {len(converted_files)} models:")
        for file in converted_files:
            size_mb = Path(file).stat().st_size / (1024 * 1024)
            print(f"  📄 {Path(file).name} ({size_mb:.1f} MB)")
        
        # Create benchmark config
        config = {
            "name": "qwen3.5-converted-benchmark",
            "hardware": "m3-max-apple-silicon",
            "backend": "neural-llama",
            "model_family": "Qwen 3.5 (Converted GGUF)",
            "targets": [],
            "drafts": [],
            "settings": {
                "llama_bin": "/Users/sam/Documents/git/crucible/neural-llama/build-apple-silicon/bin/llama-server",
                "runs": 2,
                "max_tokens": 256,
                "temperature": 0.0,
                "gpu_layers": 99,
                "ctx_size": 4096,
                "port": 8080
            }
        }
        
        # Add converted models to config
        for file in converted_files:
            model_path = Path(file)
            model_name = model_path.stem.replace("-q4_k_m", "")
            
            config["targets"].append({
                "label": model_name,
                "path": str(model_path)
            })
        
        # Save config
        config_file = output_dir.parent / "draftbench" / "configs" / "qwen3.5-converted.json"
        config_file.parent.mkdir(exist_ok=True)
        
        import json
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\n📝 Created benchmark config: {config_file}")
        print(f"🚀 Run benchmark: python3 sweep.py --config configs/qwen3.5-converted.json")
        
    else:
        print(f"❌ No models were successfully converted")
        print(f"\n💡 Troubleshooting:")
        print(f"   1. Check if model files are downloaded correctly")
        print(f"   2. Verify neural-llama conversion tools are built")
        print(f"   3. Try with smaller models first")

if __name__ == "__main__":
    main()
