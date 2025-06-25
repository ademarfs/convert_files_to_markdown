"""Module providing a function printing python version."""
import os
from extraction_functions import process_documents_batch, check_environment, merge_markdown_files


def main():
    """Function printing python version."""
    print("🚀 DOCLING BATCH PROCESSOR")
    print("=" * 50)

    if not check_environment():
        return
    print()

    # Define input and output folders
    input_folder = r"C:\\Users\\adema\\OneDrive\\Desktop\\input"
    output_folder = r"C:\\Users\\adema\\OneDrive\\Desktop\\Pasta\\convert_files_to_markdown\\output"

    if not os.path.exists(input_folder):
        print(f"❌ ERROR: Input folder does not exist: {input_folder}")
        return

    print(f"📂 Input folder: {input_folder}")
    print(f"📁 Output folder: {output_folder}")
    print()

    try:
        process_documents_batch(input_folder, output_folder)
        print("\n🎉 Processing completed!")
    except KeyboardInterrupt:
        print("\n⏹️  Processing interrupted by user")
    except ImportError as e:
        print(f"\n❌ Unhandled error: {e}")

    merge_markdown_files(output_folder)


if __name__ == "__main__":
    main()
