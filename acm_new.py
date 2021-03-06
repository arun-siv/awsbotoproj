import boto3
import os
import re

def gen_subfolders(top):
  subfolders = os.walk(top)
  first_folder = next(subfolders) # root / top folder ---> skip this
  for curdir, _, _ in subfolders:
    yield curdir


def get_cert_list(cert_path) :
  return  [os.path.join(cert_path, cer) for cer in os.listdir(cert_path)]


def get_domains_from_acm(acm) :
  cert_domains = {}
# List certificates with the pagination interface
  paginator = acm.get_paginator('list_certificates')
  for response in paginator.paginate():
      for certificate in response['CertificateSummaryList']:
          if cert_domains.get(certificate['DomainName']) is None :
            cert_domains[certificate['DomainName']] = certificate['CertificateArn']
          else :
            cert_domains.update({certificate['DomainName']:certificate['CertificateArn']})
  return cert_domains

def get_domain_from_filepath(dirpath) :
  # patt = '((www\.)?\w+\D+)\.\w+\.[a-zA-Z]+'
  patt = '((www\.)?\w+(\-)?(\w+)?)\.\w+\.[a-zA-Z]+'
  if re.search(patt, dirpath) :
    return re.search(patt, dirpath).group()
  return None


def process_cert(certs_array) :
  cert_dict = {}
  for certpath in certs_array :

    if certpath.endswith('.crt') and 'interm' in certpath  :
      with open(certpath, 'r') as f:
        chain = f.read().encode()
        if cert_dict.get('chain', 0)  == 0 and type(chain) is bytes:
          cert_dict['chain'] = chain

    if  certpath.endswith('.crt') and 'interm' not in certpath:
      with open(certpath , 'r') as f:
        cert = f.read().encode()
        if cert_dict.get('cert', 0)  == 0 and type(cert) is bytes:
          cert_dict['cert'] = cert

      domain_name = get_domain_from_filepath(certpath)
      cert_dict['domain'] = domain_name

    if  certpath.endswith('.key') :
      with open(certpath, 'r') as f:
        pvt_key = f.read().encode()
        if cert_dict.get('pvt_key', 0)  == 0 and type(pvt_key) is bytes:
          cert_dict['pvt_key'] = pvt_key

  return cert_dict

session = boto3.Session()

acm_client = session.client('acm')

cert_path = r'C:\Users\sarun\Desktop\GP2-Demo1'

acm_domains = get_domains_from_acm(acm_client)

for i in gen_subfolders(cert_path):
  cert_list = get_cert_list(i)
  cert_dict = process_cert(cert_list)

  if acm_domains.get(cert_dict['domain']) is not None:

  # print(cert_dict)
    response = acm_client.import_certificate (
      CertificateArn=acm_domains[cert_dict['domain']],
      Certificate=cert_dict['cert'],
      PrivateKey=cert_dict['pvt_key'],
      CertificateChain=cert_dict['chain']
      )
    print(response)

  elif acm_domains.get(cert_dict['domain']) is None:
    response = acm_client.import_certificate (
      Certificate=cert_dict['cert'],
      PrivateKey=cert_dict['pvt_key'],
      CertificateChain=cert_dict['chain']
      )
    print(response)
