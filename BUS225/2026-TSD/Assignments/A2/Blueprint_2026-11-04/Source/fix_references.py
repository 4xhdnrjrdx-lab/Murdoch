"""Apply only the three reference corrections approved on 4 November 2026."""
from pathlib import Path
from zipfile import ZipFile
from hashlib import sha256
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
source = ROOT / 'BUS225_A2_Group9_Carrefour_Updated.docx'
target = ROOT / 'BUS225_A2_Group9_Carrefour_ReferencesFixed.docx'
replacements = [
    ('(Carrefour Group, n.d.)', '(Carrefour Group, 2017)'),
    ('Carrefour Group. (n.d.).', 'Carrefour Group. (2017, March 31).'),
    ('Great moments for everyone, everyday: ESG report 2021.',
     'ESG report 2021: Dare together.'),
]
with ZipFile(source) as original:
    document = original.read('word/document.xml').decode('utf-8')
    before = document
    for old, new in replacements:
        assert document.count(old) == 1, (old, document.count(old))
        document = document.replace(old, new)
    ET.fromstring(document)
    with ZipFile(target, 'w') as corrected:
        for info in original.infolist():
            corrected.writestr(info, document.encode('utf-8') if info.filename == 'word/document.xml'
                              else original.read(info.filename))
with ZipFile(source) as original, ZipFile(target) as corrected:
    assert original.namelist() == corrected.namelist()
    changed_parts = [name for name in original.namelist()
                     if original.read(name) != corrected.read(name)]
    assert changed_parts == ['word/document.xml'], changed_parts
    for name in original.namelist():
        if name.startswith('word/media/'):
            assert original.read(name) == corrected.read(name)
    # Reversing the approved replacements must reproduce the complete original
    # XML byte-for-byte, including formatting and all unchanged text.
    reversed_xml = document
    for old, new in replacements:
        assert reversed_xml.count(new) == 1
        reversed_xml = reversed_xml.replace(new, old)
    assert reversed_xml == before

check = {
    'date': '2026-11-04',
    'scope': 'Only the user-approved Pepper date, corresponding in-text citation and MAF report title.',
    'source': source.name,
    'output': target.name,
    'replacements': [{'before': old, 'after': new} for old, new in replacements],
    'changed_ooxml_parts': changed_parts,
    'all_other_ooxml_parts_identical': True,
    'blueprint_image_unchanged': True,
    'reverse_replacement_restores_original_document_xml': True,
    'original_docx_sha256': sha256(source.read_bytes()).hexdigest(),
    'corrected_docx_sha256': sha256(target.read_bytes()).hexdigest(),
}
(ROOT / 'Checks_ReferencesFixed.json').write_text(json.dumps(check, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(check, ensure_ascii=False, indent=2))
