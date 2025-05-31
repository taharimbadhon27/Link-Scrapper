import re
import os
from weasyprint import HTML
from urllib.parse import urlparse

def list_txt_files(directory):
    """List all .txt files in the given directory"""
    return [f for f in os.listdir(directory) if f.endswith('.txt')]

def select_input_file(directory):
    """Prompt user to select a text file from the directory"""
    txt_files = list_txt_files(directory)
    
    if not txt_files:
        print("No .txt files found in the directory.")
        return None
    
    print("\nAvailable text files:")
    for i, filename in enumerate(txt_files, 1):
        print(f"{i}. {filename}")
    
    while True:
        try:
            choice = int(input("\nEnter the number of the file to process: "))
            if 1 <= choice <= len(txt_files):
                return os.path.join(directory, txt_files[choice-1])
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def categorize_link(link):
    """Categorize links into YouTube, Drive, or Others"""
    netloc = urlparse(link).netloc.lower()
    
    if 'youtube.com' in netloc or 'youtu.be' in netloc:
        return 'YouTube'
    elif 'drive.google.com' in netloc:
        return 'Google Drive'
    else:
        return 'Others'

def create_html_content(links_dict):
    """Generate HTML content from categorized links"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }
            h1 { color: #ff0000; border-bottom: 1px solid #ccc; padding-bottom: 10px; }
            h2 { color: #333; margin-top: 20px; }
            a { text-decoration: none; color: #0066cc; }
            a:hover { text-decoration: underline; }
            .link-list { margin-left: 20px; }
            p { margin: 8px 0; }
        </style>
    </head>
    <body>
        <h1>Links Collection</h1>
    """
    
    for category, links in links_dict.items():
        html_content += f'<h2>{category}</h2>\n<div class="link-list">\n'
        
        for i, (title, url) in enumerate(links, 1):
            html_content += f'<p>{i}. <a href="{url}">{title}</a></p>\n'
        
        html_content += '</div>\n'
    
    html_content += '</body>\n</html>'
    return html_content

def process_links_file(input_file):
    """Process input text file and create categorized links"""
    links_dict = {
        'YouTube': [],
        'Google Drive': [],
        'Others': []
    }
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
                
            url_match = re.search(r'(https?://\S+)', line)
            if not url_match:
                continue
                
            url = url_match.group(1)
            category = categorize_link(url)
            
            if category == 'YouTube':
                title = f"Video No {line_num}"
            elif category == 'Google Drive':
                title = f"Drive No {line_num}"
            else:
                title = f"Link No {line_num}"
            
            links_dict[category].append((title, url))
    
    return links_dict

def create_pdf_from_links(input_file, output_dir):
    """Main function to create PDF from links"""
    links_dict = process_links_file(input_file)
    html_content = create_html_content(links_dict)
    
    input_basename = os.path.basename(input_file)
    output_filename = os.path.splitext(input_basename)[0] + "_links.pdf"
    output_path = os.path.join(output_dir, output_filename)
    
    HTML(string=html_content).write_pdf(output_path)
    print(f"\nSuccessfully created clickable PDF: {output_path}")

def main():
    """Main program flow"""
    target_dir = "/storage/emulated/0/YouTube/Telegram/"
    
    print(f"Looking for text files in: {target_dir}")
    
    input_file = select_input_file(target_dir)
    if not input_file:
        return
    
    create_pdf_from_links(input_file, target_dir)

if __name__ == "__main__":
    main()