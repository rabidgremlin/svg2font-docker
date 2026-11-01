import fontforge

def create_font_from_svgs(svg_list, output_filename="my_custom_font"):
    # 1. Create a new font object
    font = fontforge.font()
    
    # 2. Set metadata
    font.fontname = "MyCustomFont"
    font.fullname = "My Custom Font"
    font.familyname = "My Custom Font"
    
    # 3. Map your SVGs to characters
    for character, svg_path in svg_list.items():
        # Create a slot for the character (accepts 'A', 'B', etc. or integers like 65)
        glyph = font.createChar(ord(character)) 
        
        # Import the vector outline
        glyph.importOutlines(svg_path)
        
        # Shift the glyph so its bottom bounding box sits perfectly on the baseline
        ymin = glyph.boundingBox()[1]
        glyph.transform([1, 0, 0, 1, 0, -ymin])
        
        # Set spacing padding (Side Bearings)
        glyph.left_side_bearing = 15
        glyph.right_side_bearing = 15

    # 4. Generate your font formats
    font.generate(f"{output_filename}.ttf")
    font.generate(f"{output_filename}.otf")
    print(f"Font successfully created: {output_filename}.ttf/.otf")

# Example Usage:
# Mapping characters to their corresponding SVG file paths
svg_mapping = {
    'A': 'example/A_CrossPattéeFitchée.svg',
    'C': 'example/C_dice-solid-full.svg'
}

create_font_from_svgs(svg_mapping)

