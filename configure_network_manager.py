# This file is used configure a Network Manager Profile for wpi-wireless & eduroam
# Network Manager is configured as described on the Arch Wiki to meet WPI's specifications
# as described at https://wpi-wireless-setup.wpi.edu/enroll/start under 'other operating systems'.
#
# Jeff Martin - jamartin@wpi.edu
# April 12, 2018

import subprocess
import os


def configure_network_manager(status, username, password, private_cert, public_cert):
    log_status(status, "Configuring Network Manager Profiles:")
    log_status(status, "\tGenerating WiFi profiles for WPI-Wireless and eduroam...")
    wpi_wireless_profile, eduroam_profile = generate_profiles(username, password, private_cert, public_cert)
    log_status(status, "\tInstalling WiFi profiles...")
    success = install_profiles(wpi_wireless_profile, eduroam_profile)
    if not success:
        log_status(status, "\tFailed to install profiles")
        return False
    log_status(status, "\tSuccess!")
    return True


def log_status(status, message):
    if status:
        print "[STATUS] " + message


def get_certificate_files():
    public_cert_file = raw_input("Enter the file path of the installed public certificate. ")
    private_cert_file = raw_input("Enter the file path of the installed private certificate. ")
    return public_cert_file, private_cert_file


def generate_profiles(username, password, public_cert, private_cert):
    wpi_wireless_profile = build_profile("wpi-wireless", generate_uuid(), "wifi", get_wifi_interface(),
                                         get_mac_address(), "WPI-Wireless", "wpa-eap", public_cert, private_cert,
                                         "tls;", str(username) + "@wpi.edu", private_cert, password)
    eduroam_profile = build_profile("eduroam", generate_uuid(), "wifi", get_wifi_interface(), get_mac_address(),
                                    "eduroam", "wpa-eap", public_cert, private_cert,
                                    "tls;", str(username) + "@wpi.edu", private_cert, password)
    return wpi_wireless_profile, eduroam_profile


def install_profiles(wpi_wireless_profile, eduroam_profile):
    cmd1 = ("echo '" + wpi_wireless_profile +
           "' | sudo tee /etc/NetworkManager/system-connections/wpi-wireless > /dev/null")
    cmd2 = ("echo '" + eduroam_profile +
           "' | sudo tee /etc/NetworkManager/system-connections/eduroam > /dev/null")
    cmd3 = "sudo chmod 600 /etc/NetworkManager/system-connections/wpi-wireless"
    cmd4 = "sudo chmod 600 /etc/NetworkManager/system-connections/eduroam"
    if os.system(cmd1) or os.system(cmd2) or os.system(cmd3) or os.system(cmd4):
        return False
    else:
        return True


def generate_uuid():
    return subprocess.check_output(['uuidgen']).strip()


def get_wifi_interface():
    interfaces = subprocess.check_output(['ip', 'link'])
    interface_list = interfaces.split("\n")
    count = 0
    for interface in interface_list:
        count += 1
        fragments = interface.split(':')
        if count % 2 == 0 or len(fragments) < 2:
            continue
        fragment = fragments[1].strip()
        if fragment.lower()[0] == 'w':
            return fragment
    return "None"


def get_mac_address():
    interfaces = subprocess.check_output(['ip', 'link'])
    interface_list = interfaces.split("\n")
    count = 0
    index = -1
    for interface in interface_list:
        count += 1
        fragments = interface.split(':')
        if count % 2 == 0 or len(fragments) < 2:
            continue
        fragment = fragments[1].strip()
        if fragment.lower()[0] == 'w':
            index = count
    if index == -1 or len(interface_list) <= index:
        return "None"
    else:
        return interface_list[index].split(' ')[-3].upper()


def build_profile(id_code, uuid, dev_type, interface_name, mac_address, ssid, key_mgmt, ca_cert, client_cert, eap,
                  identity, private_key, private_key_password):
    profile = "[connection]\n"
    profile += "id=" + str(id_code) + "\n"
    profile += "uuid=" + str(uuid) + "\n"
    profile += "type=" + str(dev_type) + "\n"
    profile += "interface-name=" + str(interface_name) + "\n"
    profile += "\n"
    profile += "[wifi]\n"
    profile += "mac-address=" + str(mac_address) + "\n"
    profile += "ssid=" + str(ssid) + "\n"
    profile += "\n"
    profile += "[wifi-security]\n"
    profile += "key-mgmt=" + str(key_mgmt) + "\n"
    profile += "\n"
    profile += "[802-1x]\n"
    profile += "ca-cert=" + str(ca_cert) + "\n"
    profile += "client-cert=" + str(client_cert) + "\n"
    profile += "eap=" + str(eap) + "\n"
    profile += "identity=" + str(identity) + "\n"
    profile += "private-key=" + str(private_key) + "\n"
    profile += "private-key-password=" + str(private_key_password) + "\n"
    return profile
