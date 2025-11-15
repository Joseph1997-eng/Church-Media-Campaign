import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

# Standard English Book Names (Required for VerseView to recognize the books)
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

def create_clean_zefania_doc(biblename, font, copyright_text):
    doc = minidom.Document()
    
    # SIMPLEST VALID ROOT (No Schema Links, No complex Version IDs)
    root = doc.createElement("XMLBIBLE")
    root.setAttribute("biblename", biblename)
    root.setAttribute("copyright", copyright_text)
    doc.appendChild(root)
    
    # Simple Information Header
    info = doc.createElement("INFORMATION")
    root.appendChild(info)
    
    def add_info(tag, text):
        node = doc.createElement(tag)
        node.appendChild(doc.createTextNode(text))
        info.appendChild(node)

    add_info("title", biblename)
    add_info("rights", copyright_text)
    add_info("description", f"Font: {font}")
    
    return doc, root

def process_myanmar(input_file, output_file):
    print(f"Processing {input_file} (Clean Format)...")
    try:
        tree = ET.parse(input_file)
        src_root = tree.getroot()
    except Exception as e:
        print(f"Error: {e}")
        return

    title = src_root.find('title').text if src_root.find('title') is not None else "Myanmar Bible"
    font = src_root.find('font').text if src_root.find('font') is not None else "Pyidaungsu"
    
    doc, root = create_clean_zefania_doc(title, font, "Public Domain")

    legacy_books = src_root.findall('b')
    for i, b_tag in enumerate(legacy_books):
        if i >= len(BIBLE_BOOKS): continue
        
        # Standard Zefania Book Tag
        book_node = doc.createElement("BIBLEBOOK")
        book_node.setAttribute("bnumber", str(i + 1))
        book_node.setAttribute("bname", BIBLE_BOOKS[i]) # English Names are safest
        root.appendChild(book_node)

        for j, c_tag in enumerate(b_tag.findall('c')):
            chap_node = doc.createElement("CHAPTER")
            chap_node.setAttribute("cnumber", str(j + 1))
            book_node.appendChild(chap_node)
            
            for k, v_tag in enumerate(c_tag.findall('v')):
                vers_node = doc.createElement("VERS")
                vers_node.setAttribute("vnumber", str(k + 1))
                # Plain text content (Most compatible)
                verse_text = v_tag.text if v_tag.text else ""
                vers_node.appendChild(doc.createTextNode(verse_text))
                chap_node.appendChild(vers_node)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(doc.toprettyxml(indent="  "))
    print(f"Created: {output_file}")

def process_hakha(input_file, output_file):
    print(f"Processing {input_file} (Clean Format)...")
    try:
        tree = ET.parse(input_file)
        src_root = tree.getroot()
    except Exception as e:
        print(f"Error: {e}")
        return

    title = src_root.find('title').text if src_root.find('title') is not None else "Hakha Bible"
    font = src_root.find('font').text if src_root.find('font') is not None else "Calibri"
    
    doc, root = create_clean_zefania_doc(title, font, "Public Domain")

    # Flatten nested structure (Remove <bb> tags logic)
    books = src_root.findall('.//b')
    for i, b_tag in enumerate(books):
        # Keep existing name or fallback to index
        book_name = b_tag.get('n', f"Book {i+1}")
        
        book_node = doc.createElement("BIBLEBOOK")
        book_node.setAttribute("bnumber", str(i + 1))
        book_node.setAttribute("bname", book_name)
        root.appendChild(book_node)

        for j, c_tag in enumerate(b_tag.findall('c')):
            c_num = c_tag.get('n', str(j + 1))
            chap_node = doc.createElement("CHAPTER")
            chap_node.setAttribute("cnumber", c_num)
            book_node.appendChild(chap_node)
            
            for k, v_tag in enumerate(c_tag.findall('v')):
                v_num = v_tag.get('n', str(k + 1))
                vers_node = doc.createElement("VERS")
                vers_node.setAttribute("vnumber", v_num)
                # Plain text content
                verse_text = v_tag.text if v_tag.text else ""
                vers_node.appendChild(doc.createTextNode(verse_text))
                chap_node.appendChild(vers_node)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(doc.toprettyxml(indent="  "))
    print(f"Created: {output_file}")

if __name__ == "__main__":
    if os.path.exists("Myanmar Bible.xml"):
        process_myanmar("Myanmar Bible.xml", "Myanmar_Bible_Clean_v5.xml")
    
    if os.path.exists("Hakha Bible_(HCL).xml"):
        process_hakha("Hakha Bible_(HCL).xml", "Hakha_Bible_Clean_v5.xml")