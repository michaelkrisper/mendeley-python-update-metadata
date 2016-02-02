from mendeley import Mendeley
import yaml
import ads
import re

import pickle

with open('config.yml') as f:
    config = yaml.load(f)

ads.config.token = config['adsToken']

mendeley = Mendeley(config['clientId'], config['clientSecret'], 'http://localhost:5000/oauth')


def use_login():

    auth = mendeley.start_authorization_code_flow()

    print auth.get_login_url()

    authorization_response = raw_input('Enter the full callback URL: ')

    mendeley_session = auth.authenticate(authorization_response)

    docs = [d for d in mendeley_session.documents.iter()]

    pickle.dump(docs, open("dump", "wb"))




def find_docs_without_doi():
    docs = pickle.load(open("dump"))
    docs_without_doi = filter(lambda d: d.identifiers and 'doi' not in d.identifiers, docs)

    # a list with all documents that have no doi, query by arxiv
    for doc_without_doi in docs_without_doi:
        if 'doi' in doc_without_doi.identifiers:
            print "This should not happen", doc_without_doi.identifiers
        if 'arxiv' in doc_without_doi.identifiers:

            papers = list(ads.SearchQuery(arXiv=doc_without_doi.identifiers['arxiv'],fl='first_author, bibcode, identifier, abstract, year, volume, pub, issue, page, keyword'))
            if len(papers) < 1:
                print "No valid paper found!"
            elif len(papers) > 1:
                print "Multiple matching papers!"
            else:
                print papers[0].title


def find_docs_without_arxiv():
    docs = pickle.load(open("dump"))
    docs_without_arxiv = filter(lambda d: d.identifiers and 'arxiv' not in d.identifiers, docs)

    # a list with all documents that have no doi, query by arxiv
    for doc_without_arxiv in docs_without_arxiv:
        if 'arxiv' in doc_without_arxiv.identifiers:
            print "This should not happen", doc_without_arxiv.identifiers
        if 'doi' in doc_without_arxiv.identifiers:

            papers = list(ads.SearchQuery(doi=doc_without_arxiv.identifiers['doi'],
                                          fl='first_author, bibcode, identifier, abstract, year, volume, pub, issue, page, keyword'))
            if len(papers) < 1:
                print "No valid paper found!"
            elif len(papers) > 1:
                print "Multiple matching papers!"
            else:
                print papers[0].title



if __name__ == "__main__":
    find_docs_without_doi()
    find_docs_without_arxiv()


#         print "Document  before " , d.identifiers

        # updated_document = document.update(identifiers=document.identifiers.update({'item3': 3}))
        #
        # print "Document  after " , updated_document.identifiers
        #
        # patched_document = mendeley_session.documents.get(updated_document.id)
        #
        # print "PATCHED   " , patched_document.identifiers




