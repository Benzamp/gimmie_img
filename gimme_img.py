import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin, urlparse
from tkinter import Tk
from tkinter.filedialog import askdirectory

CONFIG_FILE = "config.txt"

def display_logo():
    logo = """

       _                            _                 
      (_)                          (_)                
  __ _ _ _ __ ___  _ __ ___   ___   _ _ __ ___   __ _ 
 / _` | | '_ ` _ \| '_ ` _ \ / _ \ | | '_ ` _ \ / _` |
| (_| | | | | | | | | | | | |  __/ | | | | | | | (_| |
 \__, |_|_| |_| |_|_| |_| |_|\___| |_|_| |_| |_|\__, |
  __/ |                        ______            __/ |
 |___/                        |______|          |___/ 

            v0.1 by Ben Harrison
    """
    print(logo)

def create_directory_structure(base_path):
    date_str = datetime.now().strftime('%Y-%m-%d')
    scraper_folder = os.path.join(base_path, f'Scraper {date_str}')
    images_folder = os.path.join(scraper_folder, 'images')
    
    os.makedirs(images_folder, exist_ok=True)
    
    return images_folder

def download_images(url, images_folder):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    image_tags = soup.find_all('img')
    
    for img in image_tags:
        img_url = img.get('src')
        if not img_url:
            continue
        
        img_url = urljoin(url, img_url)
        img_name = os.path.basename(urlparse(img_url).path)
        
        img_data = requests.get(img_url).content
        with open(os.path.join(images_folder, img_name), 'wb') as handler:
            handler.write(img_data)
        print(f'Downloaded {img_name} to {images_folder}')

def load_download_path():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            path = file.read().strip()
            if os.path.isdir(path):
                return path
    return None

def save_download_path(path):
    with open(CONFIG_FILE, 'w') as file:
        file.write(path)

def select_download_location():
    input("Use the file explorer to select the download location. Press any key to continue...")
    root = Tk()
    root.withdraw()  # Hide the root window
    download_path = askdirectory()
    if download_path:
        save_download_path(download_path)
        print(f"Download location set to: {download_path}")
    else:
        print("No location selected.")
    root.destroy()

def main():
    display_logo()
    download_path = load_download_path()
    
    while True:
        print("\nMenu:")
        print("1. Scrape a webpage for images")
        print("2. Select download location")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            if download_path:
                while True:
                    url = input("Enter the URL of the webpage to scrape (or press enter to go back): ")
                    if url == "":
                        break
                    images_folder = create_directory_structure(download_path)
                    download_images(url, images_folder)
                    print('Scraping completed!')
            else:
                print("Download location not set. Please select a download location first.")
        elif choice == '2':
            select_download_location()
            download_path = load_download_path()
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
