from PIL import Image
import os
from pathlib import Path

def downsize_images(folder_path, max_size=(1000, 800), quality=85):
    """
    Downsize all images in the specified folder that are larger than max_size.
    
    Args:
        folder_path (str): Path to the folder containing images
        max_size (tuple): Maximum width and height for the resized images
        quality (int): JPEG quality (1-100)
    """
    # Supported image formats
    supported_formats = {'.jpg', '.jpeg', '.png', '.bmp'}
    
    # Convert folder path to Path object
    folder = Path(folder_path)
    
    # Ensure the folder exists
    if not folder.exists():
        raise ValueError(f"Folder not found: {folder_path}")
    
    # Process all files in the folder
    for file_path in folder.iterdir():
        # Check if file is an image
        if file_path.suffix.lower() not in supported_formats:
            continue
            
        try:
            with Image.open(file_path) as img:
                # Get original format
                img_format = img.format
                
                # Check if image needs resizing
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    # Calculate new size while maintaining aspect ratio
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                    # Create temporary filename
                    temp_path = file_path.with_name(f"temp_{file_path.name}")
                    
                    # Save with original format
                    if img_format == 'JPEG':
                        img.save(temp_path, format=img_format, quality=quality, optimize=True)
                    else:
                        img.save(temp_path, format=img_format, optimize=True)
                    
                    # Replace original with resized version
                    os.replace(temp_path, file_path)
                    print(f"Resized: {file_path.name}")
                else:
                    print(f"Skipped (already within size limits): {file_path.name}")
                    
        except Exception as e:
            print(f"Error processing {file_path.name}: {str(e)}")

if __name__ == "__main__":
    # Example usage
    folder_to_process = "C:/github/loveshijian.github.io/_assets/images/shijian/shijian03"
    downsize_images(folder_to_process)