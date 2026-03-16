# RetroArch Scraper (MiyooCFW)

YET another fork of https://github.com/mattsteen14/rascraper tailored to work with MiyooCFW out of the gate.

## About The Project

This is a Python GUI application (run from the terminal) that automatically downloads box art and preview images for your video game ROMs from the [libretro-thumbnails GitHub repository](https://github.com/libretro-thumbnails/libretro-thumbnails).

The app matches your ROM filenames exactly — including metadata like years and publishers — and fetches the corresponding images from a pinned commit on GitHub. It automatically resizes box art images to a width of 128 pixels to fit MIYOO GMenu2X's preview standard, populating the `box` OR `preview` subdirectories within the MIYOO `/roms` directory structure.

This tool is intended as an alternative to using built-in scraper in MiyooCFW, for faster & local images scraping.

### Features

- Automatic scraping of box and preview images
- Matches ROM filenames to libretro-thumbnails project
- Supports MiyooCFW directory structure and image resizing
- Works offline once downloaded
- Two flexible output options


## Getting Started

These instructions will help you set up the project locally.

### Prerequisites

- An internet connection (to download artwork from GitHub)
- ROMs organized in subdirectories (with filenames that match libretro-thumbnails)
- Knowledge of your system’s MIYOO name and libretro-thumbnails directory name

Make sure Python and Pillow are installed:

```bash
python3 --version
pip install pillow
```

---

### Installation

 - Install dependencies:

```bash
pip install -r requirements.txt
```

- Run the app:

```bash
python3 rascraper.py
```

 - Select your **ROMs directory** using the first Browse button.

 - Select the **MIYOO root directory** using the second Browse button (this is the MIYOO directory on your SD card or computer).

 - Select the **system** from the drop-down menu. This will map to the correct libretro-thumbnails directory and MIYOO `/roms/{system}` directory.

 - Choose your **output location** using the radio buttons:
   - **MIYOO structure**: Saves artwork directly to `MIYOO/{system}/.images` directory (recommended to insert SD card and specify /roms partition).
   - **ROMs directory**: Creates an `.images` directory with `Boxarts` OR `Screenshots` arts in the ROMs/{systen} directory 
  
    NOTE: If you want to copy ROMs and scraped images simultaneously from one place to your device, save artwork "Within root ROMS folder" & you can leave blank "MIYOO Root folder".

 - Click **RUN SCRAPER**.

 - Check the subdirectories — artwork should be downloaded and placed correctly.