import json
from requests.exceptions import ConnectionError
from schema import Schema, And, Use, Optional
import requests
from os.path import expanduser
import os

vul_schema = Schema(
    {
        'name': str,
        'tool': str,
        'description': str,
        'project': str,
        'target': str,
        'scan': str,
        Optional('cwe'): And(Use(int)),
        Optional('observation'): str,
        Optional('severity'): And(Use(int), lambda n: 0 <= n <= 3),
        Optional('remediation'): str,
        Optional('evidences'): list
    },
    ignore_extra_keys=False
)

evidence_schema = Schema(
    {
        'name': str,
        'url': str,
        'vulnId': str,
        Optional('param'): str,
        Optional('log'): str,
        Optional('attack'): str,
        Optional('otherInfo'): str,
        Optional('evidence'): str,
        Optional('data'): str
    },
    ignore_extra_keys=False
)


def threatplaybook_con(threatplaybook):
    """
    :param threatplaybook: URL of ThreatPlaybook API Server.
    :return: If Connection to http://threat-playbook/graph is successful, returns True.
    """
    try:
        r = requests.get(url='{}/graph'.format(threatplaybook))
        if r.status_code == 200:
            return True
        else:
            return False
    except ConnectionError:
        return False


def config_file():
    """
    Creates a ThreatPlaybook config file to store Authorization Token
    :return: Path of config file
    """
    # directory = expanduser(path='~/.threatplaybook')
    config_file_path = 'config'
    open(config_file_path,'a').close()
    return config_file_path


def clean_string(string):
    """
    Cleans the string before creating a GraphQL query. `\n`, `\\`, `\r`, etc.. cause issues.
    :param string: String that needs to be formatted
    :return: Formatted string compatible with GraphQL Query.
    """
    cleaned_string = str(string).replace("\n", " ").replace('"', " ").replace("\\", '').replace("\r", "")
    return cleaned_string


def _post_req(url, email, password):
    """
    Posts non-graphql requests to ThreatPlaybook API Server. Currently used for:
        * Create User
        * Login
    :param url: ThreatPlaybook API URL
    :param email: E-mail of the User
    :param password: Password set by the User
    :return: Returns with response
    """
    headers = {'content-type': 'application/json'}
    auth = {"email": email, "password": password}
    try:
        r = requests.post(url=url, headers=headers, data=json.dumps(auth))
        if r.status_code == 500:
            return {'error': 'Server Error'}
        return r.json()
    except ConnectionError:
        return {'error': 'Unable to contact Threatplaybook API server'}


def _post_query(**kwargs):
    """
    Posts GraphQL requests to ThreatPlaybook API Server.
    :param threatplaybook: URL of ThreatPlaybook API Server
    :param token: authorization token
    :param query: GraphQL Query
    :return: Returns with response
    """
    threatplaybook = kwargs.get('threatplaybook')
    token = kwargs.get('token')
    query = kwargs.get('query')
    url = '{}/graph'.format(threatplaybook)
    if token:
        headers = {'content-type': 'application/json', 'authorization': token}
        try:
            r = requests.post(url=url, json={'query': query}, headers=headers)
            return r.json()
        except Exception as e:
            return {'error': e.message}
    else:
        return {'error': 'Token not found in config file'}


def create_scan(target):
    """
    Creates CreateScan mutation query
    :param target: Target name
    :return: CreateScan mutation query
    """
    create_scan_query = """
        mutation {
          createScan(target: "%s") {
            scan {
              name
              createdOn
            }
          }
        }
        """ % target
    return create_scan_query


def create_evidence(evidence):
    """
    Validates evidence dictionary and creates CreateVulnerabilityEvidence mutation query
    :param evidence: Evidence dictionary of a Vulnerability
    :return: CreateVulnerabilityEvidence mutation query
    """
    valid_evidence = evidence_schema.validate(evidence)
    create_evidence_query = """
        mutation {
          createVulnerabilityEvidence(
            evidence: {
              name: "%s"
              log: "%s"
              data: "%s"
              url: "%s"
              param: "%s"
              attack: "%s"
              evidence: "%s"
              otherInfo: "%s"
              vulnId: "%s"
              })
            {
              vulnEvidence {
                name
                }
            }
        } 
    """ % (valid_evidence.get('name', 'Unknown'),
           valid_evidence.get('log'),
           valid_evidence.get('data'),
           valid_evidence.get('url'),
           valid_evidence.get('param'),
           valid_evidence.get('attack'),
           valid_evidence.get('evidence'),
           valid_evidence.get('otherInfo'),
           valid_evidence.get('vulnId'))
    return create_evidence_query


def create_vulnerability(vul_dict):
    """
    Validates vulnerability dictionary and creates CreateVulnerability mutation query
    :param vul_dict: Vulnerability dictionary
    :return: CreateVulnerability mutation query
    """
    valid_vul = vul_schema.validate(vul_dict)
    create_vulnerability_query = """
            mutation {
              createVulnerability(
                vuln: {
                  name: "%s"
                  tool: "%s"
                  description: "%s"
                  project: "%s"
                  target: "%s"
                  scan: "%s"
                  cwe: %d
                  observation: "%s"
                  severity: %d
                  remediation: "%s"
                  })
                {
                  vulnerability {
                    name
                    id
                    }
                  }
                }
    """ % (valid_vul.get('name', 'Unknown'),
           valid_vul.get('tool'),
           valid_vul.get('description', ''),
           valid_vul.get('project'),
           valid_vul.get('target'),
           valid_vul.get('scan'),
           valid_vul.get('cwe', 0),
           valid_vul.get('observation', ''),
           valid_vul.get('severity', 0),
           valid_vul.get('remediation', ''),)
    return create_vulnerability_query
