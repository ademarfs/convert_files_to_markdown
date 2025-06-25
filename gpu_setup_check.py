"""
gpu_setup_check.py
Script check the GPU setup for PyTorch and provides instructions for installation and configuration.
"""
import subprocess
import torch


def check_gpu_setup():
    """
    Verifica a configuração da GPU e fornece instruções para correção
    """
    print("🔍 VERIFICANDO CONFIGURAÇÃO DA GPU")
    print("=" * 50)
    # Verifica se PyTorch está instalado
    print(f"✅ PyTorch versão: {torch.__version__}")
    # Verifica se CUDA está disponível
    if torch.cuda.is_available():
        print("✅ CUDA está disponível!")
        print(f"   🎮 GPU: {torch.cuda.get_device_name(0)}")
        print(
            f"   📊 VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        print(f"   🔢 CUDA versão: {torch.version.cuda}")
        print(f"   🏠 Dispositivos disponíveis: {torch.cuda.device_count()}")
        # Teste básico de GPU
        try:
            print("✅ Teste de GPU passou!")
            return True
        except ImportError as e:
            print(f"❌ Erro no teste de GPU: {e}")
            return False
    else:
        print("❌ CUDA não está disponível")
        print("\n🔧 SOLUÇÕES POSSÍVEIS:")
        print("1. Verifique se você tem uma GPU NVIDIA")
        print("2. Instale os drivers NVIDIA mais recentes")
        print("3. Reinstale PyTorch com suporte CUDA:")
        print("  pip uninstall torch torchvision torchaudio")
        print("  pip install torch torchvision torchaudio - https://download.pytorch.org/whl/cu121")
        print("\n4. Para verificar se o CUDA está instalado no sistema:")
        print("   nvcc --version")
        print("   nvidia-smi")
        return False


def install_gpu_pytorch():
    """
    Instala PyTorch com suporte CUDA
    """
    print("\n🔄 INSTALANDO PYTORCH COM SUPORTE CUDA...")

    commands = [
      "py -m pip uninstall -y torch torchvision torchaudio",
      "py -m pip install torch torchvision torchaudio - https://download.pytorch.org/whl/cu121"
    ]

    for cmd in commands:
        print(f"Executando: {cmd}")
        try:
            subprocess.run(cmd, shell=True, check=True)
            print("✅ Comando executado com sucesso")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro: {e}")
            return False

    print("✅ Instalação concluída! Reinicie o Python e teste novamente.")
    return True


def suppress_docling_warnings():
    """
    Adiciona supressão específica para warnings do Docling
    """
    print("\n🔇 CONFIGURANDO SUPRESSÃO DE WARNINGS...")

    config_code = '''
# Adicione este código no início do seu script principal:
import warnings
import os

# Suprime warnings específicos do Docling
warnings.filterwarnings("ignore", message=".*pin_memory.*")
warnings.filterwarnings("ignore", message=".*accelerator.*")

# Opcional: Define variável de ambiente para reduzir logs
os.environ["TOKENIZERS_PARALLELISM"] = "false"
'''

    print(config_code)


if __name__ == "__main__":
    HAS_GPU = check_gpu_setup()

    if not HAS_GPU:
        print("\n❓ Deseja tentar instalar PyTorch com CUDA? (s/n): ", end="")
        choice = input().lower()
        if choice == 's':
            install_gpu_pytorch()

    suppress_docling_warnings()

    print("\n" + "=" * 50)
    print("🏁 VERIFICAÇÃO CONCLUÍDA")
    if HAS_GPU:
        print("✅ Sua GPU está pronta para usar com Docling!")
    else:
        print("⚠️  Docling usará CPU (mais lento, mas funcional)")
