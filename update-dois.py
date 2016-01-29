from mendeley import Mendeley
import yaml
import ads

with open('config.yml') as f:
    config = yaml.load(f)

ads.config.token = config['adsToken']

mendeley = Mendeley(config['clientId'], config['clientSecret'], 'http://localhost:5000/oauth')

auth = mendeley.start_authorization_code_flow()

print auth.get_login_url()

authorization_response = raw_input('Enter the full callback URL: ')

mendeley_session = auth.authenticate(authorization_response)

docs = mendeley_session.documents.iter()

for d in docs:


   # find all documents that have an arXiv id but not a DOI

    if d.identifiers is None:
        print "No identifiers found!"
        # docs.pop(d)
    else:

        if 'arxiv' not in d.identifiers:
            print "No arXiv found!"

        else:
            arxiv = d.identifiers['arxiv']

            if arxiv is not None:

                print "Found",arxiv

                # doi = d.identifiers['doi']
                if 'doi' not in d.identifiers:

                    print d.title
                    print d.identifiers

                    # look up the DOI using the arXiv id in ADS
                    # papers = list(ads.SearchQuery(arxiv = arxiv))
                    # print papers[0].author
                else:
                    print "DOI not None"
            else:
                print "arXiv is not NONE", arxiv
                # update the mendeley document with the doi