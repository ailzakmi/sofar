import json
import subprocess
# import socket
# import time
# import threading

import psutil
from platform import uname


port_list = []

def correct_size(bts, ending='iB'):
    size = 1024
    for item in ["", "K", "M", "G", "T", "P"]:
        if bts < size:
            return f"{bts:.2f}{item}{ending}"
        bts /= size

def creating_file():
    collect_info_dict = dict()
    if 'info' not in collect_info_dict:
        collect_info_dict['info'] = dict()
        collect_info_dict['info']['system_info'] = dict()
        collect_info_dict['info']['system_info'] = {'system': {'comp_name': uname().node,
                                                               'os_name': f"{uname().system} {uname().release}",
                                                               'version': uname().version,
                                                               'machine': uname().machine},
                                                    'processor': {'name': uname().processor,
                                                                  'phisycal_core': psutil.cpu_count(logical=False),
                                                                  'all_core': psutil.cpu_count(logical=True),
                                                                  'freq_max': f"{psutil.cpu_freq().max:.2f}Мгц"},
                                                    'ram': {'volume': correct_size(psutil.virtual_memory().total),
                                                            'aviable': correct_size(psutil.virtual_memory().available),
                                                            'used': correct_size(psutil.virtual_memory().used)}}

    for partition in psutil.disk_partitions():
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        if 'disk_info' not in collect_info_dict['info']:
            collect_info_dict['info']['disk_info'] = dict()
        if f"'device': {partition.device}" not in collect_info_dict['info']['disk_info']:
            collect_info_dict['info']['disk_info'][partition.device] = dict()
            collect_info_dict['info']['disk_info'][partition.device] = {'file_system': partition.fstype,
                                                                        'size_total': correct_size(
                                                                            partition_usage.total),
                                                                        'size_used': correct_size(
                                                                            partition_usage.used),
                                                                        'size_free': correct_size(
                                                                            partition_usage.free),
                                                                        'percent':
                                                                            f'{partition_usage.percent}'}

    for interface_name, interface_address in psutil.net_if_addrs().items():
        if interface_name == 'Loopback Pseudo-Interface 1':
            continue
        else:
            if 'net_info' not in collect_info_dict['info']:
                collect_info_dict['info']['net_info'] = dict()
            if interface_name not in collect_info_dict['info']['net_info']:
                collect_info_dict['info']['net_info'][interface_name] = dict()
                collect_info_dict['info']['net_info'][interface_name] = {
                    'mac': interface_address[0].address.replace("-", ":"),
                    'ipv4': interface_address[1].address,
                    'ipv6': interface_address[2].address}

    return collect_info_dict

def win_dop_info(dict_info):
    import windows_tools.product_key

    # motherboard
    manufacturer = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_BaseBoard).Manufacturer'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).strip()

    product = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_BaseBoard).Product'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).strip()

    # bios
    version_bios = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_BIOS).Version'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).strip()

    manufacturer_bios = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_BIOS).Manufacturer'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).strip()

    serial_num_bios = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_BIOS).SerialNumber'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).strip()

    date_version_bios = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_BIOS).Description'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).strip()

    smbios_ver = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_BIOS).SMBIOSBIOSVersion'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).strip()

    # boot configuration
    boot_directory = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_BootConfiguration).BootDirectory'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).strip()

    last_drive = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_BootConfiguration).LastDrive'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).strip()

    # processor info
    processor_name = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_Processor).Name'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).strip()

    processor_id = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_Processor).ProcessorId'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).strip()

    # system info from SMBIOS
    uuid_system = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_ComputerSystemProduct).UUID'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).strip()

    # monitor info
    pnpdeviceid = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_DesktopMonitor).PNPDeviceID'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).strip()

    if 'other_info' not in dict_info['info']:
        dict_info['info']['other_info'] = dict()
        dict_info['info']['other_info'] = {'motherboard_manufacturer': manufacturer,
                                           'motherboard_product': product,
                                           'version_bios': version_bios,
                                           'manufacturer_bios': manufacturer_bios,
                                           'serial_number_bios': serial_num_bios,
                                           'date_version_bios': date_version_bios,
                                           'smbios_version': smbios_ver,
                                           'os_boot_directory': boot_directory,
                                           'last_drive': last_drive,
                                           'processor_name': processor_name,
                                           'processor_id': processor_id,
                                           'uuid_system': uuid_system,
                                           'pnp_device_id': pnpdeviceid}

    # disk info
    disk_caption = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_DiskDrive).Caption'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).split("\n")
    d_list = []
    for cap in disk_caption:
        if '' != cap:
            cap += "\t"
            d_list.append(cap)
        
    serial_num_disk = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_DiskDrive).SerialNumber'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).split("\n")
    d_sn_list = []
    for ser in serial_num_disk:
        if '' != ser:
            d_sn_list.append(ser.strip())
       
    for num in range(0, len(d_list)):
        if (len(d_list)) != num:
            if 'drive_name_serial' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['drive_name_serial'] = dict()
            if d_list[num] not in dict_info['info']['other_info']['drive_name_serial']:
                dict_info['info']['other_info']['drive_name_serial'][d_list[num]] = dict()
                dict_info['info']['other_info']['drive_name_serial'][d_list[num]] = d_sn_list[num]

    firmvare_revision_disk = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_DiskDrive).FirmwareRevision'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).split("\n")
    for num, nf in enumerate(firmvare_revision_disk):
        if (len(firmvare_revision_disk)-1) != num:
            if 'drive_firmware' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['drive_firmware'] = dict()
            if f'drive_{num}' not in dict_info['info']['other_info']['drive_firmware']:
                dict_info['info']['other_info']['drive_firmware'][f'drive_{num}'] = dict()
                dict_info['info']['other_info']['drive_firmware'][f'drive_{num}'] = nf.strip()

    disk_signature = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_DiskDrive).Signature'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).split("\n")
    for num, sgl in enumerate(disk_signature):
        if (len(disk_signature)-1) != num:
            if 'disk_signature' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['disk_signature'] = dict()
            if f'sig_{num}' not in dict_info['info']['other_info']['disk_signature']:
                dict_info['info']['other_info']['disk_signature'][f'sig_{num}'] = sgl.strip()

    # volume disk info
    disk_volume_name = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_LogicalDisk).VolumeName'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).split("\n")
    for num, vln in enumerate(disk_volume_name):
        if (len(disk_volume_name)-1) != num:
            if 'volum_name' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['volum_name'] = dict()
            if f'volum_{num}' not in dict_info['info']['other_info']['volum_name']:
                dict_info['info']['other_info']['volum_name'][f'volum_{num}'] = dict()
                dict_info['info']['other_info']['volum_name'][f'volum_{num}'] = (vln if '' != vln else str('Drive')).strip()

    volume_serialnumber = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_LogicalDisk).VolumeSerialNumber'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).split("\n")
    
    for num, vsn in enumerate(volume_serialnumber):
        if (len(volume_serialnumber)-1) != num:
            if 'volume_serial_number' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['volume_serial_number'] = dict()
            if f'volume_serial_{num}' not in dict_info['info']['other_info']['volume_serial_number']:
                dict_info['info']['other_info']['volume_serial_number'][f'volume_serial_{num}'] = dict()
                dict_info['info']['other_info']['volume_serial_number'][f'volume_serial_{num}'] = vsn.strip()

    # ram info
    ram_form_factor = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_PhysicalMemory).FormFactor'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).split("\n")
    for num, ffm in enumerate(ram_form_factor):
        if (len(ram_form_factor)-1) != num:
            if 'memory_form_factor' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['memory_form_factor'] = dict()
            if f'memory_{num}' not in dict_info['info']['other_info']['memory_form_factor']:
                dict_info['info']['other_info']['memory_form_factor'][f'memory_{num}'] = dict()
                dict_info['info']['other_info']['memory_form_factor'][f'memory_{num}'] = ffm.strip()

    ram_bank_label = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_PhysicalMemory).BankLabel'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).split("\n")
    for num, ram_b in enumerate(ram_bank_label):
        if (len(ram_bank_label)-1) != num:
            if 'memory_bank_label' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['memory_bank_label'] = dict()
            if f'bank_label_{num}' not in dict_info['info']['other_info']['memory_bank_label']:
                dict_info['info']['other_info']['memory_bank_label'][f'bank_label_{num}'] = dict()
                dict_info['info']['other_info']['memory_bank_label'][f'bank_label_{num}'] = ram_b.strip()

    ram_device_locator = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_PhysicalMemory).DeviceLocator'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).split("\n")
    for num, ram_b in enumerate(ram_device_locator):
        if (len(ram_device_locator)-1) != num:
            if 'memory_device_locator' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['memory_device_locator'] = dict()
            if f'device_locator_{num}' not in dict_info['info']['other_info']['memory_device_locator']:
                dict_info['info']['other_info']['memory_device_locator'][f'device_locator_{num}'] = dict()
                dict_info['info']['other_info']['memory_device_locator'][f'device_locator_{num}'] = ram_b.strip()

    ram_memory_type = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_PhysicalMemory).SMBIOSMemoryType'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).split("\n")
    for num, ram_t in enumerate(ram_memory_type):
        if (len(ram_memory_type)-1) != num:
            match int(ram_t.strip()):
                case 20:
                    ram_t = "DDR1"
                case 21:
                    ram_t = "DDR2"
                case 24:
                    ram_t = "DDR3"
                case 26:
                    ram_t = "DDR4"
                case 27:
                    ram_t = "DDR5"
                case 34:
                    ram_t = "DDR5"
                case _:
                    ram_t = str(ram_t) + " неизвестная"
            if 'memory_type' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['memory_type'] = dict()
            if f'bank_{num}' not in dict_info['info']['other_info']['memory_type']:
                dict_info['info']['other_info']['memory_type'][f'bank_{num}'] = dict()
                dict_info['info']['other_info']['memory_type'][f'bank_{num}'] = ram_t

    ram_manufacturer = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_PhysicalMemory).Manufacturer'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).split("\n")
    for num, ram_m in enumerate(ram_manufacturer):
        if (len(ram_manufacturer)-1) != num:
            if 'memory_manufacturer' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['memory_manufacturer'] = dict()
            if f'manufacturer_{num}' not in dict_info['info']['other_info']['memory_manufacturer']:
                dict_info['info']['other_info']['memory_manufacturer'][f'manufacturer_{num}'] = dict()
                dict_info['info']['other_info']['memory_manufacturer'][f'manufacturer_{num}'] = ram_m.strip()

    ram_part_number = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_PhysicalMemory).PartNumber'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).split("\n")
    for num, rpn in enumerate(ram_part_number):
        if (len(ram_part_number)-1) != num:
            if 'memory_part_number' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['memory_part_number'] = dict()
            if f'part_number_{num}' not in dict_info['info']['other_info']['memory_part_number']:
                dict_info['info']['other_info']['memory_part_number'][f'part_number_{num}'] = dict()
                dict_info['info']['other_info']['memory_part_number'][f'part_number_{num}'] = rpn.strip()

    serial_number_ram = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_PhysicalMemory).SerialNumber'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).split("\n")
    for num, sn_ram in enumerate(serial_number_ram):
        if (len(serial_number_ram)-1) != num:
            if 'memory_serial_number' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['memory_serial_number'] = dict()
            if f'serial_number_{num}' not in dict_info['info']['other_info']['memory_serial_number']:
                dict_info['info']['other_info']['memory_serial_number'][f'serial_number_{num}'] = dict()
                dict_info['info']['other_info']['memory_serial_number'][f'serial_number_{num}'] = sn_ram.strip()

    ram_speed_frequency = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_PhysicalMemory).Speed'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).split("\n")
    for num, rsf in enumerate(ram_speed_frequency):
        if (len(ram_speed_frequency)-1) != num:
            if 'memory_frequency' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['memory_frequency'] = dict()
            if f'frequency_{num}' not in dict_info['info']['other_info']['memory_frequency']:
                dict_info['info']['other_info']['memory_frequency'][f'frequency_{num}'] = dict()
                dict_info['info']['other_info']['memory_frequency'][f'frequency_{num}'] = rsf.strip()

    ram_count_memory =  str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_PhysicalMemoryArray).MemoryDevices'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout)
    if 'count_memory' not in dict_info['info']['other_info']:
        dict_info['info']['other_info']['count_memory'] = dict()
        dict_info['info']['other_info']['count_memory'] = ram_count_memory.strip()

    # network adapter info
    caption_net_adapter = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_NetworkAdapter).Caption'], shell=False, capture_output=True, text=True, check=True, encoding='cp866', creationflags=subprocess.CREATE_NO_WINDOW).stdout).split("\n")
    for num, capnad in enumerate(caption_net_adapter):
        if (len(caption_net_adapter)-1) != num:
            if 'net_adapter_caption' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['net_adapter_caption'] = dict()
            if f'net_adapter_{num}' not in dict_info['info']['other_info']['net_adapter_caption']:
                dict_info['info']['other_info']['net_adapter_caption'][f'net_adapter_{num}'] = dict()
                dict_info['info']['other_info']['net_adapter_caption'][f'net_adapter_{num}'] = capnad.strip()

    guid_network_adapter = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_NetworkAdapter).GUID'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).split("\n")
    for num, guid in enumerate(guid_network_adapter):
            if (len(guid_network_adapter)-1) != num:
                if 'guid_net_adapter' not in dict_info['info']['other_info']:
                    dict_info['info']['other_info']['guid_net_adapter'] = dict()
                if f'guid_{num}' not in dict_info['info']['other_info']['guid_net_adapter']:
                    dict_info['info']['other_info']['guid_net_adapter'][f'guid_{num}'] = dict()
                    dict_info['info']['other_info']['guid_net_adapter'][f'guid_{num}'] = guid.strip()

    # os information
    os_install_date = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_OperatingSystem).InstallDate'], shell=False, capture_output=True, text=True, check=True, encoding='cp866', creationflags=subprocess.CREATE_NO_WINDOW).stdout).strip()
    if 'os_install_date_time' not in dict_info['info']['other_info']:
        dict_info['info']['other_info']['os_install_date_time'] = dict()
        dict_info['info']['other_info']['os_install_date_time'] = os_install_date.strip()

    os_serial_number = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_OperatingSystem).SerialNumber'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout)
    if 'os_serial_number' not in dict_info['info']['other_info']:
        dict_info['info']['other_info']['os_serial_number'] = dict()
        dict_info['info']['other_info']['os_serial_number'] = os_serial_number.strip()

    # license cliendID
    client_machine_id_lic = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance SoftwareLicensingService).ClientMachineID'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout)
    if 'client_machine_id_lic' not in dict_info['info']['other_info']:
        dict_info['info']['other_info']['client_machine_id_lic'] = dict()
        dict_info['info']['other_info']['client_machine_id_lic'] = client_machine_id_lic.strip()

    key_activate_win_uefi = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance SoftwareLicensingService).OA3xOriginalProductKey'], shell=False, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout)
    if key_activate_win_uefi == '':
        pkey = windows_tools.product_key.get_windows_product_key_from_reg()
        if 'key_activate_win' not in dict_info['info']['other_info']:
            dict_info['info']['other_info']['key_activate_win'] = dict()
            dict_info['info']['other_info']['key_activate_win'] = pkey.strip()
    else:
        if 'key_activate_win' not in dict_info['info']['other_info']:
            dict_info['info']['other_info']['key_activate_win'] = dict()
            dict_info['info']['other_info']['key_activate_win'] = key_activate_win_uefi.strip()

    # printer info
    printer_caption = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_Printer).Caption'], shell=False, capture_output=True, text=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout).split("\n")
    for num, prn in enumerate(printer_caption):
        if (len(printer_caption)-1) != num:
            if 'printer_caption' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['printer_caption'] = dict()
            if f'printer_{num}' not in dict_info['info']['other_info']['printer_caption']:
                dict_info['info']['other_info']['printer_caption'][f'printer_{num}'] = dict()
                dict_info['info']['other_info']['printer_caption'][f'printer_{num}'] = prn.strip()

    # time zone info
    time_zone = str(subprocess.run(['powershell.exe', '-NoProfile', '-Command', r'(Get-CimInstance Win32_TimeZone).Caption'], shell=False, capture_output=True, text=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout)
    if 'time_zone' not in dict_info['info']['other_info']:
        dict_info['info']['other_info']['time_zone'] = dict()
        dict_info['info']['other_info']['time_zone'] = time_zone.strip()

    return dict_info

def print_dop_info(dict_info_dop):
    for item in dict_info_dop['info']:
        if item == "other_info":
            print(f'[+] Дополнительная информация\n{"-"*33}')
            for elem in dict_info_dop['info'][item]:
                if elem == 'drive_name_serial':
                    print(f"\n[+] Диски: модель, серийный номер")
                    for drive in dict_info_dop['info'][item][elem]:
                        print(f"\t- {drive}: {dict_info_dop['info'][item][elem][drive]}")
                elif elem == 'drive_firmware':
                    print(f"\n[+] Версия прошивки:")
                    for firmware in dict_info_dop['info'][item][elem]:
                        print(f"\t- {firmware}: {dict_info_dop['info'][item][elem][firmware]}")
                elif elem == 'disk_signature':
                    print(f"\n[+] Цифровая подпись:")
                    for signature in dict_info_dop['info'][item][elem]:
                        print(f"\t- {signature}: {dict_info_dop['info'][item][elem][signature]}")
                elif elem == 'volum_name':
                    print(f"\n[+] Имя тома:")
                    for vol_n in dict_info_dop['info'][item][elem]:
                        print(f"\t- {vol_n}: {dict_info_dop['info'][item][elem][vol_n]}")
                elif elem == 'volume_serial_number':
                    print(f"\n[+] Серийный номер тома:")
                    for volume_serial in dict_info_dop['info'][item][elem]:
                        print(f"\t- {volume_serial}: {dict_info_dop['info'][item][elem][volume_serial]}")
                elif elem == 'memory_form_factor':
                    print(f"\n[+] RAM форм-фактор:")
                    for memory_ff in dict_info_dop['info'][item][elem]:
                        print(f"\t- {memory_ff}: {dict_info_dop['info'][item][elem][memory_ff]}")
                elif elem == 'memory_type':
                    print(f"\n[+] Тип RAM:")
                    for memory_ff in dict_info_dop['info'][item][elem]:
                        print(f"\t- {memory_ff}: {dict_info_dop['info'][item][elem][memory_ff]}")
                elif elem == 'memory_bank_label':
                    print(f"\n[+] RAM bank_label:")
                    for memory_ff in dict_info_dop['info'][item][elem]:
                        print(f"\t- {memory_ff}: {dict_info_dop['info'][item][elem][memory_ff]}")
                elif elem == 'memory_device_locator':
                    print(f"\n[+] RAM device_locator:")
                    for memory_ff in dict_info_dop['info'][item][elem]:
                        print(f"\t- {memory_ff}: {dict_info_dop['info'][item][elem][memory_ff]}")
                elif elem == 'memory_manufacturer':
                    print(f"\n[+] Производитель RAM:")
                    for memory_man in dict_info_dop['info'][item][elem]:
                        print(f"\t- {memory_man}: {dict_info_dop['info'][item][elem][memory_man]}")
                elif elem == 'memory_part_number':
                    print(f"\n[+] Инвентарный номер RAM:")
                    for memory_part in dict_info_dop['info'][item][elem]:
                        print(f"\t- {memory_part}: {dict_info_dop['info'][item][elem][memory_part]}")
                elif elem == 'memory_serial_number':
                    print(f"\n[+] Серийный номер RAM:")
                    for memory_serial in dict_info_dop['info'][item][elem]:
                        print(f"\t- {memory_serial}: {dict_info_dop['info'][item][elem][memory_serial]}")
                elif elem == 'memory_frequency':
                    print(f"\n[+] Частота RAM:")
                    for memory_fr in dict_info_dop['info'][item][elem]:
                        print(f"\t- {memory_fr}: {dict_info_dop['info'][item][elem][memory_fr]}")
                elif elem == 'net_adapter_caption':
                    print(f"\n[+] Название сетевого адаптера:")
                    for adapter_caption in dict_info_dop['info'][item][elem]:
                        print(f"\t- {adapter_caption}: {dict_info_dop['info'][item][elem][adapter_caption]}")
                elif elem == 'guid_net_adapter':
                    print(f"\n[+] GUID сетевого адаптера:")
                    for guid_net in dict_info_dop['info'][item][elem]:
                        print(f"\t- {guid_net}: {dict_info_dop['info'][item][elem][guid_net]}")
                elif elem == 'printer_caption':
                    print(f"\n[+] Название принтера:")
                    for prn_caption in dict_info_dop['info'][item][elem]:
                        print(f"\t- {prn_caption}: {dict_info_dop['info'][item][elem][prn_caption]}")
                else:
                    print(f"[+] {elem.upper()}: {dict_info_dop['info'][item][elem]}")

def print_info(dict_info):
    for item in dict_info['info']:
        if item == "system_info":
            for elem in dict_info['info'][item]:
                if elem == 'system':
                    print(f"[+] Информация о системе\n"
                          f"\t- Имя компьютера: {dict_info['info'][item][elem]['comp_name']}\n"
                          f"\t- Опереционная система: {dict_info['info'][item][elem]['os_name']}\n"
                          f"\t- Сборка: {dict_info['info'][item][elem]['version']}\n"
                          f"\t- Архитектура: {dict_info['info'][item][elem]['machine']}\n")
                if elem == 'processor':
                    print(f"[+] Информация о процессоре\n"
                          f"\t- Семейство: {dict_info['info'][item][elem]['name']}\n"
                          f"\t- Физические ядра: {dict_info['info'][item][elem]['phisycal_core']}\n"
                          f"\t- Всего ядер: {dict_info['info'][item][elem]['all_core']}\n"
                          f"\t- Максимальная частота: {dict_info['info'][item][elem]['freq_max']}\n")
                if elem == 'ram':
                    print(f"[+] Оперативная память\n"
                          f"\t- Объем: {dict_info['info'][item][elem]['volume']}\n"
                          f"\t- Доступно: {dict_info['info'][item][elem]['aviable']}\n"
                          f"\t- Используется: {dict_info['info'][item][elem]['used']}\n")
        if item == "disk_info":
            for elem in dict_info['info'][item]:
                print(f"[+] Информация о дисках\n"
                      f"\t- Имя диска: {elem}\n"
                      f"\t- Файловая система: {dict_info['info'][item][elem]['file_system']}\n"
                      f"\t- Объем диска: {dict_info['info'][item][elem]['size_total']}\n"
                      f"\t- Занято: {dict_info['info'][item][elem]['size_used']}\n"
                      f"\t- Свободно: {dict_info['info'][item][elem]['size_free']}\n"
                      f"\t- Заполненность: {dict_info['info'][item][elem]['percent']}%\n")
        if item == "net_info":
            for elem in dict_info['info'][item]:
                print(f"[+] Информация о сети\n"
                      f"\t- Имя интерфейса: {elem}\n"
                      f"\t- MAC-адрес: {dict_info['info'][item][elem]['mac']}\n"
                      f"\t- IPv4: {dict_info['info'][item][elem]['ipv4']}\n"
                      f"\t- IPv6: {dict_info['info'][item][elem]['ipv6']}\n")

# def portscanner(port, target, src):
#     s = socket.socket()
#     s.settimeout(0.5)
#     try:
#         s.connect((target, port))
#     except socket.error:
#        pass
#     else:
#         s.close()
#         try:
#             print(f'Открыт порт: {port}/{src[str(port)]}')
#             port_list.append(f'{port}/{src[str(port)]}')
#         except:
#             print(f'Открыт порт: {port}/Unassigned')
#         time.sleep(1)
#
# def thread_func(src):
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#     s.connect(('<broadcast>', 0))
#     ip = s.getsockname()[0]
#     for port in src:
#        t = threading.Thread(target=portscanner, kwargs={'port': int(port), 'target': ip, 'src': src})
#        t.start()

def main():
    if uname().system == "Windows":
        dict_info = creating_file()
        dict_info_dop = win_dop_info(dict_info)
        with open(f'{uname().node}_info.json', 'w', encoding='utf-8') as file:
            json.dump(dict_info_dop, file, indent=4, ensure_ascii=False)
        print_info(dict_info)
        print_dop_info(dict_info_dop)
    elif uname().system == "Linux":
        dict_info = creating_file()
        with open(f'{uname().node}_info.json', 'w', encoding='utf-8') as file:
            json.dump(dict_info, file, indent=4, ensure_ascii=False)
        print_info(dict_info)
    # try:
    #    with open('ps_dict.json', 'r', encoding='utf-8') as file:
    #        src = json.load(file)
    # except:
    #    src = list(range(1, 1001))
    # print(f'\n[+] Открытые порты\n{"-"*33}')
    # thread_func(src)
    # if len(port_list) > 0:
    #    with open(f'{uname().node}_open_port.txt', 'w') as file:
    #        for port in port_list:
    #            file.write(f'{port}\n')


if __name__ == "__main__":
    main()
