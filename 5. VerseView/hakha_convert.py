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

    # Create new Zefania Root
    # Using the title found in the source file for the biblename
    source_title = root.find('title').text if root.find('title') is not None else "Hakha Bible"
    new_root = ET.Element("XMLBIBLE", biblename=source_title)
    
    # Add Information Header
    info = ET.SubElement(new_root, "INFORMATION")
    ET.SubElement(info, "title").text = source_title
    ET.SubElement(info, "creator").text = root.find('copyright').text if root.find('copyright') is not None else "Unknown"
    ET.SubElement(info, "description").text = "Converted from Hakha Bible_(HCL).xml"
    
    # 1. Find all Book tags <b>
    # This file nests books inside <bb> (likely "Bible Block" or Testament), 
    # so we use ".//b" to find all <b> tags wherever they are.
    books = root.findall('.//b')
    
    print(f"Found {len(books)} books.")

    for i, b_tag in enumerate(books):
        # Get Book Name from the existing 'n' attribute (e.g., "Genesis", "Levitikas")
        book_name = b_tag.get('n')
        if not book_name: 
            book_name = f"Book {i+1}" # Fallback if attribute is missing
            
        book_number = str(i + 1)
        
        # Create Zefania BIBLEBOOK tag
        z_book = ET.SubElement(new_root, "BIBLEBOOK", bnumber=book_number, bname=book_name)
        
        # Iterate Chapters
        chapters = b_tag.findall('c')
        for j, c_tag in enumerate(chapters):
            # Get Chapter number from attribute 'n' or use counter
            chapter_num = c_tag.get('n', str(j + 1))
            
            z_chapter = ET.SubElement(z_book, "CHAPTER", cnumber=chapter_num)
            
            # Iterate Verses
            verses = c_tag.findall('v')
            for k, v_tag in enumerate(verses):
                # Get Verse number from attribute 'n' or use counter
                verse_num = v_tag.get('n', str(k + 1))
                
                z_verse = ET.SubElement(z_chapter, "VERS", vnumber=verse_num)
                z_verse.text = v_tag.text

    # Generate pretty XML string
    print("Generating Zefania XML...")
    xml_str = minidom.parseString(ET.tostring(new_root, encoding='utf-8')).toprettyxml(indent="  ")
    
    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_str)
        
    print(f"Success! Converted file saved as: {output_file}")

if __name__ == "__main__":
    input_filename = "Hakha Bible_(HCL).xml"
    output_filename = "Hakha_Bible_Zefania.xml"
    
    if os.path.exists(input_filename):
        convert_hakha_to_zefania(input_filename, output_filename)
    else:
        print(f"File '{input_filename}' not found. Please check the filename.")