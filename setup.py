#!/usr/bin/env python3
"""
Complete setup script for TTS + Wav2Lip project
Handles: requirements installation, Wav2Lip setup, compatibility fixes, and model downloads
"""

import os
import subprocess
import sys
from pathlib import Path

class TTSSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.wav2lip_dir = self.project_root / "backend" / "extras" / "Wav2Lip"
        self.checkpoint_path = self.wav2lip_dir / "checkpoints" / "wav2lip_gan.pth"
        
    def print_header(self, title):
        """Print formatted section header"""
        print(f"\n{'='*50}")
        print(f"{title}")
        print(f"{'='*50}")
    
    def run_command(self, cmd, description=None):
        """Run shell command with error handling"""
        if description:
            print(f"{description}...")
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=self.project_root)
            if result.returncode != 0:
                print(f"Command failed: {cmd}")
                if result.stderr:
                    print(f"Error: {result.stderr}")
                return False
            if result.stdout:
                print(result.stdout.strip())
            return True
        except Exception as e:
            print(f"Error running command: {e}")
            return False

    def check_python_version(self):
        """Check if Python version is compatible"""
        version = sys.version_info
        print(f"Python version: {version.major}.{version.minor}.{version.micro}")
        
        if version.major != 3 or version.minor < 8:
            print("Python 3.8+ required")
            return False
        
        if version.minor > 10:
            print("Python 3.11+ may have compatibility issues with some dependencies")
        
        print("Python version compatible")
        return True

    def install_requirements(self):
        """Install project requirements"""
        self.print_header("Installing Requirements")
        
        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            print("requirements.txt not found")
            return False
        
        print("Installing Python dependencies...")
        success = self.run_command("pip install -r requirements.txt", "Installing requirements")
        
        if success:
            print("Requirements installed successfully")
        return success

    def clone_wav2lip(self):
        """Clone Wav2Lip repository if not exists"""
        if self.wav2lip_dir.exists():
            print("Wav2Lip directory already exists")
            return True
        
        print("Cloning Wav2Lip repository...")
        # Create the backend/extras directory first
        self.wav2lip_dir.parent.mkdir(parents=True, exist_ok=True)
        
        # Clone to the correct directory
        success = self.run_command(f"git clone https://github.com/Rudrabha/Wav2Lip.git {self.wav2lip_dir}")
        
        if success:
            print("Wav2Lip cloned successfully")
        return success

    def fix_wav2lip_compatibility(self):
        """Apply librosa compatibility fixes to Wav2Lip"""
        audio_file = self.wav2lip_dir / "audio.py"
        
        if not audio_file.exists():
            print("Wav2Lip/audio.py not found")
            return False
        
        print("Applying librosa compatibility fixes...")
        
        try:
            with open(audio_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix librosa.filters.mel call
            old_pattern = "librosa.filters.mel(hp.sample_rate, hp.n_fft"
            new_pattern = "librosa.filters.mel(sr=hp.sample_rate, n_fft=hp.n_fft"
            
            if old_pattern in content:
                # Create backup
                backup_file = audio_file.with_suffix('.py.backup')
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Backup created: {backup_file}")
                
                # Apply fix
                fixed_content = content.replace(old_pattern, new_pattern)
                with open(audio_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                print("Librosa compatibility fix applied")
            else:
                print("Librosa fix already applied or different version")
            
            return True
            
        except Exception as e:
            print(f"Error applying fix: {e}")
            return False

    def download_wav2lip_checkpoint(self):
        """Download Wav2Lip checkpoint from Hugging Face"""
        checkpoint_dir = self.wav2lip_dir / "checkpoints"
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        if self.checkpoint_path.exists():
            size_mb = self.checkpoint_path.stat().st_size // (1024 * 1024)
            print(f"Checkpoint already exists ({size_mb}MB)")
            return True
        
        print("Downloading Wav2Lip checkpoint from Hugging Face...")
        checkpoint_url = "https://huggingface.co/Nekochu/Wav2Lip/resolve/fb925b05f0d353850ee0c56810e4545e274e2b5a/wav2lip_gan.pth"
        
        try:
            import requests
            response = requests.get(checkpoint_url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            print(f"Downloading {total_size // (1024*1024)}MB...")
            
            with open(self.checkpoint_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\rProgress: {percent:.1f}%", end='', flush=True)
            
            print(f"\nCheckpoint downloaded successfully!")
            size_mb = self.checkpoint_path.stat().st_size // (1024 * 1024)
            print(f"File size: {size_mb}MB")
            return True
            
        except Exception as e:
            print(f"\nFailed to download checkpoint: {e}")
            print("\nManual download fallback:")
            print(f"Please download manually from:")
            print(f"{checkpoint_url}")
            print(f"Save as: {self.checkpoint_path}")
            return False



    def download_vosk_model(self):
        """Download Vosk model"""
        models_dir = self.project_root / "backend" / "extras" / "models"
        model_dir = models_dir / "vosk-model-small-pt-0.3"
        
        if model_dir.exists():
            print("Vosk model already downloaded")
            return True
        
        print("Downloading Vosk model...")
        models_dir.mkdir(parents=True, exist_ok=True)
        
        # Try to download
        download_url = "https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip"
        zip_file = models_dir / "vosk-model-small-pt-0.3.zip"
        
        success = self.run_command(f"curl -L -o {zip_file} {download_url}", "Downloading Vosk model")
        
        if success and zip_file.exists():
            # Extract
            extract_success = self.run_command(f"cd {models_dir} && unzip -q {zip_file}", "Extracting model")
            if extract_success:
                zip_file.unlink()  # Remove zip file
                print("Vosk model downloaded and extracted")
                return True
        
        print("Failed to download Vosk model")
        print("Please download manually:")
        print(f"1. Download: {download_url}")
        print(f"2. Extract to: {models_dir}")
        return False

    def download_piper_voices(self):
        """Download Piper voice models"""
        voices_dir = self.project_root / "backend" / "extras" / "voices"
        voices_dir.mkdir(parents=True, exist_ok=True)
        
        # Tuga voice (official Rhasspy model)
        tuga_onnx = voices_dir / "pt_PT-tugao-medium.onnx"
        tuga_json = voices_dir / "pt_PT-tugao-medium.onnx.json"

        # Dii voice (OpenVoiceOS model)
        dii_onnx = voices_dir / "dii_pt-PT.onnx"
        dii_json = voices_dir / "dii_pt-PT.onnx.json"

        # If all four files exist, nothing to do
        if all(p.exists() for p in [tuga_onnx, tuga_json, dii_onnx, dii_json]):
            print("Piper voice models already downloaded (Tuga + Dii)")
            return True

        print("Downloading Piper voice models (Tuga + Dii)...")

        # Download URLs
        tuga_onnx_url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_PT/tug%C3%A3o/medium/pt_PT-tug%C3%A3o-medium.onnx"
        tuga_json_url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_PT/tug%C3%A3o/medium/pt_PT-tug%C3%A3o-medium.onnx.json"
        dii_onnx_url = "https://huggingface.co/OpenVoiceOS/phoonnx_pt-PT_dii_tugaphone/resolve/main/dii_pt-PT.onnx?download=true"

        success = True

        # Download Tuga ONNX
        if not tuga_onnx.exists():
            print("Downloading Tuga ONNX model...")
            tuga_onnx_success = self.run_command(f"curl -L -o {tuga_onnx} '{tuga_onnx_url}'", "Downloading Tuga ONNX model")
            if not tuga_onnx_success:
                success = False

        # Download Tuga JSON config
        if not tuga_json.exists():
            print("Downloading Tuga JSON config...")
            tuga_json_success = self.run_command(f"curl -L -o {tuga_json} '{tuga_json_url}'", "Downloading Tuga JSON config")
            if not tuga_json_success:
                success = False

        # Download Dii ONNX
        if not dii_onnx.exists():
            print("Downloading Dii ONNX model...")
            dii_onnx_success = self.run_command(f"curl -L -o {dii_onnx} '{dii_onnx_url}'", "Downloading Dii ONNX model")
            if not dii_onnx_success:
                success = False

        # Duplicate Tuga JSON for Dii voice config, as requested
        if tuga_json.exists() and not dii_json.exists():
            try:
                dii_json.write_bytes(tuga_json.read_bytes())
                print(f"Copied {tuga_json.name} to {dii_json.name}")
            except Exception as e:
                print(f"Warning: could not copy {tuga_json.name} to {dii_json.name}: {e}")
                success = False

        if success and all(p.exists() for p in [tuga_onnx, tuga_json, dii_onnx, dii_json]):
            print("Piper voice models downloaded successfully (Tuga + Dii)")
            return True
        else:
            print("Failed to download Piper voice models")
            print("Please download manually:")
            print(f"1. Tuga ONNX: {tuga_onnx_url}")
            print(f"2. Tuga JSON: {tuga_json_url}")
            print(f"3. Dii ONNX: {dii_onnx_url}")
            print(f"4. Save to: {voices_dir}")
            return False

    def verify_setup(self):
        """Verify the complete setup"""
        self.print_header("Verifying Setup")
        
        checks = [
            ("Python dependencies", self.project_root / "requirements.txt"),
            ("Wav2Lip repository", self.wav2lip_dir),
            ("Vosk model", self.project_root / "backend" / "extras" / "models" / "vosk-model-small-pt-0.3"),
            ("TTS voice models", self.project_root / "backend" / "extras" / "voices"),
            ("Avatar image", self.project_root / "backend" / "extras" / "photos" / "face.jpg"),
        ]
        
        all_good = True
        for name, path in checks:
            if path.exists():
                print(f"✅ {name}")
            else:
                print(f"❌ {name} - Missing: {path}")
                all_good = False
        
        # Check checkpoint separately
        if self.checkpoint_path.exists():
            size_mb = self.checkpoint_path.stat().st_size // (1024 * 1024)
            print(f"✅ Wav2Lip checkpoint ({size_mb}MB)")
        else:
            print(f"❌ Wav2Lip checkpoint - Optional: {self.checkpoint_path}")
            print("   (Basic video generation will work without this)")
        
        return all_good

    def run_complete_setup(self):
        """Run the complete setup process"""
        print("TTS + WAV2LIP COMPLETE SETUP")
        print("=" * 50)
        
        # Check Python version
        if not self.check_python_version():
            return False
        
        # Install requirements
        self.print_header("Step 1: Requirements")
        if not self.install_requirements():
            print("Failed to install requirements")
            return False
        
        # Setup Wav2Lip
        self.print_header("Step 2: Wav2Lip Setup")
        if not self.clone_wav2lip():
            print("Failed to clone Wav2Lip")
            return False
        
        if not self.fix_wav2lip_compatibility():
            print("Failed to apply compatibility fixes")
            return False
        
        # Download checkpoint
        checkpoint_ready = self.download_wav2lip_checkpoint()
        
        # Download models
        self.print_header("Step 3: Language Models")
        self.download_vosk_model()
        self.download_piper_voices()
        
        # Verify setup
        setup_complete = self.verify_setup()
        
        # Final status
        self.print_header("Setup Complete!")
        
        if setup_complete and checkpoint_ready:
            print("Full setup complete - Advanced lip sync available!")
        elif setup_complete:
            print("Basic setup complete - Download checkpoint for advanced lip sync")
        else:
            print("Partial setup - Check missing components above")
        
        print("\nYou can now run: python main.py")
        print("Check README.md for usage instructions")
        
        return True

def main():
    """Main setup function"""
    setup = TTSSetup()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--requirements-only":
            setup.print_header("Installing Requirements Only")
            setup.install_requirements()
        elif sys.argv[1] == "--wav2lip-only":
            setup.print_header("Wav2Lip Setup Only")
            setup.clone_wav2lip()
            setup.fix_wav2lip_compatibility()
            setup.download_wav2lip_checkpoint()
        elif sys.argv[1] == "--verify":
            setup.verify_setup()
        else:
            print("Usage: python setup.py [--requirements-only|--wav2lip-only|--verify]")
    else:
        setup.run_complete_setup()

if __name__ == "__main__":
    main()