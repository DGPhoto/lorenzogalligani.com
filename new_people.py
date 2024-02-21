from PIL import Image
import os
import re
import sys

def rename_and_resize_images(directory):
    # Define the regex pattern
    pattern = re.compile(r'^.*\.(jpg|jpeg|png|gif|bmp|tiff)$', flags=re.IGNORECASE)

    # Counter for the sequence
    sequence_number = 1

    # Get the folder name from the last part of the directory path
    folder_name = os.path.basename(os.path.normpath(directory))

    # Iterate through files in the directory
    for filename in os.listdir(directory):
        # Check if the filename matches the pattern
        match = pattern.match(filename)

        if match:
            # Get file extension
            ext = match.group(1).lower()

            # Create the new filename with the sequence number and underscore
            new_filename = f'{folder_name}_{sequence_number}.{ext}'
            sequence_number += 1

            # Build the full paths
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)

            # Rename the file
            os.rename(old_path, new_path)

            # Resize the image
            resize_image(new_path)




def resize_image(image_path):
    # Open the image
    with Image.open(image_path) as img:
        # Calculate the new width to maintain the aspect ratio
        target_width = 1000
        aspect_ratio = img.width / img.height
        target_height = int(target_width / aspect_ratio)

        # Resize the image
        resized_img = img.resize((target_width, target_height), resample=Image.LANCZOS)

        # Save the resized image, overwriting the original
        resized_img.save(image_path)

def create_html(directory):
    # Get the folder name from the last part of the directory path
    folder_name = os.path.basename(os.path.normpath(directory))

    # Read header content
    with open('header.txt', 'r') as header_file:
        header_content = header_file.read()

    # Read footer content
    with open('footer.txt', 'r') as footer_file:
        footer_content = footer_file.read()

    # Create the output HTML file
    output_file_path = os.path.join(directory, f'{folder_name}.html')

    # Write the header content to the HTML file
    with open(output_file_path, 'w') as html_file:
        html_file.write(header_content)

    # Iterate through image files in the folder
    for i, filename in enumerate(sorted(os.listdir(directory))):
        # Check if the file is an image
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
            # Generate the div element for each image
            div_content = f'<div class="grid-item item animate-box" data-animate-effect="fadeIn">\n\t<a href="images/{folder_name}/{filename}" class="image-popup">\n\t\t<div class="img-wrap">\n\t\t\t<img src="images/{folder_name}/{filename}" alt="" class="img-responsive">\n\t\t</div>\n\t\t<div class="text-wrap">\n\t\t\t<div class="text-inner popup">\n\t\t\t</div>\n\t\t</div>\n\t</a>\n</div>\n'

            # Append the div content to the HTML file
            with open(output_file_path, 'a') as html_file:
                html_file.write(div_content)

    # Append the footer content to the HTML file
    with open(output_file_path, 'a') as html_file:
        html_file.write(footer_content)

    # Insert the new div section into the main index.html file
    insert_into_main_html(output_file_path)


def insert_into_main_html(new_html_path):
    # Replace with the actual path to your main index.html file
    main_html_path = "./index.html"

    # Read the content of the main index.html file
    with open(main_html_path, 'r') as main_html_file:
        html_content = main_html_file.read()

        # Add a new div section to the end of the HTML content
        new_div_content = f'''
          <div class="grid-item item animate-box" data-animate-effect="fadeIn">
            <a href="{os.path.basename(new_html_path).replace(".html", "")}">
              <div class="img-wrap">
                <img src="images/{os.path.basename(new_html_path).replace(".html", "")}/{os.path.basename(new_html_path).replace(".html", "")}_1.jpg" alt="" class="img-responsive">
              </div>
              <div class="text-wrap">
                <div class="text-inner">
                  <div>
                    <h2>{os.path.basename(new_html_path).replace(".html", "").capitalize()}</h2>
                    <span>{len(os.listdir(os.path.dirname(new_html_path)))} photos</span>
                  </div>
                </div>
              </div>
            </a>
          </div>
        '''

# Find the index of the closing tag of the last existing grid item
        closing_tag_index = html_content.rfind('</div>')

# Insert the new div section after the last existing grid item
        html_content = html_content[:closing_tag_index] + new_div_content + html_content[closing_tag_index:]




        # Save the updated HTML content to the main index.html file
        with open(main_html_path, 'w') as main_html_file:
            main_html_file.write(html_content)




if __name__ == "__main__":
    # Check if the image directory is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script_name.py /path/to/your/images/folder")
        sys.exit(1)

    # Get the image directory from the command-line argument
    image_directory = sys.argv[1]

    # Rename and resize images
    rename_and_resize_images(image_directory)

    # Create the HTML file and update the main index.html
    create_html(image_directory)
