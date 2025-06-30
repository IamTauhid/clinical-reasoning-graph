import spacy
from scispacy.umls_linking import UmlsEntityLinker

def get_nlp_model():
    nlp = spacy.load("en_core_sci_md")
    linker = UmlsEntityLinker(resolve_abbreviations=True)
    nlp.add_pipe("umls_entity_linker")
    return nlp

def extract_concepts_and_relations(nlp, notes):
    concepts = []
    relations = []
    
    for note in notes:
        doc = nlp(note)
        for ent in doc.ents:
            if ent._.umls_ents:
                cui, score = ent._.umls_ents[0]
                concept_type = 'Symptom' if 'C0234450' in cui or 'C0242209' in cui else 'Finding' if 'C1293004' in cui else 'Diagnosis'
                concepts.append((ent.text, cui, concept_type, score))

        for sent in doc.sents:
            entities = [(ent.text, ent._.umls_ents[0][0]) for ent in sent.ents if ent._.umls_ents]
            for i in range(len(entities)):
                for j in range(i + 1, len(entities)):
                    weight = (entities[i][1][1] + entities[j][1][1]) / 2
                    relations.append((entities[i][0], entities[j][0], weight))
    
    return concepts, relations
