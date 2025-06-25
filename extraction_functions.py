# extraction_functions.py
"""Module providing functions for processing documents with Docling.
This module includes functions to set up the document converter, split large PDFs,"""
import gc
import time
import warnings
from pathlib import Path
import torch
from tqdm import tqdm
from PyPDF2 import PdfReader, PdfWriter
from docling.document_converter import DocumentConverter
import docling


def setup_converter_with_gpu():
    """Sets up the Docling converter with GPU support, if available."""
    print("🔧 Setting up converter...")
    if torch.cuda.is_available():
        device = "cuda"
        print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
        print(f"📊 VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    else:
        device = "cpu"
        print("⚠️  GPU not detected, using CPU")
        warnings.filterwarnings("ignore", message=".*pin_memory.*")

    try:
        print("🔄 Trying basic configuration...")
        converter = DocumentConverter()
        print("✅ Basic converter successfully configured")
    except Exception as e1:
        print(f"⚠️  Error in basic setup: {e1}")

    return converter, device


def split_pdf(file_path, output_dir, pages_per_chunk=10):
    """Splits a large PDF into several smaller files with a specific number of pages."""
    reader = PdfReader(str(file_path))
    total_pages = len(reader.pages)
    chunk_paths = []

    for i in range(0, total_pages, pages_per_chunk):
        writer = PdfWriter()

        for j in range(i, min(i + pages_per_chunk, total_pages)):
            writer.add_page(reader.pages[j])
        chunk_filename = f"{file_path.stem}_chunk_{i // pages_per_chunk + 1}.pdf"
        chunk_path = output_dir / chunk_filename

        with open(chunk_path, "wb") as f:
            writer.write(f)
        chunk_paths.append(chunk_path)

    return chunk_paths


def process_single_document(converter, file_path, output_path):
    """Processes a single document and converts it to Markdown."""
    try:
        print(f"   🔄 Converting: {file_path.name}")
        result = converter.convert(str(file_path))
        document = result.document
        base_name = file_path.stem

        try:
            markdown_output = document.export_to_markdown()
            md_output_path = output_path / f"{base_name}.md"
            with open(md_output_path, "w", encoding="utf-8") as md_file:
                md_file.write(markdown_output)
            print(f"   ✅ Markdown saved: {md_output_path.name}")
            return True, ""
        except Exception as e:
            print(f"   ⚠️  Error exporting Markdown: {e}")
            return False, str(e)

    except Exception as e:
        error_msg = str(e)
        if "'PdfPipelineOptions' object has no attribute 'backend'" in error_msg:
            error_msg = "API compatibility error - Docling may be outdated"
        elif "CUDA" in error_msg:
            error_msg = f"GPU-related error: {error_msg}"
        elif "memory" in error_msg.lower():
            error_msg = f"Memory error: {error_msg}"
        return False, error_msg


def process_documents_batch(input_folder, output_folder):
    """Process the documents in input_folder and save the results in Markdown in output_folder."""
    try:
        converter, device = setup_converter_with_gpu()
    except Exception as e:
        print(f"❌ Fatal error during converter setup: {e}")
        return

    supported_extensions = {'.pdf', '.docx', '.doc', '.pptx',
                            '.ppt', '.xlsx', '.xls', '.html', '.md', '.txt'}
    input_path = Path(input_folder)
    output_path = Path(output_folder)

    if not input_path.exists():
        print(f"❌ Input folder not found: {input_folder}")
        return

    output_path.mkdir(parents=True, exist_ok=True)
    files_to_process = [f for f in input_path.iterdir(
    ) if f.is_file() and f.suffix.lower() in supported_extensions]

    if not files_to_process:
        print(f"❌ No compatible files found in: {input_folder}")
        return

    print(f"📁 Found {len(files_to_process)} files to process")
    print(f"🖥️ Processing will be done on: {device.upper()}")
    print(f"📤 Output will be saved in: {output_folder}")
    print("-" * 50)
    successful_conversions = 0
    failed_conversions = 0
    errors_log = []

    with tqdm(total=len(files_to_process), desc="🔄 Processing documents", unit="file",
              bar_format="{desc}: {percentage:3.0f}%"
              "|{bar}"
              "| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
              "| {rate_fmt} | {postfix}",
              colour="green") as pbar:

        for file_path in files_to_process:
            pbar.set_description(f"🔄 Preparing: {file_path.name[:30]}...")

            if file_path.suffix.lower() == ".pdf" and file_path.stat().st_size > 50 * 1024 * 1024:
                tqdm.write(f"📄 Large document detected: {file_path.name}")

                try:
                    chunk_paths = split_pdf(
                        file_path, output_path, pages_per_chunk=10)
                    for chunk_path in chunk_paths:
                        success, error_msg = process_single_document(
                            converter, chunk_path, output_path)
                        if success:
                            successful_conversions += 1
                        else:
                            failed_conversions += 1
                            errors_log.append(
                                f"{chunk_path.name}: {error_msg}")
                            tqdm.write(
                                f"❌ ERROR: {chunk_path.name} - {error_msg}")
                        chunk_path.unlink()
                        gc.collect()
                        torch.cuda.empty_cache()
                        pbar.update(1)

                except Exception as e:
                    failed_conversions += 1
                    error_msg = f"Error splitting/processing: {e}"
                    errors_log.append(f"{file_path.name}: {error_msg}")
                    tqdm.write(f"❌ ERROR: {file_path.name} - {error_msg}")
                    pbar.update(1)
            else:
                success, error_msg = process_single_document(
                    converter, file_path, output_path)
                if success:
                    successful_conversions += 1
                    pbar.set_description(
                        f"✅ Done: {file_path.name[:30]}...")
                else:
                    failed_conversions += 1
                    pbar.set_description(f"❌ Error: {file_path.name[:30]}...")
                    errors_log.append(f"{file_path.name}: {error_msg}")
                    tqdm.write(f"❌ ERROR: {file_path.name} - {error_msg}")
                gc.collect()
                torch.cuda.empty_cache()
                pbar.update(1)
                time.sleep(0.1)

    print("-" * 50)
    print("📊 CONVERSION SUMMARY:")
    print(f"✅ Successes: {successful_conversions}")
    print(f"❌ Failures: {failed_conversions}")
    print(f"📁 Total processed: {len(files_to_process)}")
    print(
        f"📈 Success rate: {(successful_conversions/len(files_to_process)*100):.1f}%")

    if errors_log:
        error_log_path = output_path / "conversion_errors.log"
        with open(error_log_path, "w", encoding="utf-8") as log_file:
            log_file.write("ERROR LOG - DOCLING CONVERSION\n")
            log_file.write("=" * 40 + "\n")
            log_file.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            log_file.write(f"Total files: {len(files_to_process)}\n")
            log_file.write(f"Successes: {successful_conversions}\n")
            log_file.write(f"Failures: {failed_conversions}\n\n")
            for error in errors_log:
                log_file.write(f"{error}\n")
        print(f"📄 Error log saved at: {error_log_path}")


def check_environment():
    """Checks the runtime environment and Docling installation."""
    print("🔍 Checking environment...")
    try:
        version = getattr(docling, '__version__', 'Version not identified')
        print(f"📦 Docling version: {version}")
    except ImportError:
        print("❌ Docling is not installed!")
        return False
    try:
        print(f"🔥 PyTorch version: {torch.__version__}")
        if torch.cuda.is_available():
            print(f"🚀 CUDA available: {torch.version.cuda}")
        else:
            print("💻 Using CPU (CUDA not available)")
    except Exception:
        print("⚠️  PyTorch not detected")
    return True

def merge_markdown_files(output_folder, merged_filename="documento_final.md"):
    """
    Merges all Markdown files in the output folder into a single file.
    
    Args:
        output_folder (str): Path to the folder containing .md files
        merged_filename (str): Name of the final merged markdown file
    """
    output_path = Path(output_folder)
    markdown_files = sorted(output_path.glob("*.md"))

    if not markdown_files:
        print("❌ No Markdown files found to merge.")
        return

    merged_path = output_path / merged_filename
    print(f"🧩 Merging {len(markdown_files)} Markdown files...")

    with open(merged_path, "w", encoding="utf-8") as merged_file:
        for _, md_path in enumerate(markdown_files):
            with open(md_path, "r", encoding="utf-8") as infile:
                content = infile.read()
                merged_file.write(f"# Document: {md_path.stem}\n\n")
                merged_file.write(content)
                merged_file.write("\n\n---\n\n")  # optional separator

    print(f"✅ Merged file saved as: {merged_path.name}")
    
