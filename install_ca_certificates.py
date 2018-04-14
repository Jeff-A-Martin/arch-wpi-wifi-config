# This file is used install CA certificates.
# The commands and conventions used are based off of the Arch Wiki documentation.
#
# Jeff Martin - jamartin@wpi.edu
# April 12, 2018

import os


def install_ca_certificates(status, public_cert_file, private_cert_file):
    log_status(status, "Installing WPI Wireless Certificates:")
    log_status(status, "\tInstalling Public Certificate...")
    success, pub_cert = install_public_certificate(public_cert_file)
    if not success:
        log_status(status, "\tFailed to install public certificate.")
        return False
    log_status(status, "\tInstalling Private Certificate...")
    success, priv_cert = install_private_certificate(private_cert_file)
    if not success:
        log_status(status, "\tFailed to install public certificate.")
        return False
    log_status(status, "\tCleaning Directory...")
    success = clean_directory(public_cert_file, private_cert_file)
    if not success:
        log_status(status, "\tFailed to clean directory.")
        return False
    log_status(status, "\tSuccess!")
    return True, pub_cert, priv_cert


def log_status(status, message):
    if status:
        print "[STATUS] " + message


def get_certificate_files():
    public_cert_file = raw_input("Enter the file path of the public certificate. ")
    private_cert_file = raw_input("Enter the file path of the private certificate. ")
    return public_cert_file, private_cert_file


def install_public_certificate(public_cert_file):
    cert_clean = clean_file_name(public_cert_file) + ".crt"
    installed_pub_cert = "/etc/ca-certificates/trust-source/anchors/" + cert_clean
    if (os.system("sudo mkdir -p /etc/ca-certificates/trust-source/anchors/")
            or os.system("sudo cp " + public_cert_file + " " + installed_pub_cert)
            or os.system("sudo trust extract-compat")):
        return False, ""
    else:
        extracted_public_cert = "/etc/ca-certificates/extracted/cadir/WPI_NetOps_Wireless_CA.pem"
        return True, extracted_public_cert


def install_private_certificate(private_cert_file):
    cert_clean = clean_file_name(private_cert_file) + ".crt"
    installed_priv_cert = "/etc/ca-certificates/private/" + cert_clean
    if (os.system("sudo mkdir -p /etc/ca-certificates/private/")
            or os.system("sudo cp " + private_cert_file + " " + installed_priv_cert)):
        return False, ""
    else:
        return True, installed_priv_cert


def clean_file_name(file_path):
    return (file_path.split("/")[-1]).split(".")[0]


def clean_directory(public_cert_file, private_cert_file):
    if os.system("rm " + public_cert_file) or os.system("rm " + private_cert_file):
        return False
    else:
        return True
