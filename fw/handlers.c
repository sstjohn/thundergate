/*
 *  ThunderGate - an open source toolkit for PCI bus exploration
 *  Copyright (C) 2015-2026  Saul St. John
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

#include "fw.h"
#include "console.h"

void dump_pcie_retry_buffer(reply_t reply)
{
	u32 data[40];
	for (int i = 0; i < 40; i++) {
		pcie_dl.retry_buffer_read_ptr.value = i;
		data[i] = pcie_dl.retry_buffer_read_write_port;
	}
	(*reply)(data, 40, PCIE_RETRY_BUFFER_DUMP_ACK);
}

void dma_read(u32 addr_hi, u32 addr_low, u32 length, reply_t reply)
{
	u32 bd_cnt = (7 + length) >> 3;

	rbdi.mode.reset = 1;
	rdma.mode.reset = 1;
	while (rbdi.mode.reset | rdma.mode.reset);

	lpmb.box[mb_rbd_standard_producer].low = 0;

	rdi.std_rcb.host_addr_hi = addr_hi;
	rdi.std_rcb.host_addr_low = addr_low;
	rdi.std_rcb.ring_size = 0x200;
	rdi.std_rcb.max_frame_len = 0;
	rdi.std_rcb.nic_addr = 0x6000;
	rdi.std_rcb.disable_ring = 0;

	rdma.mode.enable = 1;
	rbdi.mode.enable = 1;

	lpmb.box[mb_rbd_standard_producer].low = bd_cnt;


	(*reply)((void *)0x6000, length, READ_DMA_REPLY);
}

/* SRAM (GATE_SHMEM) -> host physical memory; counterpart to dma_read().
 * arg1:arg2 give the 64-bit host destination, arg3 the byte length; the
 * payload is the inbound frame body, already in NIC-local memory at
 * lgate_base + 0x10.  Returns nonzero on failure.
 *
 * dma_read abuses the receive BD initiator's host->nic prefetch; there
 * is no nic->host "copy" unit to mirror it.  nic->host bulk movement is
 * the write-DMA engine's job, and wdma carries no host-address registers
 * of its own (wdma.h) -- it is descriptor-driven, and is already enabled
 * at init (init.c).  So we hand it one dma_desc (dma.h) through the
 * dma_write frame/transmit queue.
 *
 * HARDWARE-UNVERIFIED: no in-tree code drives ftq.dma_write or builds a
 * dma_desc.  Three points of the wdma contract are inferred here and
 * want checking against the BCM5719 programmer's guide / bcm5719-fw:
 *   (1) dma_desc.nic_mbuf carries a raw NIC source address;
 *   (2) enqueue is (mbuf_idx << 16 | mbuf_idx) -> q.word, the encoding
 *       tx_asf() uses for the mac_tx queue;
 *   (3) completion is the dma_write queue draining back to count 0. */
u32 dma_write(u32 addr_hi, u32 addr_low, u32 length)
{
	/* the descriptor lives in a txmbuf clear of the TX path; the FTQ
	 * enqueue ports index txmbufs, so keep the index in range */
	const u32 desc_mbuf = 0x3e;
	volatile struct dma_desc *d =
		(volatile struct dma_desc *)&txmbuf0[desc_mbuf];
	u32 spin = 0x100000;

	if (length == 0 || length > GATE_SHMEM_SIZE - 0x10)
		return 1;

	d->addr_hi   = addr_hi;
	d->addr_lo   = addr_low;
	d->nic_mbuf  = (u32)(lgate_base + 0x10);
	d->length    = length;
	d->cqid_sqid = 0;
	d->flags     = 0;
	d->opaque1   = 0;
	d->opaque2   = 0;
	d->opaque3   = 0;

	ftq.dma_write.q.word = (desc_mbuf << 16) | desc_mbuf;

	/* bounded so a wrong completion guess returns ERR, not a hang */
	while (ftq.dma_write.count && --spin)
		;

	return spin ? 0 : 1;
}

u32 local_read_dword(u32 addr)
{
	u32 *p = (u32 *)addr;
	return *p;
}

void local_write_dword(u32 addr, u32 val)
{
	u32 *p = (u32 *)addr;
	*p = val;
}

void send_msi(u32 addr_hi, u32 addr_low, u32 data)
{
    pci.msi_upper_address = addr_hi;
    pci.msi_lower_address = addr_low;
    pci.msi_data = data;
    msi.mode.msi_message = 0;

    pci.msi_cap_hdr.msi_enable = 1;
    msi.mode.enable = 1;
    msi.status.msi_pci_request = 1;
}

void cap_ctrl(u32 cap, u32 enabled)
{
	if (cap & CAP_POWER_MANAGEMENT)
		cfg_port.cap_ctrl.pm_en = !!enabled;
	if (cap & CAP_VPD)
		cfg_port.cap_ctrl.vpd_en = !!enabled;
	if (cap & CAP_MSI)
		cfg_port.cap_ctrl.msi_en = !!enabled;
	if (cap & CAP_MSIX)
		cfg_port.cap_ctrl.msix_en = !!enabled;
}

void hide_func(u32 func, u32 hidden)
{
    u32 mask = (1 << (func - 1)) & 7;
    u32 val = cpmu.control.hide_pcie_function;
    if (hidden)
	val |= mask;
    else
        val &= ~mask;
    cpmu.control.hide_pcie_function = val;
}

void pme_assert()
{
	if (!pci.pm_ctrl_status.pme_enable)
		pci.pm_ctrl_status.pme_enable = 1;
	grc.misc_local_control.pme_assert = 1;
}

void handle(reply_t reply, u16 cmd, u32 arg1, u32 arg2, u32 arg3)
{
    u32 tmp;

    switch(cmd) {
        case PING_CMD:
	    (*reply)(0, 0, PING_REPLY);
            break;

	case READ_LOCAL_CMD:
	    (*reply)((void *)arg1, arg2, READ_LOCAL_REPLY);
	    break;

	case WRITE_LOCAL_CMD:
	    local_write_dword(arg1, arg2);
	    (*reply)(0, 0, WRITE_LOCAL_ACK);
	    break;

        case READ_DMA_CMD:
            dma_read(arg1, arg2, arg3, reply);
            break;

	case SEND_MSI_CMD:
	    send_msi(arg1, arg2, arg3);
	    (*reply)(0, 0, SEND_MSI_ACK);
	    break;

	case CAP_CTRL_CMD:
	    cap_ctrl(arg1, arg2);
	    (*reply)(0, 0, CAP_CTRL_ACK);
            break;

	case HIDE_FUNC_CMD:
	    hide_func(arg1, arg2);
	    (*reply)(0, 0, HIDE_FUNC_ACK);
	    break;

	case PME_ASSERT_CMD:
	    pme_assert();
	    (*reply)(0, 0, PME_ASSERT_ACK);
	    break;

	case READ_NVRAM_CMD:
	    tmp = read_nvram(arg1);
            (*reply)(&tmp, 1, READ_NVRAM_ACK);
	    break;

	case WRITE_NVRAM_CMD:
	    write_nvram(arg1, arg2);
	    (*reply)(0, 0, WRITE_NVRAM_ACK);
	    break;

	case PCIE_RETRY_BUFFER_DUMP_CMD:
	    dump_pcie_retry_buffer(reply);
	    break;

	case CLOAK_EN_CMD:
	    cloak_engage();
	    (*reply)(0, 0, CLOAK_EN_ACK);
	    break;

	case CLOAK_DIS_CMD:
	    cloak_disengage();
	    (*reply)(0, 0, CLOAK_DIS_ACK);
	    break;

	case TX_STD_ENQ_CMD:
	    if (tx_std_enq(arg1, arg2, arg3))
		(*reply)(0, 0, TX_STD_ENQ_ERR);
	    break;

	case WRITE_DMA_CMD:
	    if (dma_write(arg1, arg2, arg3))
		(*reply)(0, 0, WRITE_DMA_ERR);
	    else
		(*reply)(0, 0, WRITE_DMA_ACK);
	    break;

	case INTERP_EVAL_CMD: {
	    /* reply layout: u32 length, then `length` bytes of console output. */
	    u32 buf[1 + (256 + 3) / 4];
	    u32 i, n;
	    con_out_reset();
	    interp_eval_line((const char *)(lgate_base + 0x10), arg1);
	    n = con_out_len();
	    buf[0] = n;
	    for (i = 0; i < n; i++)
		((u8 *)&buf[1])[i] = con_out_buf()[i];
	    (*reply)(buf, 1 + ((n + 3) >> 2), INTERP_EVAL_REPLY);
	    break;
	}

        default:
	    (*reply)(&arg1, 2, UNKNOWN_CMD);
            break;
    }
}
