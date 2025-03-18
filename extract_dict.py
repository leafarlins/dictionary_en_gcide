from bs4 import BeautifulSoup
import json

def parse_gcide(file_path,output_path):
    with open(file_path, 'r', encoding='us-ascii',errors='replace') as file:
        content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(content, 'html.parser')
    entries = soup.find_all('p')

    results = []

    current_entry = None
    current_definition = None
    examples = []
    syn = None
    definitions = []
    cs = None
    syn = None

    for p_tag in entries:
        ent_tag = p_tag.find('ent')  # Check for a new <ent> tag
        if ent_tag:
            # Save the current entry before starting a new one
            print("Tag: ent")
            if current_entry:
                if current_definition:
                    current_definition['examples'] = examples
                    definitions.append(current_definition)
                pos = {
                    'etymology': ety,
                    'part_of_speech': pos,
                    'definitions': definitions
                }
                if cs:
                    pos['cs'] = cs
                    cs = None
                if syn:
                    pos['syn'] = syn
                    syn = None
                results.append({
                    'entry': current_entry.lower(),
                    'pos': [pos]})
                #print(f"writing definition: {definitions}")
            # Start a new entry
            current_entry = ent_tag.text.strip()
            print(f"Entrie: {current_entry}")
            pos = p_tag.find_next('pos').text if p_tag.find_next('pos') else ""
            ety = p_tag.find_next('ety').text if p_tag.find_next('ety') else None
            definitions = []  # Reset definitions for the new entry
            current_definition = None

        # Search def tag
        def_tag = p_tag.find('def')
        q_tag = p_tag.find('q')
        if def_tag:
            print("Tag: def")
            # Find sense number if it exists
            #sense_number_tag = def_tag.find_previous('sn')
            #sense_number = sense_number_tag.text.strip() if sense_number_tag else None

            # Extract definition text
            definition_text = def_tag.text.strip()

            # Append the definition
            if current_definition:
                current_definition['examples'] = examples
                definitions.append(current_definition)

            examples = []
            current_definition = {
                'text': definition_text
            }
                
        elif q_tag:
            print("Tag: q")
            q_text = q_tag.text.strip()
            examples.append(q_text)
        else:
            cs_tag = p_tag.find('cs')
            syn_tag = p_tag.find('syn')
            if cs_tag:
                cs = cs_tag.text.strip()
            elif syn_tag:
                syn = syn_tag.text.strip()
            else:
                print("Tag: NOT FOUND -> ",p_tag)

    # Append the last entry after the loop
    if current_entry:
        if current_definition:
            current_definition['examples'] = examples
            definitions.append(current_definition)
        pos = {
            'etymology': ety,
            'part_of_speech': pos,
            'definitions': definitions
        }
        if cs:
            pos['cs'] = cs
        if syn:
            pos['syn'] = syn
        results.append({
            'entry': current_entry.lower(),
            'pos': [pos]})

    # Merge entries
    final_results = {}
    print("Merging final dict")
    for entry in results:
        word = entry['entry']
        pos_list = entry["pos"]
        if word in final_results:
            final_results[word]['pos'].extend(pos_list)
        else:
            final_results[word] = entry


    # Write entries to the JSON file
    #print(results)
    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(final_results, outfile, ensure_ascii=False, indent=2)

    print(f"Parsed {len(results)} entries and saved to {output_path}")

# Example usage
letras = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
for letra in letras:
    file_path = './data/gcide-0.53/CIDE.'+letra
    output_path = './dictionary/data/en/words_'+letra+'.json'
    parse_gcide(file_path, output_path)

