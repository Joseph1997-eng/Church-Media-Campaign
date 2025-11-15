import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os

def convert_hakha_to_zefania(input_file, output_file):
    print(f"Reading {input_file}...")
    
    try:
        tree = ET.parse(input_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return

    # 1. Get Metadata (Title, Font, Copyright) from the source
    source_title = root.find('title').text if root.find('title') is not None else "Hakha Bible"
    source_font = root.find('font').text if root.find('font') is not None else "Arial" # Default if missing
    source_copy = root.find('copyright').text if root.find('copyright') is not None else "Unknown"

    print(f"Detected Font: {source_font}")

    # 2. Create new Zefania Root
    new_root = ET.Element("XMLBIBLE", biblename=source_title)
    
    # 3. Add Information Header
    info = ET.SubElement(new_root, "INFORMATION")
    ET.SubElement(info, "title").text = source_title
    ET.SubElement(info, "creator").text = source_copy
    
    # We add the font info to the description so it's visible in metadata
    ET.SubElement(info, "description").text = f"Converted from Hakha Bible. Font: {source_font}"
    
    # 4. Find all Book tags <b>
    books = root.findall('.//b')
    print(f"Found {len(books)} books.")

    for i, b_tag in enumerate(books):
        # Use the 'n' attribute for the book name (e.g., "Genesis")
        book_name = b_tag.get('n')
        if not book_name: 
            book_name = f"Book {i+1}"
            
        book_number = str(i + 1)
        
        # Create Zefania BIBLEBOOK tag
        z_book = ET.SubElement(new_root, "BIBLEBOOK", bnumber=book_number, bname=book_name)
        
        # Iterate Chapters
        chapters = b_tag.findall('c')
        for j, c_tag in enumerate(chapters):
            chapter_num = c_tag.get('n', str(j + 1))
            z_chapter = ET.SubElement(z_book, "CHAPTER", cnumber=chapter_num)
            
            # Iterate Verses
            verses = c_tag.findall('v')
            for k, v_tag in enumerate(verses):
                verse_num = v_tag.get('n', str(k + 1))
                z_verse = ET.SubElement(z_chapter, "VERS", vnumber=verse_num)
                z_verse.text = v_tag.text

    # 5. Generate XML
    print("Generating Zefania XML...")
    xml_str = minidom.parseString(ET.tostring(new_root, encoding='utf-8')).toprettyxml(indent="  ")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_str)
        
    print(f"Success! Saved to: {output_file}")
    print(f"NOTE: When importing into VerseView, select '{source_font}' in the font settings.")

if __name__ == "__main__":
    input_filename = "Hakha Bible_(HCL).xml"
    output_filename = "Hakha_Bible_Zefania_v2.xml"
    
    if os.path.exists(input_filename):
        convert_hakha_to_zefania(input_filename, output_filename)
    else:
        print(f"File '{input_filename}' not found.")