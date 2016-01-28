from mendeley import Mendeley
import yaml

with open('config.yml') as f:
    config = yaml.load(f)

mendeley = Mendeley(config['clientId'], config['clientSecret'], 'http://localhost:5000/oauth')

auth = mendeley.start_authorization_code_flow()

print auth.get_login_url()

authorization_response = raw_input('Enter the full callback URL: ')

mendeley_session = auth.authenticate(authorization_response)

docs = mendeley_session.documents.list(view='client').items

for d in docs:
    print d.title