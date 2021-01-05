import boto3
import os

def gen_subfolders(top):
  subfolders = os.walk(top)
  first_folder = next(subfolders)
  for curdir, _, _ in subfolders:
    yield curdir


def get_cert_list(cert_path) :
  # curr_dir = os.chdir(cert_path)
  return  [os.path.join(cert_path, cer) for cer in os.listdir(cert_path)]


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

    if  certpath.endswith('.key') :
      with open(certpath, 'r') as f:
        pvt_key = f.read().encode()
        if cert_dict.get('pvt_key', 0)  == 0 and type(pvt_key) is bytes:
          cert_dict['pvt_key'] = pvt_key

  return cert_dict

session = boto3.Session()
acm_client = session.client('acm')

cert_path = r'C:\Users\sarun\Desktop\GP2-Demo1'

for i in gen_subfolders(cert_path):
  cert_list = get_cert_list(i)
  cert_dict = process_cert(cert_list)
  # print(cert_dict)
  response = acm_client.import_certificate(
    Certificate=cert_dict['cert'],
    PrivateKey=cert_dict['pvt_key'],
    CertificateChain=cert_dict['chain'],
)
  print(response)
