import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os

# Standard 66 Bible Books List (Protestant Order)
# Required because your file doesn't have book names in the tags
BIBLE_BOOKS = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth", 
    "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra", 
    "Nehemiah", "Esther", "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", 
    "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", 
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", 
    "Malachi", "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", 
    "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians", 
    "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James", 
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"
]

def convert_myanmar_to_zefania(input_file, output_file):
    print(f"Reading {input_file}...")
    
    try:
        tree = ET.parse(input_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return

    # 1. Extract Metadata (Title, Font, Copyright)
    source_title = root.find('title').text if root.find('title') is not None else "Myanmar Bible"
    source_font = root.find('font').text if root.find('font') is not None else "Pyidaungsu"
    source_copy = root.find('copyright').text if root.find('copyright') is not None else "Unknown"
    
    print(f"Detected Font: {source_font}")

    # 2. Create Zefania Root
    new_root = ET.Element("XMLBIBLE", biblename=source_title)
    
    # 3. Add Information Header
    info = ET.SubElement(new_root, "INFORMATION")
    ET.SubElement(info, "title").text = source_title
    ET.SubElement(info, "creator").text = source_copy
    # Add font info to description so you can see it in VerseView
    ET.SubElement(info, "description").text = f"Converted from Myanmar Bible. Font: {source_font}"
    
    # 4. Process Books
    # Your Myanmar file uses simple <b> tags without names, so we map them by index.
    legacy_books = root.findall('b')
    print(f"Found {len(legacy_books)} books.")
    
    for i, b_tag in enumerate(legacy_books):
        if i >= len(BIBLE_BOOKS):
            continue
            
        book_name = BIBLE_BOOKS[i]
        book_number = str(i + 1)
        
        # Create Book Tag
        z_book = ET.SubElement(new_root, "BIBLEBOOK", bnumber=book_number, bname=book_name)
        
        # Process Chapters
        chapters = b_tag.findall('c')
        for j, c_tag in enumerate(chapters):
            chapter_number = str(j + 1)
            z_chapter = ET.SubElement(z_book, "CHAPTER", cnumber=chapter_number)
            
            # Process Verses
            verses = c_tag.findall('v')
            for k, v_tag in enumerate(verses):
                verse_number = str(k + 1)
                z_verse = ET.SubElement(z_chapter, "VERS", vnumber=verse_number)
                z_verse.text = v_tag.text
                
    # 5. Save to File
    print("Generating Zefania XML...")
    xml_str = minidom.parseString(ET.tostring(new_root, encoding='utf-8')).toprettyxml(indent="  ")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_str)
        
    print(f"Success! Saved to: {output_file}")
    print(f"IMPORTANT: In VerseView, select '{source_font}' as the font for this version.")

if __name__ == "__main__":
    input_filename = "Myanmar Bible.xml"
    output_filename = "Myanmar_Bible_Zefania_v2.xml"
    
    if os.path.exists(input_filename):
        convert_myanmar_to_zefania(input_filename, output_filename)
    else:
        print(f"File '{input_filename}' not found.")