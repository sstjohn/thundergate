/*
 *  ThunderGate - an open source toolkit for PCI bus exploration
 *  Copyright (C) 2015  Saul St. John
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef _MSI_H_
#define _MSI_H_

struct msi_mode {
    u32 priority :2;
    u32 msix_fix_pcie_client :1;
    u32 reserved :18;
    u32 msi_message :3;
    u32 msix_multi_vector_mode :1;
    u32 msi_byte_swap_enable :1;
    u32 msi_single_shot_disable :1;
    u32 pci_parity_error_attn :1;
    u32 pci_master_abort_attn :1;
    u32 pci_target_abort_attn :1;
    u32 enable :1;
    u32 reset :1;
};

struct msi_status {
    u32 reserved :27;
    u32 pci_parity_error :1;
    u32 pci_master_abort :1;
    u32 pci_target_abort :1;
    u32 reserved2 :1;
    u32 msi_pci_request :1;
};

struct msi_regs {
    struct msi_mode mode;
    struct msi_status status;
};

#endif
