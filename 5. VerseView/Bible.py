import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os

# 1. Define the standard 66 Bible Books (Protestant Canon)
# We use English names for the 'bname' attribute to ensure VerseView indexes them correctly.
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

def convert_to_zefania(input_file, output_file):
    print(f"Reading {input_file}...")
    
    try:
        tree = ET.parse(input_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return

    # Create new Zefania Root
    new_root = ET.Element("XMLBIBLE", biblename="Myanmar Bible")
    
    # Add Information Header
    info = ET.SubElement(new_root, "INFORMATION")
    ET.SubElement(info, "title").text = "Myanmar Bible"
    ET.SubElement(info, "creator").text = root.find('copyright').text if root.find('copyright') is not None else "Unknown"
    ET.SubElement(info, "description").text = "Converted from Legacy VerseView Format"
    
    # Iterate through books
    # The legacy format relies on order: 1st <b> is Genesis, 2nd is Exodus, etc.
    legacy_books = root.findall('b')
    
    print(f"Found {len(legacy_books)} books in source file.")
    
    for i, b_tag in enumerate(legacy_books):
        if i >= len(BIBLE_BOOKS):
            print(f"Warning: Source has more books than standard 66. Skipping index {i}.")
            continue
            
        book_name = BIBLE_BOOKS[i]
        book_number = str(i + 1)
        
        # Create Zefania BIBLEBOOK tag
        # Attributes: bnumber (1-66), bname (Book Name)
        z_book = ET.SubElement(new_root, "BIBLEBOOK", bnumber=book_number, bname=book_name)
        
        # Iterate Chapters
        chapters = b_tag.findall('c')
        for j, c_tag in enumerate(chapters):
            chapter_number = str(j + 1)
            
            # Create Zefania CHAPTER tag
            z_chapter = ET.SubElement(z_book, "CHAPTER", cnumber=chapter_number)
            
            # Iterate Verses
            verses = c_tag.findall('v')
            for k, v_tag in enumerate(verses):
                verse_number = str(k + 1)
                
                # Create Zefania VERS tag
                z_verse = ET.SubElement(z_chapter, "VERS", vnumber=verse_number)
                z_verse.text = v_tag.text  # Copy the verse text
                
    # Generate pretty XML string
    print("Generating Zefania XML...")
    xml_str = minidom.parseString(ET.tostring(new_root, encoding='utf-8')).toprettyxml(indent="  ")
    
    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_str)
        
    print(f"Success! Converted file saved as: {output_file}")

# Run the conversion
if __name__ == "__main__":
    input_filename = "Myanmar Bible.xml"   # Make sure this matches your file name exactly
    output_filename = "Myanmar_Bible_Zefania.xml"
    
    if os.path.exists(input_filename):
        convert_to_zefania(input_filename, output_filename)
    else:
        print(f"File '{input_filename}' not found. Please check the filename.")