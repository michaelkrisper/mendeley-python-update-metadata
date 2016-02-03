from mendeley import Mendeley
import yaml
import ads
import re

import pickle

with open('config.yml') as f:
    config = yaml.load(f)

ads.config.token = config['adsToken']

mendeley = Mendeley(config['clientId'], config['clientSecret'], 'http://localhost:5000/oauth')

docs_without_doi = None
docs_without_arxiv = None

def use_login():

    # auth = mendeley.start_authorization_code_flow()
    #
    # print auth.get_login_url()
    #
    # authorization_response = raw_input('Enter the full callback URL: ')
    #
    # mendeley_session = auth.authenticate(authorization_response)
    #
    # docs = [d for d in mendeley_session.documents.iter()]

    # global docs_without_doi
    # global docs_without_arxiv
    # global docs_without_doi_but_with_arxiv
    global  docs_without_arxiv_but_with_doi

    docs = pickle.load(open("dump"))

    # docs_without_doi = filter(lambda d: d.identifiers and 'doi' not in d.identifiers, docs)
    # docs_without_arxiv = filter(lambda d: d.identifiers and 'arxiv' not in d.identifiers, docs)
    # docs_without_doi_but_with_arxiv = filter(lambda d: d.identifiers and 'doi' not in d.identifiers and 'arxiv' in d.identifiers, docs)
    docs_without_arxiv_but_with_doi = filter(lambda d: d.identifiers and 'arxiv' not in d.identifiers and 'doi' in d.identifiers, docs)

    print docs_without_arxiv_but_with_doi

    # pickle.dump(docs, open("dump", "wb"))


def find_docs_without_arxiv():

    # a list with all documents that have no doi so query by arxiv
    for doc_without_arxiv in docs_without_arxiv_but_with_doi:
        if 'arxiv' in doc_without_arxiv.identifiers:
            print "This should not happen", doc_without_arxiv.identifiers
        if 'doi' in doc_without_arxiv.identifiers:

            papers = list(ads.SearchQuery(doi=doc_without_arxiv.identifiers['doi'],
                                          fl='first_author, bibcode, identifier, abstract, year, volume, pub, issue, page, keyword'))

            if len(papers) > 1:
                print "Multiple matching papers!"

            else:
                if len(papers) != 0:
                    print papers[0].title
                    update_arxiv_in_mendeley(papers, doc_without_arxiv)


def update_arxiv_in_mendeley(papers, doc_without_arxiv):

    ads_papers_with_arxiv = filter(lambda d: d.identifier and 'arxiv' in d.identifier, papers)

    if len(ads_papers_with_arxiv) > 1:
                print "FOUND AN EXAMPLE", ads_papers_with_arxiv


    # print papers[0].identifier
    # for identifier in papers[0].identifier:
    #     if 'arxiv' in identifier and doc_without_arxiv.identifiers['arxiv'] == None:
    #         print 'Update Mendeley from ADS ', identifier['arxiv']


def find_docs_without_doi():

    # a list with all documents that have no doi, query by arxiv
    for doc_without_doi in docs_without_doi:
        if 'doi' in doc_without_doi.identifiers:
            print "This should not happen", doc_without_doi.identifiers
        if 'arxiv' in doc_without_doi.identifiers:

            papers = list(ads.SearchQuery(arXiv=doc_without_doi.identifiers['arxiv'],fl='first_author, bibcode, identifier, abstract, year, volume, pub, issue, page, keyword'))
            if len(papers) > 1:
                print "Multiple matching papers!"
            else:
                if len(papers) != 0:
                    print papers[0].title
                    update_doi_in_mendeley(papers, doc_without_doi)


def update_doi_in_mendeley(papers, doc_without_doi):
    for identifier in papers[0].identifier:
        if 'doi' in identifier and doc_without_doi.identifiers['doi'] == None:
            print 'Update Mendeley from ADS ', identifier['doi']





def regex_checker(identifier):
    doi_regex = '/^10.\d{4,9}/[-._;()/:A-Z0-9]+$/i'
    m = re.search(doi_regex, identifier)

    if identifier.startswith('10.'):
        try: m.group(0)
        except Exception as e : print "REGEX ERROR:", e;
    else:
        print "Was not a DOI ", identifier


if __name__ == "__main__":
    use_login()
    # find_docs_without_doi()
    find_docs_without_arxiv()


#         print "Document  before " , d.identifiers

        # updated_document = document.update(identifiers=document.identifiers.update({'item3': 3}))
        #
        # print "Document  after " , updated_document.identifiers
        #
        # patched_document = mendeley_session.documents.get(updated_document.id)
        #
        # print "PATCHED   " , patched_document.identifiers




