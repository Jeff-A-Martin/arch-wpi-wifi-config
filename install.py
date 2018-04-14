# This file is used configure a Network Manager Profile for wpi-wireless & eduroam
# Network Manager is configured as described on the Arch Wiki to meet WPI's specifications
# as described at https://wpi-wireless-setup.wpi.edu/enroll/start under 'other operating systems'.
#
# Jeff Martin - jamartin@wpi.edu
# April 12, 2018

import getpass
import get_wpi_certs
import install_ca_certificates
import configure_network_manager


def main():
    username, password = get_user_credentials()
    accepted = accept_use_policy_query(get_wpi_certs.WPI_ACCEPTABLE_USE_POLICY)
    public_cert_file = "WPI_PUBLIC_CA_CERTIFICATE"
    private_cert_file = username.upper() + "_WPI_PRIVATE_CA_CERTIFICATE"
    result = get_wpi_certs.get_wpi_certs(username, password, accepted, public_cert_file, private_cert_file, True)
    if not result:
        exit(1)
    result, installed_public_cert, installed_private_cert = \
        install_ca_certificates.install_ca_certificates(True, public_cert_file, private_cert_file)
    if not result:
        exit(1)
    result = configure_network_manager.configure_network_manager(True, username, password, installed_public_cert,
                                                                 installed_private_cert)
    if not result:
        exit(1)


def get_user_credentials():
    username = raw_input("Enter Your WPI Username: ")
    password = getpass.getpass("Enter Your WPI Password: ")
    return username, password


def accept_use_policy_query(terms_url):
    print "Please review the acceptable use policy for WPIs network before proceeding:"
    print terms_url
    accepted = raw_input("Do you agree to abide by these guidelines? [Y/N]: ")
    return accepted.lower()[0] == "y"


if __name__ == "__main__":
    main()
