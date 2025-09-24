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
        self.project_root = Path(__file__).parent.parent
        self.wav2lip_dir = self.project_root / "Wav2Lip"
        self.checkpoint_path = self.wav2lip_dir / "checkpoints" / "wav2lip_gan.pth"
        
    def print_header(self, title):
        """Print formatted section header"""
        print(f"\n{'='*50}")
        print(f"🚀 {title}")
        print(f"{'='*50}")
    
    def run_command(self, cmd, description=None):
        """Run shell command with error handling"""
        if description:
            print(f"🔄 {description}...")
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=self.project_root)
            if result.returncode != 0:
                print(f"❌ Command failed: {cmd}")
                if result.stderr:
                    print(f"Error: {result.stderr}")
                return False
            if result.stdout:
                print(result.stdout.strip())
            return True
        except Exception as e:
            print(f"❌ Error running command: {e}")
            return False

    def check_python_version(self):
        """Check if Python version is compatible"""
        version = sys.version_info
        print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
        
        if version.major != 3 or version.minor < 8:
            print("❌ Python 3.8+ required")
            return False
        
        if version.minor > 10:
            print("⚠️  Python 3.11+ may have compatibility issues with some dependencies")
        
        print("✅ Python version compatible")
        return True

    def install_requirements(self):
        """Install project requirements"""
        self.print_header("Installing Requirements")
        
        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            print("❌ requirements.txt not found")
            return False
        
        print("📦 Installing Python dependencies...")
        success = self.run_command("pip install -r requirements.txt", "Installing requirements")
        
        if success:
            print("✅ Requirements installed successfully")
        return success

    def clone_wav2lip(self):
        """Clone Wav2Lip repository if not exists"""
        if self.wav2lip_dir.exists():
            print("ℹ️  Wav2Lip directory already exists")
            return True
        
        print("📥 Cloning Wav2Lip repository...")
        success = self.run_command("git clone https://github.com/Rudrabha/Wav2Lip.git")
        
        if success:
            print("✅ Wav2Lip cloned successfully")
        return success

    def fix_wav2lip_compatibility(self):
        """Apply librosa compatibility fixes to Wav2Lip"""
        audio_file = self.wav2lip_dir / "audio.py"
        
        if not audio_file.exists():
            print("❌ Wav2Lip/audio.py not found")
            return False
        
        print("🔧 Applying librosa compatibility fixes...")
        
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
                print(f"📋 Backup created: {backup_file}")
                
                # Apply fix
                fixed_content = content.replace(old_pattern, new_pattern)
                with open(audio_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                print("✅ Librosa compatibility fix applied")
            else:
                print("ℹ️  Librosa fix already applied or different version")
            
            return True
            
        except Exception as e:
            print(f"❌ Error applying fix: {e}")
            return False

    def setup_checkpoint_directory(self):
        """Setup checkpoint directory"""
        checkpoint_dir = self.wav2lip_dir / "checkpoints"
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        if self.checkpoint_path.exists():
            size_mb = self.checkpoint_path.stat().st_size // (1024 * 1024)
            print(f"✅ Checkpoint already exists ({size_mb}MB)")
            return True
        
        print("\n📋 CHECKPOINT DOWNLOAD REQUIRED:")
        print("-" * 40)
        print("The Wav2Lip model checkpoint is required for advanced lip sync.")
        print(f"Please download 'wav2lip_gan.pth' (~400MB) and place it at:")
        print(f"📁 {self.checkpoint_path}")
        print("\n🔍 Download sources:")
        print("• GitHub: search 'wav2lip_gan.pth'")
        print("• Hugging Face: model repositories")
        print("• Your project releases (recommended)")
        print("\n⚠️  Without this file, only basic video generation will work.")
        
        return False

    def install_additional_deps(self):
        """Install additional Wav2Lip dependencies"""
        print("📦 Installing additional Wav2Lip dependencies...")
        
        additional_deps = ["face-recognition", "dlib"]
        
        for dep in additional_deps:
            print(f"Installing {dep}...")
            success = self.run_command(f"pip install {dep}")
            if not success:
                print(f"⚠️  Failed to install {dep} (may not be critical)")
        
        return True

    def download_vosk_model(self):
        """Download Vosk Portuguese model"""
        models_dir = self.project_root / "models"
        model_dir = models_dir / "vosk-model-small-pt-0.3"
        
        if model_dir.exists():
            print("✅ Vosk model already downloaded")
            return True
        
        print("📥 Downloading Vosk Portuguese model...")
        models_dir.mkdir(exist_ok=True)
        
        # Try to download
        download_url = "https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip"
        zip_file = models_dir / "vosk-model-small-pt-0.3.zip"
        
        success = self.run_command(f"curl -L -o {zip_file} {download_url}", "Downloading Vosk model")
        
        if success and zip_file.exists():
            # Extract
            extract_success = self.run_command(f"cd {models_dir} && unzip -q {zip_file}", "Extracting model")
            if extract_success:
                zip_file.unlink()  # Remove zip file
                print("✅ Vosk model downloaded and extracted")
                return True
        
        print("❌ Failed to download Vosk model")
        print("Please download manually:")
        print(f"1. Download: {download_url}")
        print(f"2. Extract to: {models_dir}")
        return False

    def verify_setup(self):
        """Verify the complete setup"""
        self.print_header("Verifying Setup")
        
        checks = [
            ("Python dependencies", self.project_root / "requirements.txt"),
            ("Wav2Lip repository", self.wav2lip_dir),
            ("Vosk model", self.project_root / "models" / "vosk-model-small-pt-0.3"),
            ("TTS voice model", self.project_root / "media" / "voices"),
            ("Avatar image", self.project_root / "media" / "photos" / "face.jpg"),
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
            print(f"⚠️  Wav2Lip checkpoint - Optional: {self.checkpoint_path}")
            print("   (Basic video generation will work without this)")
        
        return all_good

    def run_complete_setup(self):
        """Run the complete setup process"""
        print("🎭 TTS + WAV2LIP COMPLETE SETUP")
        print("=" * 50)
        
        # Check Python version
        if not self.check_python_version():
            return False
        
        # Install requirements
        self.print_header("Step 1: Requirements")
        if not self.install_requirements():
            print("❌ Failed to install requirements")
            return False
        
        # Setup Wav2Lip
        self.print_header("Step 2: Wav2Lip Setup")
        if not self.clone_wav2lip():
            print("❌ Failed to clone Wav2Lip")
            return False
        
        if not self.fix_wav2lip_compatibility():
            print("❌ Failed to apply compatibility fixes")
            return False
        
        # Setup checkpoint directory
        checkpoint_ready = self.setup_checkpoint_directory()
        
        # Install additional dependencies
        self.install_additional_deps()
        
        # Download Vosk model
        self.print_header("Step 3: Language Models")
        self.download_vosk_model()
        
        # Verify setup
        setup_complete = self.verify_setup()
        
        # Final status
        self.print_header("Setup Complete!")
        
        if setup_complete and checkpoint_ready:
            print("🎉 Full setup complete - Advanced lip sync available!")
        elif setup_complete:
            print("✅ Basic setup complete - Download checkpoint for advanced lip sync")
        else:
            print("⚠️  Partial setup - Check missing components above")
        
        print("\n🚀 You can now run: python main.py")
        print("📚 Check README.md for usage instructions")
        
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
            setup.setup_checkpoint_directory()
        elif sys.argv[1] == "--verify":
            setup.verify_setup()
        else:
            print("Usage: python setup.py [--requirements-only|--wav2lip-only|--verify]")
    else:
        setup.run_complete_setup()

if __name__ == "__main__":
    main()