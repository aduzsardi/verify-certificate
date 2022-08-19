#!/usr/bin/env python3
import datetime
import jinja2
import json
import requests
import socket
import ssl
from dateutil import parser


# Add hosts in this list in pair of ('host', port)
HOSTS = [
    ('google.com', 443),
    ('facebook.com', 443)
]

SLACK_WEBHOOK = None
DAYS_BEFORE_WARNING = 30


def get_certificate_info(host, port):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = True
    context.load_default_certs()
    socket.setdefaulttimeout(2.0)
    error = None
    certificate_info = None
    try:
        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock=sock, server_hostname=host) as ssock:
                    certificate_info = ssock.getpeercert(binary_form=False)
    except socket.gaierror:
            error = f'Hostname {host} can\'t be resolved'
    except socket.timeout:
            error = f'Connection timed out to {host}:{port}'
    except ssl.SSLCertVerificationError as e:
            error = '{0} for {1}'.format(e.verify_message.capitalize(), host)
    return (error, certificate_info)


def certificate_valid_date(certificate_info, validity):
    if validity in certificate_info:
        return certificate_info[validity]
    return


def certificate_valid_days(certificate_validity):
    validity_datetime = parser.parse(certificate_validity)
    now_datetime = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    diff_days = (validity_datetime - now_datetime).days
    return diff_days


def send_slack_message(**kwargs):
    if SLACK_WEBHOOK:
        jinja_loader = jinja2.FileSystemLoader(searchpath="./")
        jinja_env = jinja2.Environment(loader=jinja_loader)
        json_template = jinja_env.get_template('slack_payload.json.j2')
        json_template_rendered = json_template.render(**kwargs)
        return requests.post(SLACK_WEBHOOK, json.dumps(json.loads(json_template_rendered)))
    return


def main():
    for sslhost in HOSTS:
        host , port = sslhost
        err, info = get_certificate_info(host,port)
        if info is not None:
            certificate_valid_not_after = certificate_valid_date(info, 'notAfter')
            certificate_days =  certificate_valid_days(certificate_valid_not_after)
            if certificate_days <= DAYS_BEFORE_WARNING:
                send_slack_message(timestamp=datetime.datetime.now().timestamp(), domain=host, days=certificate_days, msg="Domain certificate is about to expire")
        elif err is not None:
            send_slack_message(timestamp=datetime.datetime.now().timestamp(), error_msg=True, msg=err)


if __name__ == '__main__':
    main()
