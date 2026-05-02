import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
from urllib.parse import quote
from PIL import Image, UnidentifiedImageError
from io import BytesIO

# ---- SYSTEMS MAPPING ----
systems = {
    "ARCADE - FBNeo": {
        "libretro": "FBNeo_-_Arcade_Games",
        "miyoo": "FBA"
    },
    "ARCADE - MAME": {
        "libretro": "MAME",
        "miyoo": "MAME"
    },
    "ARCADE - SNK NeoGeo": {
        "libretro": "SNK_-_Neo_Geo",
        "miyoo": "NEOGEO"
    },
    "Amstrad CPC": {
        "libretro": "Amstrad_-_CPC",
        "miyoo": "CPC"
    },
    "Amstrad GX400": {
        "libretro": "Amstrad_-_GX4000",
        "miyoo": "CPC"
    },
    "Arduboy": {
        "libretro": "Arduboy_Inc_-_Arduboy",
        "miyoo": "ARDUBOY"
    },
    "Atari 2600": {
        "libretro": "Atari_-_2600",
        "miyoo": "2600" # Would rather use smth like ATARI_2600,  but this isn't inline with legacy docs
    },
    "Atari 5200": {
        "libretro": "Atari_-_5200",
        "miyoo": "5200"
    },
    "Atari 7800": {
        "libretro": "Atari_-_7800",
        "miyoo": "7800"
    },
    "Atari 8-bit": {
        "libretro": "Atari_-_8-bit_Family",
        "miyoo": "800" # The systemid in RA suggest atari_5200, but it's atari800 core so let's use that
    },
    # "Atari Jaguar": {
    #     "libretro": "Atari_-_Jaguar",
    #     "miyoo": "JAGUAR"
    # },
    "Atari Lynx": {
        "libretro": "Atari_-_Lynx",
        "miyoo": "LYNX"
    },
    "Atari ST": {
        "libretro": "Atari_-_ST",
        "miyoo": "ST"
    },
    # "Atomiswave": {
    #     "libretro": "Atomiswave",
    #     "miyoo": "ATOMISWAVE"
    # },
    "Bandai WonderSwan": {
        "libretro": "Bandai_-_WonderSwan",
        "miyoo": "WSWAN"
    },
    "Bandai WonderSwan Color": {
        "libretro": "Bandai_-_WonderSwan_Color",
        "miyoo": "WSWAN"
    },
    # "CHIP-8": {
    #     "libretro": "",
    #     "miyoo": "CHIP_8"
    # },
    # "Cannonball": {
    #     "libretro": "Cannonball",
    #     "miyoo": "CANNONBALL"
    # },
    "Casio Loopy": {
        "libretro": "Casio_-_Loopy",
        "miyoo": "MSX"
    },
    #Casio - PV-1000
    # "Cave Story": {
    #     "libretro": "Cave Story",
    #     "miyoo": "nxengine"
    # },
    "ChaiLove": {
        "libretro": "ChaiLove",
        "miyoo": "CHAILOVE"
    },
    "ColecoVision": {
        "libretro": "Coleco_-_ColecoVision",
        "miyoo": "COLECOVISION"
    },
    "Commodore 64": {
        "libretro": "Commodore_-_64",
        "miyoo": "C64"
    },
    "Commodore Amiga": {
        "libretro": "Commodore_-_Amiga",
        "miyoo": "AMIGA"
    },
    #Commodore - CD32
    #Commodore - CDTV
    #Commodore - PET
    #Commodore - Plus-4
    #Commodore - VIC-20
    "DOOM": {
        "libretro": "DOOM",
        "miyoo": "DOOM"
    },
    "DOS": {
        "libretro": "DOS",
        "miyoo": "DOS"
    },
    #Dinothawr
    #Emerson - Arcadia 2001
    #Entex - Adventure Vision
    #Epoch - Super Cassette Vision
    # "Elektronika BK": {
    #     "libretro": "",
    #     "miyoo": "BK"
    # },
    "Fairchild Channel F": {
        "libretro": "Fairchild_-_Channel_F",
        "miyoo": "CHANNELF"
    },
    "Flashback": {
        "libretro": "Flashback",
        "miyoo": "FLASHBACK"
    },
    #Funtech - Super Acan
    "GCE Vectrex": {
        "libretro": "GCE_-_Vectrex",
        "miyoo": "VECTREX"
    },
    #GamePark - GP32
    "Game and Watch": {
        "libretro": "Handheld_Electronic_Game",
        "miyoo": "G&W"
    },
    #Hartung - Game Master
    #LeapFrog - Leapster Learning Game System
    "Jump 'n Bump": {
        "libretro": "Jump_'n_Bump",
        "miyoo": "JUMPNBUMP"
    },
    "LowRes NX": {
        "libretro": "LowRes_NX",
        "miyoo": "LOWRESNX"
    },
    "Lutro": {
        "libretro": "Lutro",
        "miyoo": "LUTRO"
    },
    "Magnavox - Odyssey2": {
        "libretro": "Magnavox_-_Odyssey2",
        "miyoo": "ODYSSEY2"
    },
    "Mattel Intellivision": {
        "libretro": "Mattel_-_Intellivision",
        "miyoo": "INT"
    },
    # "MicroW8": {
    #     "libretro": "",
    #     "miyoo": "UW9"
    # },
    "MSX": {
        "libretro": "Microsoft_-_MSX",
        "miyoo": "MSX"
    },
    "MSX2": {
        "libretro": "Microsoft_-_MSX2",
        "miyoo": "MSX"
    },
    #MrBoom
    "NEC PC Engine": {
        "libretro": "NEC_-_PC_Engine_-_TurboGrafx_16",
        "miyoo": "PCE"
    },
    "NEC PC Engine CD": {
        "libretro": "NEC_-_PC_Engine_-_TurboGrafx_CD",
        "miyoo": "PCE"
    },
    "NEC PC Engine SuperGrafx": {
        "libretro": "NEC_-_PC_Engine_SuperGrafx",
        "miyoo": "PCE"
    },
    "NEC PC 8001": {
        "libretro": "NEC_-_PC-8001_-_PC-8801",
        "miyoo": "PC_88"
    },
    #NEC - PC-98
    #NEC - PC-FX
    "Nintendo Game Boy": {
        "libretro": "Nintendo_-_Game_Boy",
        "miyoo": "GB"
    },
    "Nintendo Game Boy Color": {
        "libretro": "Nintendo_-_Game_Boy_Color",
        "miyoo": "GB" # This is inline with wiki, so the same dir for GB & GBC, since similar emulators are used
    },
    "Nintendo Game Boy Advance": {
        "libretro": "Nintendo_-_Game_Boy_Advance",
        "miyoo": "GBA"
    },
    "Nintendo Entertainment System": {
        "libretro": "Nintendo_-_Nintendo_Entertainment_System",
        "miyoo": "NES"
    },
    "Nintendo Famicom Disk System": {
        "libretro": "Nintendo_-_Family_Computer_Disk_System",
        "miyoo": "NES"
    },
    "Nintendo Pokémon Mini": {
        "libretro": "Nintendo_-_Pokemon_Mini",
        "miyoo": "POKEMINI"
    },
    "Nintendo Super Nintendo": {
        "libretro": "Nintendo_-_Super_Nintendo_Entertainment_System",
        "miyoo": "SNES"
    },
    # "Nintendo 64": {
    #     "libretro": "Nintendo_-_Nintendo_64",
    #     "miyoo": "NINTENDO_64"
    # },
    #Nintendo - Nintendo 64DD
    # "Nintendo DS": {
    #     "libretro": "Nintendo_-_Nintendo_DS",
    #     "miyoo": "NDS"
    # },
    #Nintendo - Nintendo DSi
    # "Nintendo GameCube": {
    #     "libretro": "Nintendo_-_GameCube",
    #     "miyoo": "GAMECUBE"
    # },
    "Nintendo Satellaview": {
        "libretro": "Nintendo_-_Satellaview",
        "miyoo": "SNES"
    },
    "Nintendo Sufami Turbo": {
        "libretro": "Nintendo - Sufami Turbo",
        "miyoo": "SNES"
    },
    # "Nintendo Wii": {
    #     "libretro": "Nintendo_-_Wii",
    #     "miyoo": "WII"
    # },
    #Nintendo - Wii U
    # "Nintendo Virtual Boy": {
    #     "libretro": "Nintendo_-_Virtual_Boy",
    #     "miyoo": "VIRTUAL_BOY"
    # },
    # "Philips CD-i": {
    #     "libretro": "Philips_-_CD-i",
    #     "miyoo": "CDI2015"
    # },
    "Philips Videopac+": {
        "libretro": "Philips_-_Videopac+",
        "miyoo": "ODYSSEY2"
    },
    "PlayStation 1": {
        "libretro": "Sony_-_PlayStation",
        "miyoo": "PS1"
    },
    # "PS2": {
    #     "libretro": "Sony_-_PlayStation_2",
    #     "miyoo": "PLAYSTATION2"
    # },
    # "PS3": {
    #     "libretro": "Sony_-_PlayStation_3",
    #     "miyoo": "PLAYSTATION3"
    # },
    #PS4
    # "PSP": {
    #     "libretro": "Sony_-_PlayStation_Portable",
    #     "miyoo": "PLAYSTATION_PORTABLE"
    # },
    # "PS Vita": {
    #     "libretro": "Sony_-_PlayStation_Vita",
    #     "miyoo": "PLAYSTATION_VITA"
    # },
    "Quake": {
        "libretro": "Quake",
        "miyoo": "QUAKE_1"
    },
    #Quake II
    #Quake III
    #RCA - Studio II
    #RPG Maker
    #Rick Dangerous
    "Sharp X1": {
        "libretro": "Sharp_-_X1",
        "miyoo": "SHARP_X1"
    },
    # "Sharp X68000": {
    #     "libretro": "Sharp_-_X68000",
    #     "miyoo": "SHARP_X68000"
    # },
    "ScummVM": {
        "libretro": "ScummVM",
        "miyoo": "SCUMMVM"
    },
    "SEGA SG-1000": {
        "libretro": "Sega_-_SG-1000",
        "miyoo": "SMS" # There isn't any specifc emu for SG-1000, and they use SMS for most-used case
    },
    "SEGA Game Gear": {
        "libretro": "Sega_-_Game_Gear",
        "miyoo": "SMS" # This is inline with wiki, so the same dir for SMS & GG
    },
    "SEGA Master System": {
        "libretro": "Sega_-_Master_System_-_Mark_III",
        "miyoo": "SMS"
    },
    "SEGA Mega Drive/Genesis": {
        "libretro": "Sega_-_Mega_Drive_-_Genesis",
        "miyoo": "SMD"
    },
    "SEGA CD": {
        "libretro": "Sega_-_Mega-CD_-_Sega_CD",
        "miyoo": "SMD"
    },
    "SEGA 32X": {
        "libretro": "Sega_-_32X",
        "miyoo": "SMD"
    },
    "SEGA PICO": {
        "libretro": "SEGA_-_PICO",
        "miyoo": "SMD"
    },
    # "SEGA Saturn": {
    #     "libretro": "Sega_-_Saturn",
    #     "miyoo": "SEGA_SATURN"
    # },
    # "SEGA Dreamcast": {
    #     "libretro": "Sega_-_Dreamcast",
    #     "miyoo": "DREAMCAST"
    # },
    # "SEGA Naomi": {
    #     "libretro": "Sega_-_Naomi",
    #     "miyoo": "ATOMISWAVE"
    # },
    #Sega - Naomi 2
    # "SEGA VMU": {
    #     "libretro": "",
    #     "miyoo": "VMU"
    # },
    "Sinclair ZX Spectrum": {
        "libretro": "Sinclair_-_ZX_Spectrum",
        "miyoo": "Z80"
    },
    "Sinclair ZX 81": {
        "libretro": "Sinclair_-_ZX_81",
        "miyoo": "ZX81"
    },
    # "SNK Neo Geo CD": {
    #     "libretro": "SNK_-_Neo_Geo_CD",
    #     "miyoo": "NEOGEO"
    # },
    "SNK Neo Geo Pocket": {
        "libretro": "SNK_-_Neo_Geo_Pocket",
        "miyoo": "NGP"
    },
    "SNK Neo Geo Pocket Color": {
        "libretro": "SNK_-_Neo_Geo_Pocket_Color",
        "miyoo": "NGP"
    },
    "Spectravideo": {
        "libretro": "Spectravideo_-_SVI-318_-_SVI-328",
        "miyoo": "MSX"
    },
    # "Texas Instruments": {
    #     "libretro": "",
    #     "miyoo": "TI_83"
    # },
    # "The 3DO": {
    #     "libretro": "The_3DO_Company_-_3DO",
    #     "miyoo": "3DO"
    # },
    "TIC-80": {
        "libretro": "TIC-80",
        "miyoo": "TIC80"
    },
    "Thomson": {
        "libretro": "Thomson_-_MOTO",
        "miyoo": "THOMSON"
    },
    #Tiger - Game.com
    #Tomb Raider
    #VTech - CreatiVision
    #VTech - V.Smile
    #Vircon32
    "WASM-4": {
        "libretro": "WASM-4",
        "miyoo": "WASM4"
    },
    "Watara Supervision": {
        "libretro": "Watara_-_Supervision",
        "miyoo": "SUPERVISION"
    },
    "Wolfenstein 3D": {
        "libretro": "Wolfenstein_3D",
        "miyoo": "WOLFENSTEIN3D"
    },
    # "VaporSpec": {
    #     "libretro": "",
    #     "miyoo": "VAPORSPEC"
    # },
}

extensions = ('.zip', '.7z', '.p', '.tzx', '.t81', '.a52', '.bin', '.bin', '.tvc', '.hex', '.arduboy', '.hex', '.xfd', '.atr', '.dcm', '.cas', '.bin', '.a52atx', '.car', '.rom', '.com', '.xex', '.m3u', '.bin', '.rom', '.ri', '.mx1', '.mx2', '.dsk', '.col', '.sg', '.sc', '.sf', '.cas', '.m3u', '.game', '.88', '.dsk', '.snatap', '.cdt', '.voc', '.cpr', '.m3u', '.chai', '.chailove', '.bin', '.md', '.gen', '.cue', '.iso', '.st', '.msadmy', '.k1', '.a1', '.6c', '.c6', '.d2', '.s1', '.f4', '.a4', '.1da', '.da1', '.C4', '.4c', '.4d', '.d7', '.d4', '.gamedosz', '.exe', '.com', '.bat', '.iso', '.chd', '.cue', '.ins', '.img', '.ima', '.vhd', '.jrc', '.tc', '.m3u', '.m3u8', '.conf', '.wl6', '.n3d', '.sod', '.sdm', '.wl1', '.pk3', '.exe', '.p8', '.png', '.fds', '.nes', '.unif', '.unf', '.rom', '.mx1', '.mx2', '.dsk', '.fdi', '.cas', '.m3u', '.bin', '.chf', '.int', '.bin', '.rom', '.d64', '.t64', '.x64', '.p00', '.lnx', '.lyxtzx', '.tap', '.z80', '.rzx', '.scl', '.trd', '.dsk', '.dck', '.sna', '.szxgam', '.gb', '.gbc', '.dmg', '.gb', '.dmg', '.gbc', '.cgb', '.sgb', '.col', '.cv', '.bin', '.rom', '.pce', '.sgx', '.cue', '.chd', '.lnx', '.lyx', '.o', '.sms', '.gg', '.sg', '.bin', '.rom', '.mdx', '.md', '.smd', '.gen', '.bin', '.cue', '.iso', '.sms', '.bms', '.gg', '.sg', '.68k', '.sgd', '.chd', '.m3u', '.mdx', '.md', '.smd', '.gen', '.bin', '.cue', '.iso', '.sms', '.bms', '.gg', '.sg', '.68k', '.sgd', '.chd', '.m3u', '.ay', '.gbs', '.gym', '.hes', '.kss', '.nsf', '.nsfe', '.sap', '.spc', '.vgm', '.vgz', '.gba', '.bin', '.mgw', '.lnx', '.lyx', '.o', '.ch8', '.sc8', '.xo8', '.dat', '.nx', '.lutro', '.love', '.lua7zzip', '.pce', '.cue', '.ccd', '.chd', '.toc', '.m3u', '.pce', '.sgx', '.cue', '.ccd', '.chd', '.ws', '.wsc', '.pc2', '.pcv2', '.gb', '.gbc', '.gba', '.dsk', '.imghvf', '.cmd', '.desktop', '.prc', '.pqa', '.img', '.pdb8xp', '.8xk', '.8xg', '.exe', '.bin', '.bin', '.cue', '.img', '.mdf', '.pbp', '.toc', '.cbn', '.m3u', '.ccd', '.chd', '.iso', '.exebin777', '.ptn777', '.bin', '.gen', '.smd', '.md', '.32x', '.cue', '.iso', '.chd', '.sms', '.gg', '.sg', '.sc', '.m3u', '.68k', '.sgd', '.pco', '.cdg', '.min', '.bin', '.sv', '.wad', '.iwad', '.pwad', '.a78', '.bin', '.cdf', '.d88', '.u88', '.m3u', '.nes', '.ngp', '.ngc', '.ngpc', '.npc', '.map', '.aba', '.seq', '.lev', '.p8', '.png', '.sms', '.bin', '.rom', '.col', '.gg', '.sg', '.smc', '.fig', '.sfc', '.gd3', '.gd7', '.dx2', '.bsx', '.swc', '.smc', '.fig', '.sfc', '.gd3', '.gd7', '.dx2', '.bsx', '.swc', '.a26', '.bin', '.b', '.bin', '.rom', '.fd', '.sap', '.k7', '.m7', '.m5', '.rom', '.tic', '.pak', '.adf', '.adz', '.uw8', '.wasm', '.vaporbin', '.bin', '.vec', '.vms', '.dci', '.bin', '.wasm', '.dx12d', '.2hd', '.tfd', '.d88', '.88d', '.hdm', '.xdf', '.dup', '.tap', '.cmd')

libretro_replacements = {
    "&": "_", 
    "~": "_",
}
def normalize_libretro_filename(name):
    for original, replacement in libretro_replacements.items():
        name = name.replace(original, replacement)
    return name.strip()

revs = {
    "(Rev 1)": "",
    "(Rev 2)": "",
    "(Rev 3)": "",
    "(Rev 4)": "",
    "(Rev 5)": "",
    "(Rev 6)": "",
    "Rev A": "",
    "Rev B": "",
    "Rev C": "",
}

def no_rev_filename(name):
    for original, replacement in revs.items():
        name = name.replace(original, replacement)
    return name

def is_valid_image(data):
    try:
        with Image.open(BytesIO(data)) as img:
            img.verify()
        return True
    except (UnidentifiedImageError, OSError):
        return False

# --- UTILS ___

def get_latest_commit_hash(libretro_folder):
    api_url = f"https://api.github.com/repos/libretro-thumbnails/{libretro_folder}/commits"
    headers = {"Accept": "application/vnd.github+json"}
    response = requests.get(api_url, headers=headers, timeout=10)
    if response.status_code == 200:
        return response.json()[0]["sha"]
    else:
        raise RuntimeError(f"Failed to fetch latest commit for {libretro_folder}: {response.status_code}")

def download_libretro_thumbnail(libretro_folder, art_type, rom_name, commit):
    filename = f"{rom_name}.png"
    encoded_filename = quote(filename, safe="")  # full encoding
    url = f"https://raw.githubusercontent.com/libretro-thumbnails/{libretro_folder}/{commit}/{art_type}/{encoded_filename}"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.content
    else:
        return None
    
def resize_image(image_bytes, width=128):
    try:
        img = Image.open(BytesIO(image_bytes))
        w_percent = width / float(img.size[0])
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((width, h_size), Image.LANCZOS)
        output = BytesIO()
        img.save(output, format="PNG")
        return output.getvalue()
    except Exception as e:
        print(f"✖ [ERROR] Failed to resize image: {e}") 
        return None
    # TODO: replace print with logging or GUI status output
    
def save_image(image_bytes, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(image_bytes)
        
def get_rom_files(roms_folder, extensions):
    roms = []
    for root, _, files in os.walk(roms_folder):
        for f in files:
            if f.lower().endswith(extensions) and not f.startswith("._"):
                roms.append(f)
    return roms

# --- SCRAPER LOGIC ---
def run_scraper(roms_folder, system_key, output_mode, scraper_mode, progress_callback=None, miyoo_root=None):
    libretro_folder = systems[system_key]["libretro"]
    miyoo_folder = systems[system_key]["miyoo"]
    commit = get_latest_commit_hash(libretro_folder)
    
    if output_mode == "miyoo":
        if not miyoo_root:
            raise RuntimeError("No MIYOO root folder selected.")
        base_output = os.path.join(miyoo_root, miyoo_folder)
        output_boxarts = output_logos = output_snaps = output_titles = os.path.join(base_output, ".images")
    else:
        output_boxarts = output_logos = output_snaps = output_titles = os.path.join(roms_folder, ".images")
        
    rom_files = get_rom_files(roms_folder, extensions)
    total = len(rom_files)
    if total == 0:
        raise RuntimeError(f"No ROM files found in {roms_folder} folder.")
    
    failed = []
    skipped = []
    for idx, rom in enumerate(rom_files, start=1):
        rom_name, _ = os.path.splitext(rom)
        normalized_name = normalize_libretro_filename(rom_name)
        if scraper_mode == "boxarts":
            boxart_path = os.path.join(output_boxarts, f"{rom_name}.png")
        elif scraper_mode == "logos":
            logo_path = os.path.join(output_logos, f"{rom_name}.png")
        elif scraper_mode == "screenshots":
            snap_path = os.path.join(output_snaps, f"{rom_name}.png")
        else:
            title_path = os.path.join(output_titles, f"{rom_name}.png")
        
        # Scrap Art
        if scraper_mode == "boxarts":
        # Download Boxart
            if not os.path.exists(boxart_path):
                # Try download with normalized name
                boxart_bytes = download_libretro_thumbnail(libretro_folder, "Named_Boxarts", normalized_name, commit)  
                # Fallback: try without (Rev X) etc if 1st attempt failed
                if not boxart_bytes or not is_valid_image(boxart_bytes):
                    fallback_name = normalize_libretro_filename(no_rev_filename(rom_name))
                    if fallback_name != normalized_name:
                        boxart_bytes = download_libretro_thumbnail(
                            libretro_folder, "Named_Boxarts", fallback_name, commit
                        )        
                if boxart_bytes:
                    resized = resize_image(boxart_bytes)
                    if resized:
                        save_image(resized, boxart_path)
                    else:
                        failed.append(f"{rom_name} (Boxart - Resize Error)")
                else:
                    failed.append(f"{rom_name} (Boxart)")
            else:
                skipped.append(f"{rom_name} (Boxart)")
        elif scraper_mode == "logos":
            # Download Logos
            if not os.path.exists(logo_path):
                logo_bytes = download_libretro_thumbnail(libretro_folder, "Named_Logos", normalized_name, commit)
                if not logo_bytes or not is_valid_image(logo_bytes):
                    fallback_name = normalize_libretro_filename(no_rev_filename(rom_name))
                    if fallback_name != normalized_name:
                        logo_bytes = download_libretro_thumbnail(
                            libretro_folder, "Named_Logos", fallback_name, commit
                        )
                if logo_bytes:
                    save_image(logo_bytes, logo_path)
                else:
                    failed.append(f"{rom_name} (Logo)")
            else:
                skipped.append(f"{rom_name} (Logo)")
        elif scraper_mode == "screenshots":
            # Download Snap(screenshot)
            if not os.path.exists(snap_path):
                snap_bytes = download_libretro_thumbnail(libretro_folder, "Named_Snaps", normalized_name, commit)
                if not snap_bytes or not is_valid_image(snap_bytes):
                    fallback_name = normalize_libretro_filename(no_rev_filename(rom_name))
                    if fallback_name != normalized_name:
                        snap_bytes = download_libretro_thumbnail(
                            libretro_folder, "Named_Snaps", fallback_name, commit
                        )
                if snap_bytes:
                    save_image(snap_bytes, snap_path)
                else:
                    failed.append(f"{rom_name} (Screenshot)")
            else:
                skipped.append(f"{rom_name} (Screenshot)")
        else:
            # Download Title
            if not os.path.exists(title_path):
                title_bytes = download_libretro_thumbnail(libretro_folder, "Named_Titles", normalized_name, commit)
                if not title_bytes or not is_valid_image(title_bytes):
                    fallback_name = normalize_libretro_filename(no_rev_filename(rom_name))
                    if fallback_name != normalized_name:
                        title_bytes = download_libretro_thumbnail(
                            libretro_folder, "Named_Titles", fallback_name, commit
                        )
                if title_bytes:
                    save_image(title_bytes, title_path)
                else:
                    failed.append(f"{rom_name} (Title)")
            else:
                skipped.append(f"{rom_name} (Title)")
        
        if progress_callback:
            progress_callback(idx, total)
            
    return failed, skipped

# --- GUI CLASS ---
class RAScraperGUI:
    def __init__(self, root):
        self.root = root
        root.title("RetroArch Scraper")
        root.geometry("800x600")
        
        # Variables
        self.roms_path = tk.StringVar()
        self.miyoo_root_path = tk.StringVar()
        self.selected_system = tk.StringVar()
        self.output_option = tk.StringVar(value="miyoo")
        self.scraper_option = tk.StringVar(value="boxarts")
        self.progress = tk.IntVar(value=0)
        self.progress_text = tk.StringVar(value="")
        
        # ROMs folder
        tk.Label(root, text="ROMs Folder:").pack(anchor="w", padx=10, pady=(10,0))
        rom_frame = tk.Frame(root)
        rom_frame.pack(fill="x", padx=10)
        tk.Entry(rom_frame, textvariable=self.roms_path).pack(side="left", fill="x", expand=True)
        tk.Button(rom_frame, text="Browse", command=self.browse_roms).pack(side="right")
        
        # MIYOO root folder
        tk.Label(root, text="MIYOO Root Folder (only needed if MIYOO output selected):").pack(anchor="w", padx=10, pady=(10,0))
        miyoo_frame = tk.Frame(root)
        miyoo_frame.pack(fill="x", padx=10)
        tk.Entry(miyoo_frame, textvariable=self.miyoo_root_path).pack(side="left", fill="x", expand=True)
        tk.Button(miyoo_frame, text="Browse", command=self.browse_miyoo).pack(side="right")
        
        # System dropdown
        tk.Label(root, text="Select System:").pack(anchor="w", padx=10, pady=(10,0))
        systems_list = list(systems.keys())
        self.selected_system.set(systems_list[0])
        tk.OptionMenu(root, self.selected_system, *systems_list).pack(fill="x", padx=10)
        
        # Output options
        tk.Label(root, text="Where should artwork be saved?").pack(anchor="w", padx=10, pady=(10,0))
        output_frame = tk.Frame(root)
        output_frame.pack(fill="x", padx=20)
        tk.Radiobutton(output_frame, text="MIYOO-compatible roms folder (MIYOO/{system}/.images)", variable=self.output_option, value="miyoo").pack(anchor="w")
        tk.Radiobutton(output_frame, text="Within root ROMs folder (/.images)", variable=self.output_option, value="roms").pack(anchor="w")

        tk.Label(root, text="What type of artwork should be downloaded?").pack(anchor="w", padx=10, pady=(10,0))
        output_frame = tk.Frame(root)
        output_frame.pack(fill="x", padx=20)
        tk.Radiobutton(output_frame, text="Boxarts", variable=self.scraper_option, value="boxarts").pack(anchor="w")
        tk.Radiobutton(output_frame, text="Logos", variable=self.scraper_option, value="logos").pack(anchor="w")
        tk.Radiobutton(output_frame, text="Screenshots", variable=self.scraper_option, value="screenshots").pack(anchor="w")
        tk.Radiobutton(output_frame, text="Titles", variable=self.scraper_option, value="titles").pack(anchor="w")

        # Progress bar and label
        self.progress_bar = ttk.Progressbar(root, maximum=100, variable=self.progress)
        self.progress_bar.pack(fill="x", padx=10, pady=(15,5))
        tk.Label(root, textvariable=self.progress_text).pack()
        
        # Run button
        self.btn_run = tk.Button(root, text="RUN SCRAPER", bg="white", fg="black", font=("Arial", 12, "bold"),  command=self.run_scraper_thread)
        self.btn_run.pack(pady=15, ipadx=10, ipady=5)
        
    def browse_roms(self):
        path = filedialog.askdirectory()
        if path:
            self.roms_path.set(path)
            
    def browse_miyoo(self):
        path = filedialog.askdirectory()
        if path:
            self.miyoo_root_path.set(path)
            
    def update_progress(self, current, total):
        percent = int((current / total) * 100)
        self.progress.set(percent)
        self.progress_text.set(f"Processing {current} of {total} ROMs...")
        
    def run_scraper_thread(self):
        roms_folder = self.roms_path.get().strip()
        miyoo_root = self.miyoo_root_path.get().strip()
        system_key = self.selected_system.get()
        output_mode = self.output_option.get()
        scraper_mode = self.scraper_option.get()
        
        if not roms_folder:
            messagebox.showwarning("Missing input", "Please select a ROMs folder.")
            return
        
        if output_mode == "miyoo" and not miyoo_root:
            messagebox.showwarning("Missing input", "Please select your MIYOO root folder.")
            return
        
        self.btn_run.config(state="disabled")
        self.progress.set(0)
        self.progress_text.set("Starting...")
        
        def task():
            try:
                failed, skipped = run_scraper(roms_folder, system_key, output_mode, scraper_mode, self.update_progress, miyoo_root)
                self.progress_text.set("Done!")
                message = "Scraping complete!\n"
                if skipped:
                    message += f"✓ Skipped {len(skipped)} image(s) already present.\n"
                if failed:
                    message += f"✖ Failed to find {len(failed)} images:\n" + "\n".join(failed)
                if skipped or failed:
                    messagebox.showinfo("Completed", message)
                else:
                    messagebox.showinfo("Completed", "All images have been downloaded.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                self.btn_run.config(state="normal")
                
        threading.Thread(target=task, daemon=True).start()
        
# ---  RUN APP ---

def main():
    root = tk.Tk()
    app = RAScraperGUI(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()