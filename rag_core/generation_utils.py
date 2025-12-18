import re

def extract_cited_chunk_ids(answer: str) -> set[int]:
    pattern = r"chunk_id\s*=\s*([\d,\s]+)"
    matches = re.findall(pattern, answer)

    cited_ids = set()
    for match in matches:
        for part in match.split(","):
            part = part.strip()
            if part.isdigit():
                cited_ids.add(int(part))

    return cited_ids