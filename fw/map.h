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

#ifndef _MAP_H_
#define _MAP_H_

#include "mbuf.h"
#include "rcb.h"
#include "dma.h"

#include "utypes.h"
#include "pci.h"
#include "emac.h"
#include "sdi.h"
#include "sdc.h"
#include "sbds.h"
#include "sbdi.h"
#include "sbdc.h"
#include "rlp.h"
#include "rdi.h"
#include "rdc.h"
#include "rbdi.h"
#include "rbdc.h"
#include "cpmu.h"
#include "hc.h"
#include "ma.h"
#include "bufman.h"
#include "bdrdma.h"
#include "rdma.h"
#include "wdma.h"
#include "cpu.h"
#include "ftq.h"
#include "dmac.h"
#include "msi.h"
#include "grc.h"
#include "otp.h"
#include "tcp_seg_ctrl.h"
#include "nvram.h"
#include "cfg_port.h"
#include "pcie.h"

volatile u32 gencomm[300];
volatile struct mbuf txmbuf0[0];
volatile struct mbuf txmbuf1[0];
volatile struct mbuf rxmbuf[0];
volatile u32 rom[0];
volatile u32 reg[0];
volatile u32 scratchpad[0];
volatile struct pci_regs pci;
volatile u32 hpmb[0];
volatile struct lpmb_regs lpmb;
volatile struct emac_regs emac;
volatile struct sdi_regs sdi;
volatile struct sdc_regs sdc;
volatile struct sbds_regs sbds;
volatile struct sbdi_regs sbdi;
volatile struct sbdc_regs sbdc;
volatile struct rlp_regs rlp;
volatile struct rdi_regs rdi;
volatile struct rdc_regs rdc;
volatile struct rbdi_regs rbdi;
volatile struct rbdc_regs rbdc;
volatile struct cpmu_regs cpmu;
volatile struct hc_regs hc;
volatile struct ma_regs ma;
volatile struct bufman_regs bufman;
volatile struct rdma_regs rdma;
volatile struct wdma_regs wdma;
volatile struct cpu_regs rxcpu;
volatile struct ftq_regs ftq;
volatile struct dmac_regs dmac;
volatile struct msi_regs msi;
volatile struct cfg_port_regs cfg_port;
volatile struct grc_regs grc;
volatile struct otp_regs otp;
volatile struct nvram_regs nvram;
volatile struct tcp_seg_ctrl_regs tcp_seg_ctrl;
volatile struct bdrdma_regs bdrdma;
volatile struct pcie_tl_regs pcie_tl;
volatile struct pcie_dl_regs pcie_dl;
#endif
