from ctypes import *



mb_sbd_nic_producer = 112
mb_sbd_host_producer = 32
mb_rbd_rr3_consumer = 19
mb_rbd_rr2_consumer = 18
mb_rbd_rr1_consumer = 17
mb_rbd_standard_producer = 13
mb_interrupt = 0
mb_rbd_rr0_consumer = 16
def TG3_IMAGE_TYPE(x): return ((x) >> 24) # macro
def TG3_IMAGE_LEN(x): return (((x) & 0x3fffff) << 2) # macro
class dmar_tbl_hdr(Structure):
    pass
uint32_t = c_uint32
u32 = uint32_t
uint8_t = c_uint8
u8 = uint8_t
dmar_tbl_hdr._pack_ = 1
dmar_tbl_hdr._fields_ = [
    ('sig', c_char * 4),
    ('length', u32),
    ('rev', u8),
    ('cksum', u8),
    ('oemid', c_char * 6),
    ('oemtableid', c_char * 8),
    ('oem_rev', u32),
    ('creator_id', c_char * 4),
    ('creator_rev', u32),
    ('host_addr_width', u8),
    ('flags', u8),
    ('reserved', c_char * 10),
]
class dmar_dev_scope(Structure):
    pass
uint16_t = c_uint16
u16 = uint16_t
class N14dmar_dev_scope3DOT_0E(Structure):
    pass
N14dmar_dev_scope3DOT_0E._fields_ = [
    ('device', u8),
    ('function', u8),
]
dmar_dev_scope._pack_ = 1
dmar_dev_scope._fields_ = [
    ('type', u8),
    ('length', u8),
    ('reserved', u16),
    ('enum_id', u8),
    ('start_bus_number', u8),
    ('path', N14dmar_dev_scope3DOT_0E * 0),
]
class dmar_drhd(Structure):
    pass
uint64_t = c_uint64
u64 = uint64_t
dmar_drhd._pack_ = 1
dmar_drhd._fields_ = [
    ('type', u16),
    ('length', u16),
    ('flags', u8),
    ('reserved', u8),
    ('seg_no', u16),
    ('base_address', u64),
]
class dmar_rmrr(Structure):
    pass
dmar_rmrr._pack_ = 1
dmar_rmrr._fields_ = [
    ('type', u16),
    ('length', u16),
    ('flags', u8),
    ('reserved', u8),
    ('seg_no', u16),
    ('base_addr', u64),
    ('limit_addr', u64),
]
class dmar_atsr(Structure):
    pass
dmar_atsr._pack_ = 1
dmar_atsr._fields_ = [
    ('type', u16),
    ('length', u16),
    ('flags', u8),
    ('reserved', u8),
    ('seg_no', u16),
    ('dev_scope', dmar_dev_scope * 0),
]
class dmar_rhsa(Structure):
    pass
dmar_rhsa._pack_ = 1
dmar_rhsa._fields_ = [
    ('type', u16),
    ('length', u16),
    ('reserved', u32),
    ('base_addr', u64),
    ('proximity_domain', u32),
]
class dmar_andd(Structure):
    pass
dmar_andd._pack_ = 1
dmar_andd._fields_ = [
    ('type', u16),
    ('length', u16),
    ('reserved', u8 * 3),
    ('acpi_dev_no', u8),
    ('object_name', c_char * 0),
]
class acpi_sdt_hdr(Structure):
    pass
acpi_sdt_hdr._pack_ = 1
acpi_sdt_hdr._fields_ = [
    ('sig', c_char * 4),
    ('length', u32),
    ('rev', u8),
    ('cksum', u8),
    ('oemid', c_char * 6),
    ('oemtableid', c_char * 8),
    ('oem_rev', u32),
    ('creator_id', u32),
    ('creator_rev', u32),
]
class xsdt(Structure):
    pass
xsdt._pack_ = 1
xsdt._fields_ = [
    ('h', acpi_sdt_hdr),
    ('sdt', POINTER(acpi_sdt_hdr) * 0),
]
class rsdp_t(Structure):
    pass
rsdp_t._pack_ = 1
rsdp_t._fields_ = [
    ('sig', c_char * 8),
    ('cksum', u8),
    ('oemid', c_char * 6),
    ('rev', u8),
    ('rsdt_address', u32),
]
class rsdp2_t(Structure):
    pass
rsdp2_t._pack_ = 1
rsdp2_t._fields_ = [
    ('sig', c_char * 8),
    ('cksum', u8),
    ('oemid', c_char * 6),
    ('rev', u8),
    ('rsdt_address', u32),
    ('length', u32),
    ('xsdt_address', u64),
    ('extended_cksum', u8),
    ('reserved', u8 * 3),
]
class asf_control(Structure):
    pass
asf_control._fields_ = [
    ('smb_early_attention', u32, 1),
    ('smb_enable_addr_0', u32, 1),
    ('nic_smb_addr_2', u32, 7),
    ('nic_smb_addr_1', u32, 7),
    ('smb_autoread', u32, 1),
    ('smb_addr_filter', u32, 1),
    ('smb_bit_bang_en', u32, 1),
    ('smb_en', u32, 1),
    ('asf_attention_loc', u32, 4),
    ('smb_attention', u32, 1),
    ('retransmission_timer_expired', u32, 1),
    ('poll_legacy_timer_expired', u32, 1),
    ('poll_asf_timer_expired', u32, 1),
    ('heartbeat_timer_expired', u32, 1),
    ('watchdog_timer_expired', u32, 1),
    ('timestamp_counter_en', u32, 1),
    ('reset', u32, 1),
]
class asf_smbus_input(Structure):
    pass
asf_smbus_input._fields_ = [
    ('reserved', u32, 18),
    ('smb_input_status', u32, 3),
    ('input_firstbye', u32, 1),
    ('input_done', u32, 1),
    ('input_ready', u32, 1),
    ('data_input', u32, 8),
]
class asf_smbus_output(Structure):
    pass
asf_smbus_output._fields_ = [
    ('reserved', u32, 3),
    ('clock_input', u32, 1),
    ('clock_enable', u32, 1),
    ('data_input_value', u32, 1),
    ('data_enable', u32, 1),
    ('slave_mode', u32, 1),
    ('output_status', u32, 4),
    ('read_length', u32, 6),
    ('get_receive_length', u32, 1),
    ('enable_pec', u32, 1),
    ('access_type', u32, 1),
    ('output_last', u32, 1),
    ('output_start', u32, 1),
    ('output_ready', u32, 1),
    ('data_output', u32, 8),
]
class asf_watchdog_timer(Structure):
    pass
asf_watchdog_timer._fields_ = [
    ('reserved', u32, 24),
    ('count', u32, 8),
]
class asf_heartbeat_timer(Structure):
    pass
asf_heartbeat_timer._fields_ = [
    ('reserved', u32, 16),
    ('count', u32, 8),
]
class asf_poll_timer(Structure):
    pass
asf_poll_timer._fields_ = [
    ('reserved', u32, 24),
    ('count', u32, 8),
]
class asf_poll_legacy_timer(Structure):
    pass
asf_poll_legacy_timer._fields_ = [
    ('reserved', u32, 24),
    ('count', u32, 8),
]
class asf_retransmission_timer(Structure):
    pass
asf_retransmission_timer._fields_ = [
    ('reserved', u32, 24),
    ('count', u32, 8),
]
class asf_time_stamp_counter(Structure):
    pass
asf_time_stamp_counter._fields_ = [
    ('count', u32),
]
class asf_smbus_driver_select(Structure):
    pass
asf_smbus_driver_select._fields_ = [
    ('enable_smbus_stretching', u32, 1),
    ('reserved', u32, 9),
    ('rng', u32, 2),
    ('valid', u32, 1),
    ('div2', u32, 1),
    ('rng_enable', u32, 1),
    ('rng_reset', u32, 1),
    ('reserved2', u32, 16),
]
class asf_regs(Structure):
    pass
asf_regs._fields_ = [
    ('control', asf_control),
    ('smbus_input', asf_smbus_input),
    ('smbus_output', asf_smbus_output),
    ('watchdog_timer', asf_watchdog_timer),
    ('heartbeat_timer', asf_heartbeat_timer),
    ('poll_timer', asf_poll_timer),
    ('poll_legacy_timer', asf_poll_legacy_timer),
    ('retransmission_timer', asf_retransmission_timer),
    ('time_stamp_counter', asf_time_stamp_counter),
    ('smbus_driver_select', asf_smbus_driver_select),
]
class sbd_flags(Structure):
    pass
class N9sbd_flags3DOT_1E(Union):
    pass
class N9sbd_flags3DOT_13DOT_2E(Structure):
    pass
N9sbd_flags3DOT_13DOT_2E._fields_ = [
    ('l4_cksum_offload', u16, 1),
    ('ip_cksum_offload', u16, 1),
    ('packet_end', u16, 1),
    ('jumbo_frame', u16, 1),
    ('hdrlen_2', u16, 1),
    ('snap', u16, 1),
    ('vlan_tag', u16, 1),
    ('coalesce_now', u16, 1),
    ('cpu_pre_dma', u16, 1),
    ('cpu_post_dma', u16, 1),
    ('hdrlen_3', u16, 1),
    ('hdrlen_4', u16, 1),
    ('hdrlen_5', u16, 1),
    ('hdrlen_6', u16, 1),
    ('hdrlen_7', u16, 1),
    ('no_crc', u16, 1),
]
N9sbd_flags3DOT_1E._anonymous_ = ['_0']
N9sbd_flags3DOT_1E._fields_ = [
    ('_0', N9sbd_flags3DOT_13DOT_2E),
    ('word', u16),
]
sbd_flags._anonymous_ = ['_0']
sbd_flags._fields_ = [
    ('_0', N9sbd_flags3DOT_1E),
]
class sbd(Structure):
    pass
sbd._fields_ = [
    ('addr_hi', u32),
    ('addr_low', u32),
    ('flags', sbd_flags),
    ('length', u16),
    ('vlan_tag', u16),
    ('mss', u16, 14),
    ('hdrlen_0_1', u16, 2),
]
class rbd_flags(Structure):
    pass
class N9rbd_flags3DOT_3E(Union):
    pass
class N9rbd_flags3DOT_33DOT_4E(Structure):
    pass
N9rbd_flags3DOT_33DOT_4E._fields_ = [
    ('is_ipv6', u16, 1),
    ('is_tcp', u16, 1),
    ('l4_checksum_correct', u16, 1),
    ('ip_checksum_correct', u16, 1),
    ('reserved', u16, 1),
    ('has_error', u16, 1),
    ('rss_hash_type', u16, 3),
    ('has_vlan_tag', u16, 1),
    ('reserved2', u16, 1),
    ('reserved3', u16, 1),
    ('rss_hash_valid', u16, 1),
    ('packet_end', u16, 1),
    ('reserved4', u16, 1),
    ('reserved5', u16, 1),
]
N9rbd_flags3DOT_3E._anonymous_ = ['_0']
N9rbd_flags3DOT_3E._fields_ = [
    ('_0', N9rbd_flags3DOT_33DOT_4E),
    ('word', u16),
]
rbd_flags._anonymous_ = ['_0']
rbd_flags._fields_ = [
    ('_0', N9rbd_flags3DOT_3E),
]
class rbd_error_flags(Structure):
    pass
class N15rbd_error_flags3DOT_5E(Union):
    pass
class N15rbd_error_flags3DOT_53DOT_6E(Structure):
    pass
N15rbd_error_flags3DOT_53DOT_6E._fields_ = [
    ('reserved1', u16, 1),
    ('reserved2', u16, 1),
    ('reserved3', u16, 1),
    ('reserved4', u16, 1),
    ('reserved5', u16, 1),
    ('reserved6', u16, 1),
    ('reserved7', u16, 1),
    ('giant_packet', u16, 1),
    ('trunc_no_res', u16, 1),
    ('len_less_64', u16, 1),
    ('mac_abort', u16, 1),
    ('dribble_nibble', u16, 1),
    ('phy_decode_error', u16, 1),
    ('link_lost', u16, 1),
    ('collision', u16, 1),
    ('bad_crc', u16, 1),
]
N15rbd_error_flags3DOT_5E._anonymous_ = ['_0']
N15rbd_error_flags3DOT_5E._fields_ = [
    ('_0', N15rbd_error_flags3DOT_53DOT_6E),
    ('word', u16),
]
rbd_error_flags._anonymous_ = ['_0']
rbd_error_flags._fields_ = [
    ('_0', N15rbd_error_flags3DOT_5E),
]
class rbd(Structure):
    pass
rbd._fields_ = [
    ('addr_hi', u32),
    ('addr_low', u32),
    ('length', u16),
    ('index', u16),
    ('type', u16),
    ('flags', rbd_flags),
    ('ip_cksum', u16),
    ('l4_cksum', u16),
    ('error_flags', rbd_error_flags),
    ('vlan_tag', u16),
    ('rss_hash', u32),
    ('opaque', u32),
]
class rbd_ex(Structure):
    pass
rbd_ex._fields_ = [
    ('addr1_hi', u32),
    ('addr1_low', u32),
    ('addr2_hi', u32),
    ('addr2_low', u32),
    ('addr3_hi', u32),
    ('addr3_low', u32),
    ('len1', u16),
    ('len2', u16),
    ('len3', u16),
    ('reserved', u16),
    ('addr0_hi', u32),
    ('addr0_low', u32),
    ('index', u16),
    ('len0', u16),
    ('type', u16),
    ('flats', u16),
    ('ip_cksum', u16),
    ('tcp_udp_cksum', u16),
    ('error_flags', u16),
    ('vlan_tag', u16),
    ('rss_hash', u32),
    ('opaque', u32),
]
class bdrdma_mode(Structure):
    pass
bdrdma_mode._fields_ = [
    ('reserved26', u32, 6),
    ('addr_oflow_err_log_en', u32, 1),
    ('reserved18', u32, 7),
    ('pci_req_burst_len', u32, 2),
    ('reserved14', u32, 2),
    ('attention_enables', u32, 12),
    ('enable', u32, 1),
    ('reserved0', u32, 1),
]
class bdrdma_status(Structure):
    pass
bdrdma_status._fields_ = [
    ('reserved10', u32, 21),
    ('malformed_tlp_or_poison_tlp_err_det', u32, 1),
    ('local_mem_wr_longer_than_dma_len_err', u32, 1),
    ('pci_fifo_overread_err', u32, 1),
    ('pci_fifo_underread_err', u32, 1),
    ('pci_fifo_overrun_err', u32, 1),
    ('pci_host_addr_oflow_err', u32, 1),
    ('dma_rd_compltn_timeout', u32, 1),
    ('compltn_abrt_err', u32, 1),
    ('unsup_req_err_det', u32, 1),
    ('reserved0', u32, 2),
]
class bdrdma_len_dbg(Structure):
    pass
bdrdma_len_dbg._fields_ = [
    ('rdmad_length_b_2', u32, 16),
    ('rdmad_length_b_1', u32, 16),
]
class bdrdma_rstates_dbg(Structure):
    pass
bdrdma_rstates_dbg._fields_ = [
    ('rbdi_cnt', u32, 16),
    ('reserved2', u32, 14),
    ('rstate1', u32, 2),
]
class bdrdma_rstate2_dbg(Structure):
    pass
bdrdma_rstate2_dbg._fields_ = [
    ('host_addr', u32, 28),
    ('rstate2', u32, 4),
]
class bdrdma_bd_status_dbg(Structure):
    pass
bdrdma_bd_status_dbg._fields_ = [
    ('rlctrl', u32, 9),
    ('dmad_load_and_mem_ok', u32, 1),
    ('int_rh_dmad_load', u32, 1),
    ('rh_dmad_load_fst', u32, 1),
    ('rh_dmad_done_syn3', u32, 1),
    ('rh_dmad_load_en', u32, 1),
    ('rh_dmad_no_empty', u32, 1),
    ('hold_dmad_n_empty', u32, 1),
    ('rwr_ptr', u32, 2),
    ('rrd_ptr', u32, 2),
    ('dmad_pnt2', u32, 2),
    ('dmad_pnt1', u32, 2),
    ('dmad_pnt0', u32, 2),
    ('dmad_pnt', u32, 2),
    ('reserved3', u32, 1),
    ('bd_non_mbuf', u32, 1),
    ('fst_bd_mbuf', u32, 1),
    ('lst_bd_mbuf', u32, 1),
]
class bdrdma_req_ptr_dbg(Structure):
    pass
bdrdma_req_ptr_dbg._fields_ = [
    ('ih_dmad_len', u32, 16),
    ('reserved13', u32, 3),
    ('txmbuf_left', u32, 8),
    ('rh_dmad_load_en', u32, 1),
    ('rftq_d_dmad_pnt', u32, 2),
    ('rftq_b_dmad_pnt', u32, 2),
]
class bdrdma_hold_d_dmad_dbg(Structure):
    pass
bdrdma_hold_d_dmad_dbg._fields_ = [
    ('reserved4', u32, 28),
    ('rhold_b_dmad', u32, 2),
    ('reserved0', u32, 2),
]
class bdrdma_len_and_addr_idx_dbg(Structure):
    pass
bdrdma_len_and_addr_idx_dbg._fields_ = [
    ('rdma_rd_length', u32, 16),
    ('reserved0', u32, 16),
]
class bdrdma_addr_idx_dbg(Structure):
    pass
bdrdma_addr_idx_dbg._fields_ = [
    ('reserved5', u32, 23),
    ('h_host_addr_i', u32, 5),
]
class bdrdma_pcie_dbg_status(Structure):
    pass
bdrdma_pcie_dbg_status._fields_ = [
    ('lt_term', u32, 4),
    ('reserved27', u32, 1),
    ('lt_too_lg', u32, 1),
    ('lt_dma_reload', u32, 1),
    ('lt_dma_good', u32, 1),
    ('cur_trans_active', u32, 1),
    ('dr_pci_req', u32, 1),
    ('dr_pci_word_swap', u32, 1),
    ('dr_pci_byte_swap', u32, 1),
    ('new_slow_core_clk_mode', u32, 1),
    ('rbd_non_mbuf', u32, 1),
    ('rfst_bd_mbuf', u32, 1),
    ('rlsd_bd_mbuf', u32, 1),
    ('dr_pci_len', u32, 16),
]
class bdrdma_pcie_dma_rd_req_addr_dbg(Structure):
    pass
bdrdma_pcie_dma_rd_req_addr_dbg._fields_ = [
    ('dr_pci_ad_hi', u32, 16),
    ('dr_pci_ad_lo', u32, 16),
]
class bdrdma_pcie_dma_req_len_dbg(Structure):
    pass
bdrdma_pcie_dma_req_len_dbg._fields_ = [
    ('reserved16', u32, 16),
    ('rdma_len', u32, 16),
]
class bdrdma_fifo1_dbg(Structure):
    pass
bdrdma_fifo1_dbg._fields_ = [
    ('reserved9', u32, 23),
    ('c_write_addr', u32, 9),
]
class bdrdma_fifo2_dbg(Structure):
    pass
bdrdma_fifo2_dbg._fields_ = [
    ('reserved18', u32, 14),
    ('rlctrl_in', u32, 9),
    ('c_read_addr', u32, 9),
]
class bdrdma_rsvrd_ctrl(Structure):
    pass
bdrdma_rsvrd_ctrl._fields_ = [
    ('reserved21', u32, 11),
    ('sel_fed_en_bd', u32, 1),
    ('fifo_high_mark_bd', u32, 8),
    ('fifo_low_mark_bd', u32, 8),
    ('slow_clock_fix_dis_bd', u32, 1),
    ('hw_fix_cq25155_en', u32, 1),
    ('reserved0', u32, 2),
]
class bdrdma_regs(Structure):
    pass
bdrdma_regs._fields_ = [
    ('mode', bdrdma_mode),
    ('status', bdrdma_status),
    ('len_dbg', bdrdma_len_dbg),
    ('rstates_dbg', bdrdma_rstates_dbg),
    ('rstate2_dbg', bdrdma_rstate2_dbg),
    ('bd_status_dbg', bdrdma_bd_status_dbg),
    ('req_ptr_dbg', bdrdma_req_ptr_dbg),
    ('hold_d_dmad_dbg', bdrdma_hold_d_dmad_dbg),
    ('len_and_addr_idx_dbg', bdrdma_len_and_addr_idx_dbg),
    ('addr_idx_dbg', bdrdma_addr_idx_dbg),
    ('pcie_dbg_status', bdrdma_pcie_dbg_status),
    ('pcie_dma_rd_req_addr_dbg', bdrdma_pcie_dma_rd_req_addr_dbg),
    ('pcie_dma_req_len_dbg', bdrdma_pcie_dma_req_len_dbg),
    ('fifo1_dbg', bdrdma_fifo1_dbg),
    ('fifo2_dbg', bdrdma_fifo2_dbg),
    ('ofs_3c', u32),
    ('ofs_40', u32),
    ('ofs_44', u32),
    ('ofs_48', u32),
    ('ofs_4c', u32),
    ('ofs_50', u32),
    ('ofs_54', u32),
    ('ofs_58', u32),
    ('ofs_5c', u32),
    ('ofs_60', u32),
    ('ofs_64', u32),
    ('ofs_68', u32),
    ('ofs_6c', u32),
    ('bdrdma_reserved_cntrl', u32),
    ('bdrdma_flow_reserved_cntrl', u32),
    ('bdrdma_corruption_en_ctrl', u32),
    ('ofs_7c', u32),
]
class bufman_mode(Structure):
    pass
class N11bufman_mode3DOT_7E(Union):
    pass
class N11bufman_mode3DOT_73DOT_8E(Structure):
    pass
N11bufman_mode3DOT_73DOT_8E._fields_ = [
    ('txfifo_underrun_protection', u32, 1),
    ('reserved', u32, 25),
    ('reset_rxmbuf_pointer', u32, 1),
    ('mbuf_low_attention_enable', u32, 1),
    ('test_mode', u32, 1),
    ('attention_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
N11bufman_mode3DOT_7E._anonymous_ = ['_0']
N11bufman_mode3DOT_7E._fields_ = [
    ('_0', N11bufman_mode3DOT_73DOT_8E),
    ('word', u32),
]
bufman_mode._anonymous_ = ['_0']
bufman_mode._fields_ = [
    ('_0', N11bufman_mode3DOT_7E),
]
class bufman_status(Structure):
    pass
bufman_status._fields_ = [
    ('test_mode', u32, 27),
    ('mbuf_low_attention', u32, 1),
    ('reserved', u32, 1),
    ('error', u32, 1),
    ('reserved2', u32, 2),
]
class bufman_mbuf_pool_bar(Structure):
    pass
bufman_mbuf_pool_bar._fields_ = [
    ('reserved', u32, 9),
    ('mbuf_base_addr', u32, 23),
]
class bufman_mbuf_pool_length(Structure):
    pass
bufman_mbuf_pool_length._fields_ = [
    ('reserved', u32, 9),
    ('mbuf_length', u32, 23),
]
class bufman_rdma_mbuf_low_watermark(Structure):
    pass
bufman_rdma_mbuf_low_watermark._fields_ = [
    ('reserved', u32, 26),
    ('count', u32, 6),
]
class bufman_dma_mbuf_low_watermark(Structure):
    pass
bufman_dma_mbuf_low_watermark._fields_ = [
    ('reserved', u32, 23),
    ('count', u32, 9),
]
class bufman_mbuf_high_watermark(Structure):
    pass
bufman_mbuf_high_watermark._fields_ = [
    ('reserved', u32, 23),
    ('count', u32, 9),
]
class bufman_risc_mbuf_cluster_allocation_request(Structure):
    pass
bufman_risc_mbuf_cluster_allocation_request._fields_ = [
    ('allocation_request', u32, 1),
    ('reserved', u32, 31),
]
class bufman_risc_mbuf_cluster_allocation_response(Structure):
    pass
bufman_risc_mbuf_cluster_allocation_response._fields_ = [
    ('mbuf', u32),
]
class bufman_hardware_diagnostic_1(Structure):
    pass
bufman_hardware_diagnostic_1._fields_ = [
    ('reserved', u32, 6),
    ('last_txmbuf_deallocation_head_ptr', u32, 6),
    ('reserved2', u32, 4),
    ('last_txmbuf_deallocation_tail_ptr', u32, 6),
    ('reserved3', u32, 4),
    ('next_txmbuf_allocation_ptr', u32, 6),
]
class bufman_hardware_diagnostic_2(Structure):
    pass
bufman_hardware_diagnostic_2._fields_ = [
    ('reserved', u32, 7),
    ('rxmbuf_count', u32, 9),
    ('reserved2', u32, 1),
    ('txmbuf_count', u32, 6),
    ('rxmbuf_left', u32, 9),
]
class bufman_hardware_diagnostic_3(Structure):
    pass
bufman_hardware_diagnostic_3._fields_ = [
    ('reserved', u32, 7),
    ('next_rxmbuf_deallocation_ptr', u32, 9),
    ('reserved2', u32, 7),
    ('next_rxmbuf_allocation_ptr', u32, 9),
]
class bufman_receive_flow_threshold(Structure):
    pass
bufman_receive_flow_threshold._fields_ = [
    ('reserved', u32, 23),
    ('mbuf_threshold', u32, 9),
]
class bufman_regs(Structure):
    pass
bufman_regs._fields_ = [
    ('mode', bufman_mode),
    ('status', bufman_status),
    ('mbuf_pool_base_address', bufman_mbuf_pool_bar),
    ('mbuf_pool_length', bufman_mbuf_pool_length),
    ('rdma_mbuf_low_watermark', bufman_rdma_mbuf_low_watermark),
    ('dma_mbuf_low_watermark', bufman_dma_mbuf_low_watermark),
    ('mbuf_high_watermark', bufman_mbuf_high_watermark),
    ('rx_risc_mbuf_cluster_allocation_request', bufman_risc_mbuf_cluster_allocation_request),
    ('rx_risc_mbuf_cluster_allocation_response', bufman_risc_mbuf_cluster_allocation_response),
    ('tx_risc_mbuf_cluster_allocation_request', bufman_risc_mbuf_cluster_allocation_request),
    ('tx_risc_mbuf_cluster_allocation_response', bufman_risc_mbuf_cluster_allocation_response),
    ('dma_desc_pool_addr', u32),
    ('dma_desc_pool_size', u32),
    ('dma_low_water', u32),
    ('dma_high_water', u32),
    ('rx_dma_alloc_request', u32),
    ('rx_dma_alloc_response', u32),
    ('tx_dma_alloc_request', u32),
    ('tx_dma_alloc_response', u32),
    ('hardware_diagnostic_1', bufman_hardware_diagnostic_1),
    ('hardware_diagnostic_2', bufman_hardware_diagnostic_2),
    ('hardware_diagnostic_3', bufman_hardware_diagnostic_3),
    ('receive_flow_threshold', bufman_receive_flow_threshold),
]
class cfg_port_cap_ctrl(Structure):
    pass
cfg_port_cap_ctrl._fields_ = [
    ('unknown4', u32, 28),
    ('pm_en', u32, 1),
    ('vpd_en', u32, 1),
    ('msi_en', u32, 1),
    ('msix_en', u32, 1),
]
class cfg_port_bar_ctrl(Structure):
    pass
cfg_port_bar_ctrl._fields_ = [
    ('unknown12', u32, 20),
    ('rom_bar_sz', u32, 4),
    ('unknown4', u32, 3),
    ('bar0_64bit', u32, 1),
    ('bar0_sz', u32, 4),
]
class cfg_port_pci_id(Structure):
    pass
class N15cfg_port_pci_id3DOT_9E(Union):
    pass
class N15cfg_port_pci_id3DOT_94DOT_10E(Structure):
    pass
N15cfg_port_pci_id3DOT_94DOT_10E._fields_ = [
    ('vid', u16),
    ('did', u16),
]
N15cfg_port_pci_id3DOT_9E._anonymous_ = ['_0']
N15cfg_port_pci_id3DOT_9E._fields_ = [
    ('_0', N15cfg_port_pci_id3DOT_94DOT_10E),
    ('word', u32),
]
cfg_port_pci_id._anonymous_ = ['_0']
cfg_port_pci_id._fields_ = [
    ('_0', N15cfg_port_pci_id3DOT_9E),
]
class cfg_port_pci_sid(Structure):
    pass
class N16cfg_port_pci_sid4DOT_11E(Union):
    pass
class N16cfg_port_pci_sid4DOT_114DOT_12E(Structure):
    pass
N16cfg_port_pci_sid4DOT_114DOT_12E._fields_ = [
    ('ssid', u16),
    ('svid', u16),
]
N16cfg_port_pci_sid4DOT_11E._anonymous_ = ['_0']
N16cfg_port_pci_sid4DOT_11E._fields_ = [
    ('_0', N16cfg_port_pci_sid4DOT_114DOT_12E),
    ('word', u32),
]
cfg_port_pci_sid._anonymous_ = ['_0']
cfg_port_pci_sid._fields_ = [
    ('_0', N16cfg_port_pci_sid4DOT_11E),
]
class cfg_port_pci_class(Structure):
    pass
class N18cfg_port_pci_class4DOT_13E(Union):
    pass
class N18cfg_port_pci_class4DOT_134DOT_14E(Structure):
    pass
N18cfg_port_pci_class4DOT_134DOT_14E._fields_ = [
    ('unknown24', u32, 8),
    ('class_code', u32, 8),
    ('subclass_code', u32, 8),
    ('unknown0', u32, 8),
]
N18cfg_port_pci_class4DOT_13E._anonymous_ = ['_0']
N18cfg_port_pci_class4DOT_13E._fields_ = [
    ('_0', N18cfg_port_pci_class4DOT_134DOT_14E),
    ('word', u32),
]
cfg_port_pci_class._anonymous_ = ['_0']
cfg_port_pci_class._fields_ = [
    ('_0', N18cfg_port_pci_class4DOT_13E),
]
class cfg_port_regs(Structure):
    pass
cfg_port_regs._fields_ = [
    ('ofs_00', u32),
    ('ofs_04', u32),
    ('bar_ctrl', cfg_port_bar_ctrl),
    ('ofs_0c', u32),
    ('ofs_10', u32),
    ('ofs_14', u32),
    ('ofs_18', u32),
    ('ofs_1c', u32),
    ('ofs_20', u32),
    ('ofs_24', u32),
    ('ofs_28', u32),
    ('ofs_2c', u32),
    ('ofs_30', u32),
    ('pci_id', cfg_port_pci_id),
    ('pci_sid', cfg_port_pci_sid),
    ('pci_class', cfg_port_pci_class),
    ('cap_ctrl', cfg_port_cap_ctrl),
    ('ofs_44', u32),
    ('ofs_48', u32),
    ('ofs_4c', u32),
    ('ofs_50', u32),
    ('ofs_54', u32),
    ('ofs_58', u32),
    ('ofs_5c', u32),
    ('ofs_60', u32),
    ('ofs_64', u32),
    ('ofs_68', u32),
    ('ofs_6c', u32),
    ('ofs_70', u32),
    ('ofs_74', u32),
    ('ofs_78', u32),
    ('ofs_7c', u32),
    ('ofs_80', u32),
    ('ofs_84', u32),
    ('ofs_88', u32),
    ('ofs_8c', u32),
    ('ofs_90', u32),
    ('ofs_94', u32),
    ('ofs_98', u32),
    ('ofs_9c', u32),
    ('ofs_a0', u32),
    ('ofs_a4', u32),
    ('ofs_a8', u32),
    ('ofs_ac', u32),
    ('ofs_b0', u32),
    ('ofs_b4', u32),
    ('ofs_b8', u32),
    ('ofs_bc', u32),
    ('ofs_c0', u32),
    ('ofs_c4', u32),
    ('ofs_c8', u32),
    ('ofs_cc', u32),
    ('ofs_d0', u32),
    ('ofs_d4', u32),
    ('ofs_d8', u32),
    ('ofs_dc', u32),
    ('ofs_e0', u32),
    ('ofs_e4', u32),
    ('ofs_e8', u32),
    ('ofs_ec', u32),
    ('ofs_f0', u32),
    ('ofs_f4', u32),
    ('ofs_f8', u32),
    ('ofs_fc', u32),
    ('ofs_100', u32),
    ('ofs_104', u32),
    ('ofs_108', u32),
    ('ofs_10c', u32),
    ('ofs_110', u32),
    ('ofs_114', u32),
    ('ofs_118', u32),
    ('ofs_11c', u32),
    ('ofs_120', u32),
    ('ofs_124', u32),
    ('ofs_128', u32),
    ('ofs_12c', u32),
    ('ofs_130', u32),
    ('ofs_134', u32),
    ('ofs_138', u32),
    ('ofs_13c', u32),
    ('ofs_140', u32),
    ('ofs_144', u32),
    ('ofs_148', u32),
    ('ofs_14c', u32),
    ('ofs_150', u32),
    ('ofs_154', u32),
    ('ofs_158', u32),
    ('ofs_15c', u32),
    ('ofs_160', u32),
    ('ofs_164', u32),
    ('ofs_168', u32),
    ('ofs_16c', u32),
    ('ofs_170', u32),
    ('ofs_174', u32),
    ('ofs_178', u32),
    ('ofs_17c', u32),
    ('ofs_180', u32),
    ('ofs_184', u32),
    ('ofs_188', u32),
    ('ofs_18c', u32),
    ('ofs_190', u32),
    ('ofs_194', u32),
    ('ofs_198', u32),
    ('ofs_19c', u32),
    ('ofs_1a0', u32),
    ('ofs_1a4', u32),
    ('ofs_1a8', u32),
    ('ofs_1ac', u32),
    ('ofs_1b0', u32),
    ('ofs_1b4', u32),
    ('ofs_1b8', u32),
    ('ofs_1bc', u32),
    ('ofs_1c0', u32),
    ('ofs_1c4', u32),
    ('ofs_1c8', u32),
    ('ofs_1cc', u32),
    ('ofs_1d0', u32),
    ('ofs_1d4', u32),
    ('ofs_1d8', u32),
    ('ofs_1dc', u32),
    ('ofs_1e0', u32),
    ('ofs_1e4', u32),
    ('ofs_1e8', u32),
    ('ofs_1ec', u32),
    ('ofs_1f0', u32),
    ('ofs_1f4', u32),
    ('ofs_1f8', u32),
    ('ofs_1fc', u32),
    ('ofs_200', u32),
    ('ofs_204', u32),
    ('ofs_208', u32),
    ('ofs_20c', u32),
    ('ofs_210', u32),
    ('ofs_214', u32),
    ('ofs_218', u32),
    ('ofs_21c', u32),
    ('ofs_220', u32),
    ('ofs_224', u32),
    ('ofs_228', u32),
    ('ofs_22c', u32),
    ('ofs_230', u32),
    ('ofs_234', u32),
    ('ofs_238', u32),
    ('ofs_23c', u32),
    ('ofs_240', u32),
    ('ofs_244', u32),
    ('ofs_248', u32),
    ('ofs_24c', u32),
    ('ofs_250', u32),
    ('ofs_254', u32),
    ('ofs_258', u32),
    ('ofs_25c', u32),
    ('ofs_260', u32),
    ('ofs_264', u32),
    ('ofs_268', u32),
    ('ofs_26c', u32),
    ('ofs_270', u32),
    ('ofs_274', u32),
    ('ofs_278', u32),
    ('ofs_27c', u32),
    ('ofs_280', u32),
    ('ofs_284', u32),
    ('ofs_288', u32),
    ('ofs_28c', u32),
    ('ofs_290', u32),
    ('ofs_294', u32),
    ('ofs_298', u32),
    ('ofs_29c', u32),
    ('ofs_2a0', u32),
    ('ofs_2a4', u32),
    ('ofs_2a8', u32),
    ('ofs_2ac', u32),
    ('ofs_2b0', u32),
    ('ofs_2b4', u32),
    ('ofs_2b8', u32),
    ('ofs_2bc', u32),
    ('ofs_2c0', u32),
    ('ofs_2c4', u32),
    ('ofs_2c8', u32),
    ('ofs_2cc', u32),
    ('ofs_2d0', u32),
    ('ofs_2d4', u32),
    ('ofs_2d8', u32),
    ('ofs_2dc', u32),
    ('ofs_2e0', u32),
    ('ofs_2e4', u32),
    ('ofs_2e8', u32),
    ('ofs_2ec', u32),
    ('ofs_2f0', u32),
    ('ofs_2f4', u32),
    ('ofs_2f8', u32),
    ('ofs_2fc', u32),
    ('ofs_300', u32),
    ('ofs_304', u32),
    ('ofs_308', u32),
    ('ofs_30c', u32),
    ('ofs_310', u32),
    ('ofs_314', u32),
    ('ofs_318', u32),
    ('ofs_31c', u32),
    ('ofs_320', u32),
    ('ofs_324', u32),
    ('ofs_328', u32),
    ('ofs_32c', u32),
    ('ofs_330', u32),
    ('ofs_334', u32),
    ('ofs_338', u32),
    ('ofs_33c', u32),
    ('ofs_340', u32),
    ('ofs_344', u32),
    ('ofs_348', u32),
    ('ofs_34c', u32),
    ('ofs_350', u32),
    ('ofs_354', u32),
    ('ofs_358', u32),
    ('ofs_35c', u32),
    ('ofs_360', u32),
    ('ofs_364', u32),
    ('ofs_368', u32),
    ('ofs_36c', u32),
    ('ofs_370', u32),
    ('ofs_374', u32),
    ('ofs_378', u32),
    ('ofs_37c', u32),
    ('ofs_380', u32),
    ('ofs_384', u32),
    ('ofs_388', u32),
    ('ofs_38c', u32),
    ('ofs_390', u32),
    ('ofs_394', u32),
    ('ofs_398', u32),
    ('ofs_39c', u32),
    ('ofs_3a0', u32),
    ('ofs_3a4', u32),
    ('ofs_3a8', u32),
    ('ofs_3ac', u32),
    ('ofs_3b0', u32),
    ('ofs_3b4', u32),
    ('ofs_3b8', u32),
    ('ofs_3bc', u32),
    ('ofs_3c0', u32),
    ('ofs_3c4', u32),
    ('ofs_3c8', u32),
    ('ofs_3cc', u32),
    ('ofs_3d0', u32),
    ('ofs_3d4', u32),
    ('ofs_3d8', u32),
    ('ofs_3dc', u32),
    ('ofs_3e0', u32),
    ('ofs_3e4', u32),
    ('ofs_3e8', u32),
    ('ofs_3ec', u32),
    ('ofs_3f0', u32),
    ('ofs_3f4', u32),
    ('ofs_3f8', u32),
    ('ofs_3fc', u32),
]
class cpmu_control(Structure):
    pass
cpmu_control._fields_ = [
    ('reserved31', u32, 1),
    ('reserved30', u32, 1),
    ('reserved29', u32, 1),
    ('always_force_gphy_dll_on', u32, 1),
    ('enable_gphy_powerdown_in_dou', u32, 1),
    ('reserved26', u32, 1),
    ('reserved25', u32, 1),
    ('reserved24', u32, 1),
    ('reserved23', u32, 1),
    ('sw_ctrl_ape_reset', u32, 1),
    ('sw_ctrl_core_reset', u32, 1),
    ('media_sense_power_mode_enable', u32, 1),
    ('reserved19', u32, 1),
    ('legacy_timer_enable', u32, 1),
    ('frequency_multiplier_enable', u32, 1),
    ('gphy_10mb_receive_only_mode_enable', u32, 1),
    ('play_dead_mode_enable', u32, 1),
    ('link_speed_power_mode_enable', u32, 1),
    ('hide_pcie_function', u32, 3),
    ('link_aware_power_mode_enable', u32, 1),
    ('link_idle_power_mode_enable', u32, 1),
    ('card_reader_idle_enable', u32, 1),
    ('card_read_iddq', u32, 1),
    ('lan_iddq', u32, 1),
    ('ape_deep_sleep_mode_en', u32, 1),
    ('ape_sleep_mode_en', u32, 1),
    ('reserved3', u32, 1),
    ('power_down', u32, 1),
    ('register_software_reset', u32, 1),
    ('software_reset', u32, 1),
]
class cpmu_clock(Structure):
    pass
cpmu_clock._fields_ = [
    ('reserved21', u32, 11),
    ('mac_clock_switch', u32, 5),
    ('reserved13', u32, 3),
    ('ape_clock_switch', u32, 5),
    ('reserved0', u32, 8),
]
class cpmu_override(Structure):
    pass
cpmu_override._fields_ = [
    ('reserved', u32, 18),
    ('mac_clock_speed_override_enable', u32, 1),
    ('reserved2', u32, 13),
]
class cpmu_status(Structure):
    pass
cpmu_status._fields_ = [
    ('reserved', u32, 9),
    ('wol_acpi_detection_enabled', u32, 1),
    ('wol_magic_packet_detection_enabled', u32, 1),
    ('ethernet_link', u32, 2),
    ('link_idle', u32, 1),
    ('reserved2', u32, 2),
    ('reserved3', u32, 2),
    ('vmain_power', u32, 1),
    ('iddq', u32, 3),
    ('power_state', u32, 2),
    ('energy_detect', u32, 1),
    ('cpmu_power', u32, 3),
    ('pm_state_machine_state', u32, 4),
]
class cpmu_clock_status(Structure):
    pass
cpmu_clock_status._fields_ = [
    ('reserved30', u32, 2),
    ('flash_clk_dis', u32, 1),
    ('reserved26', u32, 3),
    ('ape_hclk_dis', u32, 1),
    ('ape_fclk_dis', u32, 1),
    ('reserved21', u32, 3),
    ('mac_clk_sw', u32, 5),
    ('reserved13', u32, 3),
    ('ape_clk_sw', u32, 5),
    ('reserved7', u32, 1),
    ('flash_clk_sw', u32, 3),
    ('reserved0', u32, 4),
]
class cpmu_pcie_status(Structure):
    pass
cpmu_pcie_status._fields_ = [
    ('dl_active', u32, 1),
    ('debug_vector_sel_2', u32, 4),
    ('debug_vector_2', u32, 11),
    ('phylinkup', u32, 1),
    ('debug_vector_sel_1', u32, 4),
    ('debug_vector_1', u32, 11),
]
class cpmu_gphy_control_status(Structure):
    pass
cpmu_gphy_control_status._fields_ = [
    ('logan_sku', u32, 3),
    ('reserved14', u32, 15),
    ('gphy_10mb_rcv_only_mode_tx_idle_debounce_timer', u32, 2),
    ('reserved11', u32, 1),
    ('dll_iddq_state', u32, 1),
    ('pwrdn', u32, 1),
    ('set_bias_iddq', u32, 1),
    ('force_dll_on', u32, 1),
    ('dll_pwrdn_ok', u32, 1),
    ('sw_ctrl_por', u32, 1),
    ('reset_ctrl', u32, 1),
    ('reserved3', u32, 1),
    ('dll_handshaking_disable', u32, 1),
    ('bias_iddq', u32, 1),
    ('phy_iddq', u32, 1),
]
class cpmu_ram_control(Structure):
    pass
cpmu_ram_control._fields_ = [
    ('core_ram_power_down', u32, 1),
    ('bd_ram_power_down', u32, 1),
    ('reserved22', u32, 8),
    ('disable_secure_fw_loading_status', u32, 1),
    ('remove_lan_function', u32, 1),
    ('reserved18', u32, 2),
    ('hide_function_7', u32, 1),
    ('hide_function_6', u32, 1),
    ('hide_function_5', u32, 1),
    ('hide_function_4', u32, 1),
    ('hide_function_3', u32, 1),
    ('hide_function_2', u32, 1),
    ('hide_function_1', u32, 1),
    ('hide_function_0', u32, 1),
    ('reserved8', u32, 2),
    ('ram_bank7_dis', u32, 1),
    ('ram_bank6_dis', u32, 1),
    ('ram_bank5_dis', u32, 1),
    ('ram_bank4_dis', u32, 1),
    ('ram_bank3_dis', u32, 1),
    ('ram_bank2_dis', u32, 1),
    ('ram_bank1_dis', u32, 1),
    ('ram_bank0_dis', u32, 1),
]
class cpmu_cr_idle_det_debounce_ctrl(Structure):
    pass
cpmu_cr_idle_det_debounce_ctrl._fields_ = [
    ('reserved16', u32, 16),
    ('timer', u32, 16),
]
class cpmu_core_idle_det_debounce_ctrl(Structure):
    pass
cpmu_core_idle_det_debounce_ctrl._fields_ = [
    ('reserved8', u32, 24),
    ('timer', u32, 8),
]
class cpmu_pcie_idle_det_debounce_ctrl(Structure):
    pass
cpmu_pcie_idle_det_debounce_ctrl._fields_ = [
    ('reserved8', u32, 24),
    ('timer', u32, 8),
]
class cpmu_energy_det_debounce_ctrl(Structure):
    pass
cpmu_energy_det_debounce_ctrl._fields_ = [
    ('reserved10', u32, 22),
    ('energy_detect_select', u32, 1),
    ('select_hw_energy_det', u32, 1),
    ('select_sw_hw_oring_energy_det', u32, 1),
    ('sw_force_energy_det_value', u32, 1),
    ('disable_energy_det_debounce_low', u32, 1),
    ('disable_energy_det_debounce_high', u32, 1),
    ('energy_det_debounce_high_limit', u32, 2),
    ('energy_det_debounce_low_limit', u32, 2),
]
class cpmu_dll_lock_timer(Structure):
    pass
cpmu_dll_lock_timer._fields_ = [
    ('reserved12', u32, 20),
    ('gphy_dll_lock_dimer_enable', u32, 1),
    ('gphy_dll_lock_timer', u32, 11),
]
class cpmu_chip_id(Structure):
    pass
cpmu_chip_id._fields_ = [
    ('chip_id_hi', u32, 4),
    ('chip_id_lo', u32, 16),
    ('base_layer_revision', u32, 4),
    ('metal_layer_revision', u32, 8),
]
class cpmu_mutex(Structure):
    pass
cpmu_mutex._fields_ = [
    ('reserved13', u32, 19),
    ('req_12', u32, 1),
    ('reserved9', u32, 3),
    ('req_8', u32, 1),
    ('reserved5', u32, 3),
    ('req_4', u32, 1),
    ('reserved3', u32, 1),
    ('req_2', u32, 1),
    ('reserved0', u32, 2),
]
class cpmu_padring_control(Structure):
    pass
cpmu_padring_control._fields_ = [
    ('power_sm_or_state', u32, 4),
    ('power_sm_override', u32, 1),
    ('cr_io_hys_en', u32, 1),
    ('cr_activity_led_en', u32, 1),
    ('switching_regulator_power_off_option', u32, 1),
    ('cr_bus_power_dis', u32, 1),
    ('unknown', u32, 3),
    ('pcie_serdes_pll_tuning_bypass', u32, 1),
    ('pcie_serdes_lfck_rx_select_cnt0', u32, 1),
    ('pcie_serdes_lfck_rx_select_refclk', u32, 1),
    ('reserved', u32, 1),
    ('clkreq_l_in_low_power_mode_improvement', u32, 1),
    ('cq31984_opt_2_fix_disable', u32, 1),
    ('serdes_standalone_mode', u32, 1),
    ('pipe_standalone_mode_control', u32, 1),
    ('cq31984_opt_4_fix_enable', u32, 1),
    ('cq31177_fix_disable', u32, 1),
    ('cq30674_fix_enable', u32, 1),
    ('chicken_bit_for_cq31116', u32, 1),
    ('cq31984_opt_3_fix_disable', u32, 1),
    ('disable_default_gigabit_advertisement', u32, 1),
    ('enable_gphy_reset_on_perst_l_deassertion', u32, 1),
    ('cq39842_fix_disable', u32, 1),
    ('cq39544_fix_disable', u32, 1),
    ('reserved2', u32, 1),
    ('eclk_switch_using_link_status_disable', u32, 1),
    ('perst_l_pad_hysteris_enable', u32, 1),
]
class cpmu_regs(Structure):
    pass
cpmu_regs._fields_ = [
    ('control', cpmu_control),
    ('no_link_or_10mb_policy', cpmu_clock),
    ('megabit_policy', cpmu_clock),
    ('gigabit_policy', cpmu_clock),
    ('link_aware_policy', cpmu_clock),
    ('d0u_policy', cpmu_clock),
    ('link_idle_policy', cpmu_clock),
    ('ofs_1c', u32),
    ('ofs_20', u32),
    ('override_policy', cpmu_clock),
    ('override_enable', cpmu_override),
    ('status', cpmu_status),
    ('clock_status', cpmu_clock_status),
    ('pcie_status', cpmu_pcie_status),
    ('gphy_control_status', cpmu_gphy_control_status),
    ('ram_control', cpmu_ram_control),
    ('cr_idle_detect_debounce_ctrl', cpmu_cr_idle_det_debounce_ctrl),
    ('eee_debug', u32),
    ('core_idle_detect_debounce_ctrl', cpmu_core_idle_det_debounce_ctrl),
    ('pcie_idle_detect_debounce_ctrl', cpmu_pcie_idle_det_debounce_ctrl),
    ('energy_detect_debounce_timer', cpmu_energy_det_debounce_ctrl),
    ('dll_lock_timer', cpmu_dll_lock_timer),
    ('chip_id', cpmu_chip_id),
    ('mutex_request', cpmu_mutex),
    ('mutex_grant', cpmu_mutex),
    ('ofs_64', u32),
    ('padring_control', cpmu_padring_control),
    ('ofs_6c', u32),
    ('link_idle_control', u32),
    ('link_idle_status', u32),
    ('play_dead_mode_iddq_debounce_control', u32),
    ('top_misc_control_1', u32),
    ('debug_bus', u32),
    ('debug_select', u32),
    ('ofs_88', u32),
    ('ofs_8c', u32),
    ('ltr_control', u32),
    ('ofs_94', u32),
    ('ofs_98', u32),
    ('ofs_9c', u32),
    ('swregulator_control_1', u32),
    ('swregulator_control_2', u32),
    ('swregulator_control_3', u32),
    ('misc_control', u32),
    ('eee_mode', u32),
    ('eee_debounce_timer1_control', u32),
    ('eee_debounce_timer2_control', u32),
    ('eee_link_idle_control', u32),
    ('eee_link_idle_status', u32),
    ('eee_statistic_counter_1', u32),
    ('eee_statistic_counter_2', u32),
    ('eee_statistic_counter_3', u32),
    ('eee_control', u32),
    ('current_measurement_control', u32),
    ('current_measurement_read_upper', u32),
    ('current_measurement_read_lower', u32),
    ('card_reader_idle_control', u32),
    ('card_reader_clock_policy', u32),
    ('card_reader_clock_status', u32),
    ('ofs_ec', u32),
    ('pll_control_1', u32),
    ('pll_control_2', u32),
    ('pll_control_3', u32),
    ('clock_gen_control', u32),
]
class cpu_mode(Structure):
    pass
cpu_mode._fields_ = [
    ('reserved15', u32, 17),
    ('register_addr_trap_halt_en', u32, 1),
    ('memory_addr_trap_halt_en', u32, 1),
    ('invalid_instruction_fetch_halt_en', u32, 1),
    ('invalid_data_access_halt_en', u32, 1),
    ('halt', u32, 1),
    ('flush_icache', u32, 1),
    ('icache_pref_en', u32, 1),
    ('watchdog_en', u32, 1),
    ('rom_fail', u32, 1),
    ('data_cache_en', u32, 1),
    ('write_post_en', u32, 1),
    ('page_0_instr_halt_en', u32, 1),
    ('page_0_data_halt_en', u32, 1),
    ('single_step', u32, 1),
    ('reset', u32, 1),
]
class cpu_status(Structure):
    pass
class N10cpu_status4DOT_15E(Union):
    pass
class N10cpu_status4DOT_154DOT_16E(Structure):
    pass
N10cpu_status4DOT_154DOT_16E._fields_ = [
    ('blocking_read', u32, 1),
    ('ma_request_fifo_overflow', u32, 1),
    ('ma_data_bytemask_fifo_overflow', u32, 1),
    ('ma_outstanding_read_fifo_overflow', u32, 1),
    ('ma_outstanding_write_fifo_overflow', u32, 1),
    ('reserved16', u32, 11),
    ('instruction_fetch_stall', u32, 1),
    ('data_access_stall', u32, 1),
    ('reserved13', u32, 1),
    ('interrupt_received', u32, 1),
    ('reserved11', u32, 1),
    ('halted', u32, 1),
    ('register_address_trap', u32, 1),
    ('memory_address_trap', u32, 1),
    ('bad_memory_alignment', u32, 1),
    ('invalid_instruction_fetch', u32, 1),
    ('invalid_data_access', u32, 1),
    ('page_0_instr_reference', u32, 1),
    ('page_0_data_reference', u32, 1),
    ('invalid_instruction', u32, 1),
    ('halt_instruction_executed', u32, 1),
    ('hardware_breakpoint', u32, 1),
]
N10cpu_status4DOT_15E._anonymous_ = ['_0']
N10cpu_status4DOT_15E._fields_ = [
    ('_0', N10cpu_status4DOT_154DOT_16E),
    ('word', u32),
]
cpu_status._anonymous_ = ['_0']
cpu_status._fields_ = [
    ('_0', N10cpu_status4DOT_15E),
]
class cpu_event_mask(Structure):
    pass
cpu_event_mask._fields_ = [
    ('unknown', u32, 18),
    ('reserved13', u32, 1),
    ('interrupt', u32, 1),
    ('spad_underflow', u32, 1),
    ('soft_halted', u32, 1),
    ('reserved9', u32, 1),
    ('fio_abort', u32, 1),
    ('align_halted', u32, 1),
    ('bad_pc_halted', u32, 1),
    ('bad_data_addr_halted', u32, 1),
    ('page_0_instr_halted', u32, 1),
    ('page_0_data_halted', u32, 1),
    ('bad_instr_halted', u32, 1),
    ('reserved1', u32, 1),
    ('breakpoint', u32, 1),
]
class cpu_breakpoint(Structure):
    pass
class N14cpu_breakpoint4DOT_17E(Union):
    pass
class N14cpu_breakpoint4DOT_174DOT_18E(Structure):
    pass
N14cpu_breakpoint4DOT_174DOT_18E._fields_ = [
    ('addr_word', u32, 30),
    ('reserved', u32, 1),
    ('disabled', u32, 1),
]
N14cpu_breakpoint4DOT_17E._anonymous_ = ['_0']
N14cpu_breakpoint4DOT_17E._fields_ = [
    ('address', u32),
    ('_0', N14cpu_breakpoint4DOT_174DOT_18E),
]
cpu_breakpoint._anonymous_ = ['_0']
cpu_breakpoint._fields_ = [
    ('_0', N14cpu_breakpoint4DOT_17E),
]
class cpu_last_branch_address(Structure):
    pass
class N23cpu_last_branch_address4DOT_19E(Union):
    pass
class N23cpu_last_branch_address4DOT_194DOT_20E(Structure):
    pass
N23cpu_last_branch_address4DOT_194DOT_20E._fields_ = [
    ('addr_word', u32, 30),
    ('type', u32, 1),
    ('reserved', u32, 1),
]
N23cpu_last_branch_address4DOT_19E._anonymous_ = ['_0']
N23cpu_last_branch_address4DOT_19E._fields_ = [
    ('address', u32),
    ('_0', N23cpu_last_branch_address4DOT_194DOT_20E),
]
cpu_last_branch_address._anonymous_ = ['_0']
cpu_last_branch_address._fields_ = [
    ('_0', N23cpu_last_branch_address4DOT_19E),
]
class cpu_regs(Structure):
    pass
cpu_regs._fields_ = [
    ('mode', cpu_mode),
    ('status', cpu_status),
    ('mask', cpu_event_mask),
    ('ofs_0c', u32),
    ('ofs_10', u32),
    ('ofs_14', u32),
    ('ofs_18', u32),
    ('pc', u32),
    ('ir', u32),
    ('spad_uflow', u32),
    ('watchdog_enable', u32),
    ('watchdog_vector', u32),
    ('watchdog_saved_pc', u32),
    ('breakpoint', cpu_breakpoint),
    ('ofs_38', u32),
    ('ofs_3c', u32),
    ('ofs_40', u32),
    ('watchdog_saved_state', u32),
    ('lba', cpu_last_branch_address),
    ('spad_uflow_set', u32),
    ('ofs_50', u32),
    ('ofs_54', u32),
    ('ofs_58', u32),
    ('ofs_5c', u32),
    ('ofs_60', u32),
    ('ofs_64', u32),
    ('ofs_68', u32),
    ('ofs_6c', u32),
    ('ofs_70', u32),
    ('ofs_74', u32),
    ('ofs_78', u32),
    ('ofs_7c', u32),
    ('ofs_80', u32),
    ('ofs_84', u32),
    ('ofs_88', u32),
    ('ofs_8c', u32),
    ('ofs_90', u32),
    ('ofs_94', u32),
    ('ofs_98', u32),
    ('ofs_9c', u32),
    ('ofs_a0', u32),
    ('ofs_a4', u32),
    ('ofs_a8', u32),
    ('ofs_ac', u32),
    ('ofs_b0', u32),
    ('ofs_b4', u32),
    ('ofs_b8', u32),
    ('ofs_bc', u32),
    ('ofs_c0', u32),
    ('ofs_c4', u32),
    ('ofs_c8', u32),
    ('ofs_cc', u32),
    ('ofs_d0', u32),
    ('ofs_d4', u32),
    ('ofs_d8', u32),
    ('ofs_dc', u32),
    ('ofs_e0', u32),
    ('ofs_e4', u32),
    ('ofs_e8', u32),
    ('ofs_ec', u32),
    ('ofs_f0', u32),
    ('ofs_f4', u32),
    ('ofs_f8', u32),
    ('ofs_fc', u32),
    ('vcpu_status', u32),
    ('device_configuration', u32),
    ('vcpu_holding', u32),
    ('vcpu_data', u32),
    ('vcpu_debug', u32),
    ('vcpu_config_shadow_1', u32),
    ('vcpu_config_shadow_2', u32),
    ('ofs_11c', u32),
    ('ofs_120', u32),
    ('ofs_124', u32),
    ('ofs_128', u32),
    ('ofs_12c', u32),
    ('ofs_130', u32),
    ('ofs_134', u32),
    ('ofs_138', u32),
    ('ofs_13c', u32),
    ('ofs_140', u32),
    ('ofs_144', u32),
    ('ofs_148', u32),
    ('ofs_14c', u32),
    ('ofs_150', u32),
    ('ofs_154', u32),
    ('ofs_158', u32),
    ('ofs_15c', u32),
    ('ofs_160', u32),
    ('ofs_164', u32),
    ('ofs_168', u32),
    ('ofs_16c', u32),
    ('ofs_170', u32),
    ('ofs_174', u32),
    ('ofs_178', u32),
    ('ofs_17c', u32),
    ('ofs_180', u32),
    ('ofs_184', u32),
    ('ofs_188', u32),
    ('ofs_18c', u32),
    ('ofs_190', u32),
    ('ofs_194', u32),
    ('ofs_198', u32),
    ('ofs_19c', u32),
    ('ofs_1a0', u32),
    ('ofs_1a4', u32),
    ('ofs_1a8', u32),
    ('ofs_1ac', u32),
    ('ofs_1b0', u32),
    ('ofs_1b4', u32),
    ('ofs_1b8', u32),
    ('ofs_1bc', u32),
    ('ofs_1c0', u32),
    ('ofs_1c4', u32),
    ('ofs_1c8', u32),
    ('ofs_1cc', u32),
    ('ofs_1d0', u32),
    ('ofs_1d4', u32),
    ('ofs_1d8', u32),
    ('ofs_1dc', u32),
    ('ofs_1e0', u32),
    ('ofs_1e4', u32),
    ('ofs_1e8', u32),
    ('ofs_1ec', u32),
    ('ofs_1f0', u32),
    ('ofs_1f4', u32),
    ('ofs_1f8', u32),
    ('ofs_1fc', u32),
    ('r0', u32),
    ('r1', u32),
    ('r2', u32),
    ('r3', u32),
    ('r4', u32),
    ('r5', u32),
    ('r6', u32),
    ('r7', u32),
    ('r8', u32),
    ('r9', u32),
    ('r10', u32),
    ('r11', u32),
    ('r12', u32),
    ('r13', u32),
    ('r14', u32),
    ('r15', u32),
    ('r16', u32),
    ('r17', u32),
    ('r18', u32),
    ('r19', u32),
    ('r20', u32),
    ('r21', u32),
    ('r22', u32),
    ('r23', u32),
    ('r24', u32),
    ('r25', u32),
    ('r26', u32),
    ('r27', u32),
    ('r28', u32),
    ('r29', u32),
    ('r30', u32),
    ('r31', u32),
]
class cr_port_regs(Structure):
    pass
cr_port_regs._fields_ = [
    ('ofs_00', u32),
    ('ofs_04', u32),
    ('ofs_08', u32),
    ('ofs_0c', u32),
    ('ofs_10', u32),
    ('ofs_14', u32),
    ('ofs_18', u32),
    ('ofs_1c', u32),
    ('ofs_20', u32),
    ('ofs_24', u32),
    ('ofs_28', u32),
    ('ofs_2c', u32),
    ('ofs_30', u32),
    ('ofs_34', u32),
    ('ofs_38', u32),
    ('ofs_3c', u32),
    ('ofs_40', u32),
    ('ofs_44', u32),
    ('ofs_48', u32),
    ('ofs_4c', u32),
    ('ofs_50', u32),
    ('ofs_54', u32),
    ('ofs_58', u32),
    ('ofs_5c', u32),
    ('ofs_60', u32),
    ('ofs_64', u32),
    ('ofs_68', u32),
    ('ofs_6c', u32),
    ('ofs_70', u32),
    ('ofs_74', u32),
    ('ofs_78', u32),
    ('ofs_7c', u32),
    ('ofs_80', u32),
    ('ofs_84', u32),
    ('ofs_88', u32),
    ('ofs_8c', u32),
    ('ofs_90', u32),
    ('ofs_94', u32),
    ('ofs_98', u32),
    ('ofs_9c', u32),
    ('ofs_a0', u32),
    ('ofs_a4', u32),
    ('ofs_a8', u32),
    ('ofs_ac', u32),
    ('ofs_b0', u32),
    ('ofs_b4', u32),
    ('ofs_b8', u32),
    ('ofs_bc', u32),
    ('ofs_c0', u32),
    ('ofs_c4', u32),
    ('ofs_c8', u32),
    ('ofs_cc', u32),
    ('ofs_d0', u32),
    ('ofs_d4', u32),
    ('ofs_d8', u32),
    ('ofs_dc', u32),
    ('ofs_e0', u32),
    ('ofs_e4', u32),
    ('ofs_e8', u32),
    ('ofs_ec', u32),
    ('ofs_f0', u32),
    ('ofs_f4', u32),
    ('ofs_f8', u32),
    ('ofs_fc', u32),
    ('ofs_100', u32),
    ('ofs_104', u32),
    ('ofs_108', u32),
    ('ofs_10c', u32),
    ('ofs_110', u32),
    ('ofs_114', u32),
    ('ofs_118', u32),
    ('ofs_11c', u32),
    ('ofs_120', u32),
    ('ofs_124', u32),
    ('ofs_128', u32),
    ('ofs_12c', u32),
    ('ofs_130', u32),
    ('ofs_134', u32),
    ('ofs_138', u32),
    ('ofs_13c', u32),
    ('ofs_140', u32),
    ('ofs_144', u32),
    ('ofs_148', u32),
    ('ofs_14c', u32),
    ('ofs_150', u32),
    ('ofs_154', u32),
    ('ofs_158', u32),
    ('ofs_15c', u32),
    ('ofs_160', u32),
    ('ofs_164', u32),
    ('ofs_168', u32),
    ('ofs_16c', u32),
    ('ofs_170', u32),
    ('ofs_174', u32),
    ('ofs_178', u32),
    ('ofs_17c', u32),
    ('ofs_180', u32),
    ('ofs_184', u32),
    ('ofs_188', u32),
    ('ofs_18c', u32),
    ('ofs_190', u32),
    ('ofs_194', u32),
    ('ofs_198', u32),
    ('ofs_19c', u32),
    ('ofs_1a0', u32),
    ('ofs_1a4', u32),
    ('ofs_1a8', u32),
    ('ofs_1ac', u32),
    ('ofs_1b0', u32),
    ('ofs_1b4', u32),
    ('ofs_1b8', u32),
    ('ofs_1bc', u32),
    ('ofs_1c0', u32),
    ('ofs_1c4', u32),
    ('ofs_1c8', u32),
    ('ofs_1cc', u32),
    ('ofs_1d0', u32),
    ('ofs_1d4', u32),
    ('ofs_1d8', u32),
    ('ofs_1dc', u32),
    ('ofs_1e0', u32),
    ('ofs_1e4', u32),
    ('ofs_1e8', u32),
    ('ofs_1ec', u32),
    ('ofs_1f0', u32),
    ('ofs_1f4', u32),
    ('ofs_1f8', u32),
    ('ofs_1fc', u32),
]
class dma_desc(Structure):
    pass
class N8dma_desc4DOT_23E(Structure):
    pass
N8dma_desc4DOT_23E._fields_ = [
    ('length', u32, 16),
    ('cqid_sqid', u32, 16),
]
dma_desc._anonymous_ = ['_0']
dma_desc._fields_ = [
    ('addr_hi', u32),
    ('addr_lo', u32),
    ('nic_mbuf', u32),
    ('_0', N8dma_desc4DOT_23E),
    ('flags', u32),
    ('opaque1', u32),
    ('opaque2', u32),
    ('opaque3', u32),
]
class dmac_mode(Structure):
    pass
class N9dmac_mode4DOT_21E(Union):
    pass
class N9dmac_mode4DOT_214DOT_22E(Structure):
    pass
N9dmac_mode4DOT_214DOT_22E._fields_ = [
    ('reserved', u32, 30),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
N9dmac_mode4DOT_21E._anonymous_ = ['_0']
N9dmac_mode4DOT_21E._fields_ = [
    ('_0', N9dmac_mode4DOT_214DOT_22E),
    ('word', u32),
]
dmac_mode._anonymous_ = ['_0']
dmac_mode._fields_ = [
    ('_0', N9dmac_mode4DOT_21E),
]
class dmac_regs(Structure):
    pass
dmac_regs._fields_ = [
    ('mode', dmac_mode),
]
class emac_mode(Structure):
    pass
emac_mode._fields_ = [
    ('ext_magic_pkt_en', u32, 1),
    ('magic_pkt_free_running_mode_en', u32, 1),
    ('mac_loop_back_mode_ctrl', u32, 1),
    ('en_ape_tx_path', u32, 1),
    ('en_ape_rx_path', u32, 1),
    ('free_running_acpi', u32, 1),
    ('halt_interesting_packets_pme', u32, 1),
    ('keep_frame_in_wol', u32, 1),
    ('en_fhde', u32, 1),
    ('en_rde', u32, 1),
    ('en_tde', u32, 1),
    ('reserved20', u32, 1),
    ('acpi_power_on', u32, 1),
    ('magic_packet_detection', u32, 1),
    ('send_config_command', u32, 1),
    ('flush_tx_statistics', u32, 1),
    ('clear_tx_statistics', u32, 1),
    ('en_tx_statistics', u32, 1),
    ('flush_rx_statistics', u32, 1),
    ('clear_rx_statistics', u32, 1),
    ('en_rx_statistics', u32, 1),
    ('reserved10', u32, 1),
    ('max_defer', u32, 1),
    ('en_tx_bursting', u32, 1),
    ('tagged_mac_control', u32, 1),
    ('reserved5', u32, 2),
    ('loopback', u32, 1),
    ('port_mode', u32, 2),
    ('half_duplex', u32, 1),
    ('global_reset', u32, 1),
]
class emac_status(Structure):
    pass
emac_status._fields_ = [
    ('reserved29', u32, 3),
    ('interesting_packet_pme_attention', u32, 1),
    ('tx_statistic_overrun', u32, 1),
    ('rx_statistic_overrun', u32, 1),
    ('odi_error', u32, 1),
    ('ap_error', u32, 1),
    ('mii_interrupt', u32, 1),
    ('mii_completion', u32, 1),
    ('reserved13', u32, 9),
    ('link_state_changed', u32, 1),
    ('reserved0', u32, 12),
]
class emac_event_enable(Structure):
    pass
emac_event_enable._fields_ = [
    ('reserved30', u32, 2),
    ('tx_offload_error_interrupt', u32, 1),
    ('interesting_packet_pme_attn_en', u32, 1),
    ('tx_statistics_overrun', u32, 1),
    ('rx_statistics_overrun', u32, 1),
    ('odi_error', u32, 1),
    ('ap_error', u32, 1),
    ('mii_interrupt', u32, 1),
    ('mii_completion', u32, 1),
    ('reserved13', u32, 9),
    ('link_state_changed', u32, 1),
    ('reserved0', u32, 12),
]
class emac_led_control(Structure):
    pass
class N16emac_led_control4DOT_24E(Union):
    pass
class N16emac_led_control4DOT_244DOT_25E(Structure):
    pass
N16emac_led_control4DOT_244DOT_25E._fields_ = [
    ('override_blink_rate', u32, 1),
    ('blink_period', u32, 12),
    ('reserved16', u32, 3),
    ('speed_10_100_mode', u32, 1),
    ('shared_traffic_link_led_mode', u32, 1),
    ('mac_mode', u32, 1),
    ('led_mode', u32, 2),
    ('traffic_led_status', u32, 1),
    ('ten_mbps_led_status', u32, 1),
    ('hundred_mbps_led_status', u32, 1),
    ('gig_mbps_led_status', u32, 1),
    ('traffic_led', u32, 1),
    ('blink_traffic_led', u32, 1),
    ('override_traffic_led', u32, 1),
    ('ten_mbps_led', u32, 1),
    ('hundred_mbps_led', u32, 1),
    ('gig_mbps_led', u32, 1),
    ('override_link_leds', u32, 1),
]
N16emac_led_control4DOT_24E._anonymous_ = ['_0']
N16emac_led_control4DOT_24E._fields_ = [
    ('_0', N16emac_led_control4DOT_244DOT_25E),
    ('word', u32),
]
emac_led_control._anonymous_ = ['_0']
emac_led_control._fields_ = [
    ('_0', N16emac_led_control4DOT_24E),
]
class transmit_mac_mode(Structure):
    pass
transmit_mac_mode._fields_ = [
    ('rr_weight', u32, 5),
    ('transmit_ftq_arbitration_mode', u32, 3),
    ('reserved21', u32, 3),
    ('txmbuf_burst_size', u32, 4),
    ('do_not_insert_gcm_gmac_iv', u32, 1),
    ('do_not_drop_packet_if_malformed', u32, 1),
    ('do_not_drop_if_sa_found_in_rx_direction', u32, 1),
    ('do_not_drop_if_unsupported_ipv6_extension_or_ipv4_option_found', u32, 1),
    ('do_not_drop_if_sa_invalid', u32, 1),
    ('do_not_drop_if_ah_esp_header_not_found', u32, 1),
    ('en_tx_ah_offload', u32, 1),
    ('en_rx_esp_offload', u32, 1),
    ('enable_bad_txmbuf_lockup_fix', u32, 1),
    ('link_aware_enable', u32, 1),
    ('enable_long_pause', u32, 1),
    ('enable_big_backoff', u32, 1),
    ('enable_flow_control', u32, 1),
    ('reserved2', u32, 2),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
class transmit_mac_status(Structure):
    pass
class N19transmit_mac_status4DOT_26E(Union):
    pass
class N19transmit_mac_status4DOT_264DOT_27E(Structure):
    pass
N19transmit_mac_status4DOT_264DOT_27E._fields_ = [
    ('reserved', u32, 26),
    ('odi_overrun', u32, 1),
    ('odi_underrun', u32, 1),
    ('link_up', u32, 1),
    ('sent_xon', u32, 1),
    ('sent_xoff', u32, 1),
    ('currently_xoffed', u32, 1),
]
N19transmit_mac_status4DOT_26E._anonymous_ = ['_0']
N19transmit_mac_status4DOT_26E._fields_ = [
    ('_0', N19transmit_mac_status4DOT_264DOT_27E),
    ('word', u32),
]
transmit_mac_status._anonymous_ = ['_0']
transmit_mac_status._fields_ = [
    ('_0', N19transmit_mac_status4DOT_26E),
]
class transmit_mac_lengths(Structure):
    pass
transmit_mac_lengths._fields_ = [
    ('reserved', u32, 18),
    ('ipg_crs', u32, 2),
    ('ipg', u32, 4),
    ('slot', u32, 8),
]
class receive_mac_mode(Structure):
    pass
receive_mac_mode._fields_ = [
    ('disable_hw_fix_24175', u32, 1),
    ('disable_hw_fix_29914', u32, 1),
    ('disable_8023_len_chk_fix', u32, 1),
    ('reserved28', u32, 1),
    ('reserved27', u32, 1),
    ('status_ready_new_disable', u32, 1),
    ('ipv4_frag_fix', u32, 1),
    ('ipv6_enable', u32, 1),
    ('rss_enable', u32, 1),
    ('rss_hash_mask_bits', u32, 3),
    ('rss_tcpipv6_hash_enable', u32, 1),
    ('rss_ipv6_hash_enable', u32, 1),
    ('rss_tcpipv4_hash_enable', u32, 1),
    ('rss_ipv4_hash_enable', u32, 1),
    ('reserved14', u32, 2),
    ('ape_promisc_mode_en', u32, 1),
    ('cq42199_fix_dis', u32, 1),
    ('filter_broadcast', u32, 1),
    ('keep_vlan_tag_diag', u32, 1),
    ('no_crc_check', u32, 1),
    ('promiscuous_mode', u32, 1),
    ('length_check', u32, 1),
    ('accept_runts', u32, 1),
    ('keep_oversized', u32, 1),
    ('keep_pause', u32, 1),
    ('keep_mfc', u32, 1),
    ('enable_flow_control', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
class receive_mac_status(Structure):
    pass
class N18receive_mac_status4DOT_28E(Union):
    pass
class N18receive_mac_status4DOT_284DOT_29E(Structure):
    pass
N18receive_mac_status4DOT_284DOT_29E._fields_ = [
    ('reserved', u32, 26),
    ('acpi_packet_rcvd', u32, 1),
    ('magic_packet_rcvd', u32, 1),
    ('rx_fifo_overrun', u32, 1),
    ('xon_received', u32, 1),
    ('xoff_received', u32, 1),
    ('remote_transmitter_xoffed', u32, 1),
]
N18receive_mac_status4DOT_28E._anonymous_ = ['_0']
N18receive_mac_status4DOT_28E._fields_ = [
    ('_0', N18receive_mac_status4DOT_284DOT_29E),
    ('word', u32),
]
receive_mac_status._anonymous_ = ['_0']
receive_mac_status._fields_ = [
    ('_0', N18receive_mac_status4DOT_28E),
]
class emac_mac_addr(Structure):
    pass
class N13emac_mac_addr4DOT_30E(Union):
    pass
class N13emac_mac_addr4DOT_304DOT_31E(Structure):
    pass
N13emac_mac_addr4DOT_304DOT_31E._fields_ = [
    ('byte_2', u32, 8),
    ('byte_1', u32, 8),
    ('reserved', u32, 16),
]
N13emac_mac_addr4DOT_30E._anonymous_ = ['_0']
N13emac_mac_addr4DOT_30E._fields_ = [
    ('_0', N13emac_mac_addr4DOT_304DOT_31E),
    ('word_hi', u32),
]
class N13emac_mac_addr4DOT_32E(Union):
    pass
class N13emac_mac_addr4DOT_324DOT_33E(Structure):
    pass
N13emac_mac_addr4DOT_324DOT_33E._fields_ = [
    ('byte_3', u32, 8),
    ('byte_4', u32, 8),
    ('byte_5', u32, 8),
    ('byte_6', u32, 8),
]
N13emac_mac_addr4DOT_32E._anonymous_ = ['_0']
N13emac_mac_addr4DOT_32E._fields_ = [
    ('_0', N13emac_mac_addr4DOT_324DOT_33E),
    ('word_low', u32),
]
emac_mac_addr._anonymous_ = ['_0', '_1']
emac_mac_addr._fields_ = [
    ('_0', N13emac_mac_addr4DOT_30E),
    ('_1', N13emac_mac_addr4DOT_32E),
]
class emac_rx_rule_control(Structure):
    pass
class N20emac_rx_rule_control4DOT_34E(Union):
    pass
class N20emac_rx_rule_control4DOT_344DOT_35E(Structure):
    pass
N20emac_rx_rule_control4DOT_344DOT_35E._fields_ = [
    ('enable', u32, 1),
    ('and_with_next', u32, 1),
    ('activate_rxcpu', u32, 1),
    ('reserved', u32, 1),
    ('reserved2', u32, 1),
    ('mask', u32, 1),
    ('discard', u32, 1),
    ('map', u32, 1),
    ('reserved3', u32, 6),
    ('comparison_op', u32, 2),
    ('header_type', u32, 3),
    ('pclass', u32, 5),
    ('offset', u32, 8),
]
N20emac_rx_rule_control4DOT_34E._anonymous_ = ['_0']
N20emac_rx_rule_control4DOT_34E._fields_ = [
    ('_0', N20emac_rx_rule_control4DOT_344DOT_35E),
    ('word', u32),
]
emac_rx_rule_control._anonymous_ = ['_0']
emac_rx_rule_control._fields_ = [
    ('_0', N20emac_rx_rule_control4DOT_34E),
]
class receive_mac_rules_configuration(Structure):
    pass
receive_mac_rules_configuration._fields_ = [
    ('reserved', u32, 27),
    ('no_rules_matches_default_class', u32, 3),
    ('reserved2', u32, 2),
]
class emac_low_watermark_max_receive_frame(Structure):
    pass
emac_low_watermark_max_receive_frame._fields_ = [
    ('reserved', u32, 11),
    ('txfifo_almost_empty_thresh', u32, 5),
    ('count', u32, 16),
]
class emac_mii_status(Structure):
    pass
emac_mii_status._fields_ = [
    ('communications_register_overlap_error', u32, 1),
    ('reserved2', u32, 29),
    ('mode_10mbps', u32, 1),
    ('link_status', u32, 1),
]
class emac_mii_mode(Structure):
    pass
emac_mii_mode._fields_ = [
    ('communication_delay_fix_disable', u32, 1),
    ('reserved21', u32, 10),
    ('mii_clock_count', u32, 5),
    ('enable_constant_mdc_clock_speed', u32, 1),
    ('reserved10', u32, 5),
    ('phy_address', u32, 5),
    ('port_polling', u32, 1),
    ('reserved3', u32, 1),
    ('auto_control', u32, 1),
    ('use_short_preamble', u32, 1),
    ('fast_clock', u32, 1),
]
class emac_autopolling_status(Structure):
    pass
emac_autopolling_status._fields_ = [
    ('reserved', u32, 31),
    ('error', u32, 1),
]
class emac_mii_communication(Structure):
    pass
emac_mii_communication._fields_ = [
    ('reserved30', u32, 2),
    ('start_busy', u32, 1),
    ('read_failed', u32, 1),
    ('read_command', u32, 1),
    ('write_command', u32, 1),
    ('phy_addr', u32, 5),
    ('reg_addr', u32, 5),
    ('data', u32, 16),
]
class emac_regulator_voltage_control(Structure):
    pass
emac_regulator_voltage_control._fields_ = [
    ('reserved', u32, 8),
    ('regclt_1_2v_core', u32, 4),
    ('reserved2', u32, 4),
    ('spd1000_led_pin_output_override', u32, 1),
    ('spd1000_led_pin_output_en_override', u32, 1),
    ('spd1000_led_pin_override_en', u32, 1),
    ('spd1000_led_pin_input', u32, 1),
    ('spd100_led_pin_output_override', u32, 1),
    ('spd100_led_pin_output_en_override', u32, 1),
    ('spd100_led_pin_override_en', u32, 1),
    ('spd100_led_pin_input', u32, 1),
    ('link_led_pin_output_override', u32, 1),
    ('link_led_pin_output_en_override', u32, 1),
    ('link_led_pin_override_en', u32, 1),
    ('link_led_pin_input', u32, 1),
    ('traffic_led_pin_output_override', u32, 1),
    ('traffic_led_pin_output_en_override', u32, 1),
    ('traffic_led_pin_override_en', u32, 1),
    ('traffic_led_pin_input', u32, 1),
]
class emac_regs(Structure):
    pass
class N9emac_regs4DOT_36E(Structure):
    pass
N9emac_regs4DOT_36E._fields_ = [
    ('control', emac_rx_rule_control),
    ('mask_value', u32),
]
emac_regs._fields_ = [
    ('mode', emac_mode),
    ('status', emac_status),
    ('event_enable', emac_event_enable),
    ('led_control', emac_led_control),
    ('addr', emac_mac_addr * 4),
    ('wol_pattern_pointer', u32),
    ('wol_pattern_configuration', u32),
    ('tx_random_backoff', u32),
    ('rx_mtu', u32),
    ('ofs_40', u32),
    ('ofs_44', u32),
    ('ofs_48', u32),
    ('mii_communication', emac_mii_communication),
    ('mii_status', emac_mii_status),
    ('mii_mode', emac_mii_mode),
    ('autopolling_status', emac_autopolling_status),
    ('tx_mac_mode', transmit_mac_mode),
    ('tx_mac_status', transmit_mac_status),
    ('tx_mac_lengths', transmit_mac_lengths),
    ('rx_mac_mode', receive_mac_mode),
    ('rx_mac_status', receive_mac_status),
    ('mac_hash_0', u32),
    ('mac_hash_1', u32),
    ('mac_hash_2', u32),
    ('mac_hash_3', u32),
    ('rx_rule', N9emac_regs4DOT_36E * 8),
    ('ofs_c0', u32),
    ('ofs_c4', u32),
    ('ofs_c8', u32),
    ('ofs_cc', u32),
    ('ofs_d0', u32),
    ('ofs_d4', u32),
    ('ofs_d8', u32),
    ('ofs_dc', u32),
    ('ofs_e0', u32),
    ('ofs_e4', u32),
    ('ofs_e8', u32),
    ('ofs_ec', u32),
    ('ofs_f0', u32),
    ('ofs_f4', u32),
    ('ofs_f8', u32),
    ('ofs_fc', u32),
    ('rx_rules_conf', receive_mac_rules_configuration),
    ('low_watermark_max_receive_frame', emac_low_watermark_max_receive_frame),
    ('ofs_108', u32),
    ('ofs_10c', u32),
    ('ofs_110', u32),
    ('ofs_114', u32),
    ('ofs_118', u32),
    ('ofs_11c', u32),
    ('ofs_120', u32),
    ('ofs_124', u32),
    ('ofs_128', u32),
    ('ofs_12c', u32),
    ('ofs_130', u32),
    ('ofs_134', u32),
    ('ofs_138', u32),
    ('ofs_13c', u32),
    ('ofs_140', u32),
    ('ofs_144', u32),
    ('ofs_148', u32),
    ('ofs_14c', u32),
    ('ofs_150', u32),
    ('ofs_154', u32),
    ('ofs_158', u32),
    ('ofs_15c', u32),
    ('ofs_160', u32),
    ('ofs_164', u32),
    ('ofs_168', u32),
    ('ofs_16c', u32),
    ('ofs_170', u32),
    ('ofs_174', u32),
    ('ofs_178', u32),
    ('ofs_17c', u32),
    ('ofs_180', u32),
    ('ofs_184', u32),
    ('ofs_188', u32),
    ('ofs_18c', u32),
    ('regulator_voltage_control', emac_regulator_voltage_control),
    ('ofs_194', u32),
    ('ofs_198', u32),
    ('ofs_19c', u32),
    ('ofs_1a0', u32),
    ('ofs_1a4', u32),
    ('ofs_1a8', u32),
    ('ofs_1ac', u32),
    ('ofs_1b0', u32),
    ('ofs_1b4', u32),
    ('ofs_1b8', u32),
    ('ofs_1bc', u32),
    ('eav_tx_time_stamp_lsb', u32),
    ('eav_tx_time_stamp_msb', u32),
    ('eav_av_transmit_tolerance_window', u32),
    ('eav_rt_tx_quality_1', u32),
    ('eav_rt_tx_quality_2', u32),
    ('eav_rt_tx_quality_3', u32),
    ('eav_rt_tx_quality_4', u32),
    ('ofs_1dc', u32),
]
class frame(Structure):
    pass
frame._fields_ = [
    ('dest', u8 * 6),
    ('src', u8 * 6),
    ('type', u16),
    ('data', u8 * 0),
]
class vlan_frame(Structure):
    pass
class N10vlan_frame4DOT_37E(Union):
    pass
class N10vlan_frame4DOT_374DOT_38E(Structure):
    pass
N10vlan_frame4DOT_374DOT_38E._fields_ = [
    ('priority', u16, 3),
    ('cfi', u16, 1),
    ('vlan', u16, 12),
]
N10vlan_frame4DOT_37E._anonymous_ = ['_0']
N10vlan_frame4DOT_37E._fields_ = [
    ('tci', u16),
    ('_0', N10vlan_frame4DOT_374DOT_38E),
]
vlan_frame._anonymous_ = ['_0']
vlan_frame._fields_ = [
    ('dest', u8 * 6),
    ('src', u8 * 6),
    ('tpid', u16),
    ('_0', N10vlan_frame4DOT_37E),
    ('type', u16),
    ('data', u8 * 0),
]
class ftq_reset(Structure):
    pass
class N9ftq_reset4DOT_39E(Union):
    pass
class N9ftq_reset4DOT_394DOT_40E(Structure):
    pass
N9ftq_reset4DOT_394DOT_40E._fields_ = [
    ('reserved', u32, 15),
    ('receive_data_completion', u32, 1),
    ('reserved2', u32, 1),
    ('receive_list_placement', u32, 1),
    ('receive_bd_complete', u32, 1),
    ('reserved3', u32, 1),
    ('mac_tx', u32, 1),
    ('host_coalescing', u32, 1),
    ('send_data_completion', u32, 1),
    ('reserved4', u32, 1),
    ('dma_high_prio_write', u32, 1),
    ('dma_write', u32, 1),
    ('reserved5', u32, 1),
    ('send_bd_completion', u32, 1),
    ('reserved6', u32, 1),
    ('dma_high_prio_read', u32, 1),
    ('dma_read', u32, 1),
    ('reserved7', u32, 1),
]
N9ftq_reset4DOT_39E._anonymous_ = ['_0']
N9ftq_reset4DOT_39E._fields_ = [
    ('word', u32),
    ('_0', N9ftq_reset4DOT_394DOT_40E),
]
ftq_reset._anonymous_ = ['_0']
ftq_reset._fields_ = [
    ('_0', N9ftq_reset4DOT_39E),
]
class ftq_enqueue_dequeue(Structure):
    pass
class N19ftq_enqueue_dequeue4DOT_41E(Union):
    pass
class N19ftq_enqueue_dequeue4DOT_414DOT_42E(Structure):
    pass
N19ftq_enqueue_dequeue4DOT_414DOT_42E._fields_ = [
    ('ignored1', u32, 10),
    ('head_txmbuf_ptr', u32, 6),
    ('ignored2', u32, 10),
    ('tail_txmbuf_ptr', u32, 6),
]
N19ftq_enqueue_dequeue4DOT_41E._anonymous_ = ['_0']
N19ftq_enqueue_dequeue4DOT_41E._fields_ = [
    ('_0', N19ftq_enqueue_dequeue4DOT_414DOT_42E),
    ('word', u32),
]
ftq_enqueue_dequeue._anonymous_ = ['_0']
ftq_enqueue_dequeue._fields_ = [
    ('_0', N19ftq_enqueue_dequeue4DOT_41E),
]
class ftq_write_peek(Structure):
    pass
class N14ftq_write_peek4DOT_43E(Union):
    pass
class N14ftq_write_peek4DOT_434DOT_44E(Structure):
    pass
N14ftq_write_peek4DOT_434DOT_44E._fields_ = [
    ('reserved', u32, 11),
    ('valid', u32, 1),
    ('skip', u32, 1),
    ('pass', u32, 1),
    ('head_rxmbuf_ptr', u32, 9),
    ('tail_rxmbuf_ptr', u32, 9),
]
N14ftq_write_peek4DOT_43E._anonymous_ = ['_0']
N14ftq_write_peek4DOT_43E._fields_ = [
    ('_0', N14ftq_write_peek4DOT_434DOT_44E),
    ('word', u32),
]
ftq_write_peek._anonymous_ = ['_0']
ftq_write_peek._fields_ = [
    ('_0', N14ftq_write_peek4DOT_43E),
]
class ftq_queue_regs(Structure):
    pass
ftq_queue_regs._fields_ = [
    ('control', u32),
    ('count', u32),
    ('q', ftq_enqueue_dequeue),
    ('peek', ftq_write_peek),
]
class ftq_regs(Structure):
    pass
ftq_regs._fields_ = [
    ('reset', ftq_reset),
    ('ofs_04', u32),
    ('ofs_08', u32),
    ('ofs_0c', u32),
    ('dma_read', ftq_queue_regs),
    ('dma_high_read', ftq_queue_regs),
    ('dma_comp_discard', ftq_queue_regs),
    ('send_bd_comp', ftq_queue_regs),
    ('send_data_init', ftq_queue_regs),
    ('dma_write', ftq_queue_regs),
    ('dma_high_write', ftq_queue_regs),
    ('sw_type1', ftq_queue_regs),
    ('send_data_comp', ftq_queue_regs),
    ('host_coalesce', ftq_queue_regs),
    ('mac_tx', ftq_queue_regs),
    ('mbuf_clust_free', ftq_queue_regs),
    ('rcv_bd_comp', ftq_queue_regs),
    ('rcv_list_plmt', ftq_queue_regs),
    ('rdiq', ftq_queue_regs),
    ('rcv_data_comp', ftq_queue_regs),
    ('sw_type2', ftq_queue_regs),
]
class gencomm(Structure):
    pass
gencomm._fields_ = [
    ('dword', u32 * 256),
]
class grc_mode(Structure):
    pass
grc_mode._fields_ = [
    ('pcie_hi1k_en', u32, 1),
    ('multi_cast_enable', u32, 1),
    ('pcie_dl_sel', u32, 1),
    ('int_on_flow_attn', u32, 1),
    ('int_on_dma_attn', u32, 1),
    ('int_on_mac_attn', u32, 1),
    ('int_on_rxcpu_attn', u32, 1),
    ('int_on_txcpu_attn', u32, 1),
    ('receive_no_pseudo_header_cksum', u32, 1),
    ('pcie_pl_sel', u32, 1),
    ('nvram_write_enable', u32, 1),
    ('send_no_pseudo_header_cksum', u32, 1),
    ('time_sync_enable', u32, 1),
    ('eav_mode_enable', u32, 1),
    ('host_send_bds', u32, 1),
    ('host_stack_up', u32, 1),
    ('force_32bit_pci_bus_mode', u32, 1),
    ('no_int_on_recv', u32, 1),
    ('no_int_on_send', u32, 1),
    ('dma_write_sys_attn', u32, 1),
    ('allow_bad_frames', u32, 1),
    ('no_crc', u32, 1),
    ('no_frame_cracking', u32, 1),
    ('split_hdr_mode', u32, 1),
    ('cr_func_sel', u32, 2),
    ('word_swap_data', u32, 1),
    ('byte_swap_data', u32, 1),
    ('reserved5', u32, 1),
    ('word_swap_bd', u32, 1),
    ('byte_swap_bd', u32, 1),
    ('int_send_tick', u32, 1),
]
class grc_misc_config(Structure):
    pass
grc_misc_config._fields_ = [
    ('bond_id_7', u32, 1),
    ('bond_id_6', u32, 1),
    ('disable_grc_reset_on_pcie_block', u32, 1),
    ('bond_id_5', u32, 1),
    ('bond_id_4', u32, 1),
    ('gphy_keep_power_during_reset', u32, 1),
    ('reserved1', u32, 1),
    ('ram_powerdown', u32, 1),
    ('reserved2', u32, 1),
    ('bias_iddq', u32, 1),
    ('gphy_iddq', u32, 1),
    ('powerdown', u32, 1),
    ('vmain_prsnt_state', u32, 1),
    ('power_state', u32, 2),
    ('bond_id_3', u32, 1),
    ('bond_id_2', u32, 1),
    ('bond_id_1', u32, 1),
    ('bond_id_0', u32, 1),
    ('reserved3', u32, 5),
    ('timer_prescaler', u32, 7),
    ('grc_reset', u32, 1),
]
class grc_misc_local_control(Structure):
    pass
grc_misc_local_control._fields_ = [
    ('wake_on_link_up', u32, 1),
    ('wake_on_link_down', u32, 1),
    ('disable_traffic_led_fix', u32, 1),
    ('reserved', u32, 2),
    ('pme_assert', u32, 1),
    ('reserved1', u32, 1),
    ('auto_seeprom', u32, 1),
    ('reserved2', u32, 1),
    ('ctrl_ssram_type', u32, 1),
    ('bank_select', u32, 1),
    ('reserved3', u32, 3),
    ('enable_ext_memory', u32, 1),
    ('gpio2_output', u32, 1),
    ('gpio1_output', u32, 1),
    ('gpio0_output', u32, 1),
    ('gpio2_output_enable', u32, 1),
    ('gpio1_output_enable', u32, 1),
    ('gpio0_output_enable', u32, 1),
    ('gpio2_input', u32, 1),
    ('gpio1_input', u32, 1),
    ('gpio0_input', u32, 1),
    ('reserved4', u32, 2),
    ('energy_detection_pin', u32, 1),
    ('uart_disable', u32, 1),
    ('interrupt_on_attention', u32, 1),
    ('set_interrupt', u32, 1),
    ('clear_interrupt', u32, 1),
    ('interrupt_state', u32, 1),
]
class grc_cpu_event(Structure):
    pass
class N13grc_cpu_event4DOT_45E(Union):
    pass
class N13grc_cpu_event4DOT_454DOT_46E(Structure):
    pass
N13grc_cpu_event4DOT_454DOT_46E._fields_ = [
    ('sw_event_13', u32, 1),
    ('sw_event_12', u32, 1),
    ('timer', u32, 1),
    ('sw_event_11', u32, 1),
    ('flow', u32, 1),
    ('rx_cpu', u32, 1),
    ('emac', u32, 1),
    ('tx_cpu', u32, 1),
    ('sw_event_10', u32, 1),
    ('hi_prio_mbox', u32, 1),
    ('low_prio_mbox', u32, 1),
    ('dma', u32, 1),
    ('sw_event_9', u32, 1),
    ('hi_dma_rd', u32, 1),
    ('hi_dma_wr', u32, 1),
    ('sw_event_8', u32, 1),
    ('host_coalescing', u32, 1),
    ('sw_event_7', u32, 1),
    ('receive_data_comp', u32, 1),
    ('sw_event_6', u32, 1),
    ('rx_sw_queue', u32, 1),
    ('dma_rd', u32, 1),
    ('dma_wr', u32, 1),
    ('rdiq', u32, 1),
    ('sw_event_5', u32, 1),
    ('recv_bd_comp', u32, 1),
    ('sw_event_4', u32, 1),
    ('recv_list_selector', u32, 1),
    ('sw_event_3', u32, 1),
    ('recv_list_placement', u32, 1),
    ('sw_event_1', u32, 1),
    ('sw_event_0', u32, 1),
]
N13grc_cpu_event4DOT_45E._anonymous_ = ['_0']
N13grc_cpu_event4DOT_45E._fields_ = [
    ('_0', N13grc_cpu_event4DOT_454DOT_46E),
    ('word', u32),
]
grc_cpu_event._anonymous_ = ['_0']
grc_cpu_event._fields_ = [
    ('_0', N13grc_cpu_event4DOT_45E),
]
class grc_cpu_semaphore(Structure):
    pass
grc_cpu_semaphore._fields_ = [
    ('reserved', u32, 31),
    ('semaphore', u32, 1),
]
class grc_pcie_misc_status(Structure):
    pass
grc_pcie_misc_status._fields_ = [
    ('reserved', u32, 8),
    ('p1_pcie_ack_fifo_underrun', u32, 1),
    ('p0_pcie_ack_fifo_underrun', u32, 1),
    ('p1_pcie_ack_fifo_overrun', u32, 1),
    ('p0_pcie_ack_fifo_overrun', u32, 1),
    ('reserved2', u32, 3),
    ('pcie_link_in_l23', u32, 1),
    ('f0_pcie_powerstate', u32, 2),
    ('f1_pcie_powerstate', u32, 2),
    ('f2_pcie_powerstate', u32, 2),
    ('f3_pcie_powerstate', u32, 2),
    ('pcie_phy_attn', u32, 4),
    ('pci_grc_intb_f3', u32, 1),
    ('pci_grc_intb_f2', u32, 1),
    ('pci_grc_intb_f1', u32, 1),
    ('pci_grc_inta', u32, 1),
]
class grc_cpu_event_enable(Structure):
    pass
class N20grc_cpu_event_enable4DOT_47E(Union):
    pass
class N20grc_cpu_event_enable4DOT_474DOT_48E(Structure):
    pass
N20grc_cpu_event_enable4DOT_474DOT_48E._fields_ = [
    ('flash', u32, 1),
    ('vpd', u32, 1),
    ('timer', u32, 1),
    ('rom', u32, 1),
    ('hc_module', u32, 1),
    ('rx_cpu_module', u32, 1),
    ('emac', u32, 1),
    ('memory_map_enable', u32, 1),
    ('reserved23', u32, 1),
    ('high_prio_mbox', u32, 1),
    ('low_prio_mbox', u32, 1),
    ('dma', u32, 1),
    ('reserved19', u32, 1),
    ('reserved18', u32, 1),
    ('reserved17', u32, 1),
    ('asf_location_15', u32, 1),
    ('tpm_interrupt_enable', u32, 1),
    ('asf_location_14', u32, 1),
    ('reserved13', u32, 1),
    ('asf_location_13', u32, 1),
    ('unused_sdi', u32, 1),
    ('sdc', u32, 1),
    ('sdi', u32, 1),
    ('rdiq', u32, 1),
    ('asf_location_12', u32, 1),
    ('reserved6', u32, 1),
    ('asf_location_11', u32, 1),
    ('reserved4', u32, 1),
    ('asf_location_10', u32, 1),
    ('reserved2', u32, 1),
    ('asf_location_9', u32, 1),
    ('asf_location_8', u32, 1),
]
N20grc_cpu_event_enable4DOT_47E._anonymous_ = ['_0']
N20grc_cpu_event_enable4DOT_47E._fields_ = [
    ('_0', N20grc_cpu_event_enable4DOT_474DOT_48E),
    ('word', u32),
]
grc_cpu_event_enable._anonymous_ = ['_0']
grc_cpu_event_enable._fields_ = [
    ('_0', N20grc_cpu_event_enable4DOT_47E),
]
class grc_secfg_1(Structure):
    pass
grc_secfg_1._fields_ = [
    ('cr_vddio_30v_reg_out_adj', u32, 4),
    ('cr_vddio_18v_reg_out_adj', u32, 4),
    ('si_eedata_pin_str_ctrl', u32, 3),
    ('so_pin_str_ctrl', u32, 3),
    ('sclk_pin_str_ctrl', u32, 3),
    ('so_pin_str_ctrl2', u32, 3),
    ('flash_led_pin_sharing_ctrl', u32, 1),
    ('sd_clk_pull_up_ctrl', u32, 1),
    ('xd_r_b_n_pull_up_ctrl', u32, 1),
    ('gpio0_sd_bus_pow_ctrl', u32, 1),
    ('sd_bus_pow_led_ctrl', u32, 1),
    ('sd_led_output_mode_ctrl', u32, 2),
    ('sd_bus_pow_output_pol_ctrl', u32, 1),
    ('sd_write_protect_pol_ctrl', u32, 1),
    ('sd_mmc_card_detect_pol_ctrl', u32, 1),
    ('mem_stk_ins_pol_ctrl', u32, 1),
    ('xd_picture_card_det_pol_ctrl', u32, 1),
]
class grc_secfg_2(Structure):
    pass
grc_secfg_2._fields_ = [
    ('reserved', u32, 24),
    ('sd_write_prot_int_pu_pd_ovrd_ctrl', u32, 2),
    ('reserved2', u32, 2),
    ('mem_stk_ins_int_pu_pd_ovrd_ctrl', u32, 2),
    ('xd_picture_card_det_pu_pd_ovrd_ctrl', u32, 2),
]
class grc_bond_id(Structure):
    pass
grc_bond_id._fields_ = [
    ('serdes_l0_exit_lat_sel', u32, 2),
    ('umc_bg_wa', u32, 1),
    ('uart_enable', u32, 1),
    ('eav_disable', u32, 1),
    ('sedata_oe_ctrl', u32, 1),
    ('disable_auto_eeprom_reset', u32, 1),
    ('eee_lpi_enable_hw_default', u32, 1),
    ('pcie_gen2_mode', u32, 1),
    ('vaux_prsnt', u32, 2),
    ('non_cr_sku', u32, 1),
    ('disable_gigabit', u32, 1),
    ('disable_led_pin_sharing', u32, 1),
    ('cr_regulator_power_down', u32, 1),
    ('bond_id', u32, 17),
]
class grc_clock_ctrl(Structure):
    pass
grc_clock_ctrl._fields_ = [
    ('pl_clock_disable', u32, 1),
    ('dll_clock_disable', u32, 1),
    ('tl_clock_disable', u32, 1),
    ('pci_express_clock_to_core_clock', u32, 1),
    ('reserved1', u32, 1),
    ('reserved2', u32, 1),
    ('reserved3', u32, 1),
    ('reserved4', u32, 1),
    ('reserved5', u32, 1),
    ('reserved6', u32, 1),
    ('reserved7', u32, 1),
    ('select_final_alt_clock_src', u32, 1),
    ('slow_core_clock_mode', u32, 1),
    ('led_polarity', u32, 1),
    ('bist_function_ctrl', u32, 1),
    ('asynchronous_bist_reset', u32, 1),
    ('reserved8', u32, 2),
    ('select_alt_clock_src', u32, 1),
    ('select_alt_clock', u32, 1),
    ('reserved9', u32, 2),
    ('core_clock_disable', u32, 1),
    ('reserved10', u32, 1),
    ('reserved11', u32, 1),
    ('reserved12', u32, 2),
    ('reserved13', u32, 5),
]
class grc_misc_control(Structure):
    pass
grc_misc_control._fields_ = [
    ('done_dr_fix4_en', u32, 1),
    ('done_dr_fix3_en', u32, 1),
    ('done_dr_fix2_en', u32, 1),
    ('done_dr_fix_en', u32, 1),
    ('clkreq_delay_dis', u32, 1),
    ('lcrc_dr_fix2_en', u32, 1),
    ('lcrc_dr_fix_en', u32, 1),
    ('chksum_fix_en', u32, 1),
    ('ma_addr_fix_en', u32, 1),
    ('ma_prior_en', u32, 1),
    ('underrun_fix_en', u32, 1),
    ('underrun_clear', u32, 1),
    ('overrun_clear', u32, 1),
    ('reserved0', u32, 19),
]
class grc_fastboot_program_counter(Structure):
    pass
class N28grc_fastboot_program_counter4DOT_49E(Union):
    pass
class N28grc_fastboot_program_counter4DOT_494DOT_50E(Structure):
    pass
N28grc_fastboot_program_counter4DOT_494DOT_50E._fields_ = [
    ('enable', u32, 1),
    ('addr', u32, 31),
]
N28grc_fastboot_program_counter4DOT_49E._anonymous_ = ['_0']
N28grc_fastboot_program_counter4DOT_49E._fields_ = [
    ('_0', N28grc_fastboot_program_counter4DOT_494DOT_50E),
    ('word', u32),
]
grc_fastboot_program_counter._anonymous_ = ['_0']
grc_fastboot_program_counter._fields_ = [
    ('_0', N28grc_fastboot_program_counter4DOT_49E),
]
class grc_power_management_debug(Structure):
    pass
grc_power_management_debug._fields_ = [
    ('pclk_sw_force_override_en', u32, 1),
    ('pclk_sw_force_override_val', u32, 1),
    ('pclk_sw_sel_override_en', u32, 1),
    ('pclk_sw_sel_override_val', u32, 1),
    ('pclk_sw_force_cond_a_dis', u32, 1),
    ('pclk_sw_force_cond_b_dis', u32, 1),
    ('pclk_sw_force_cond_c_en', u32, 1),
    ('pclk_sw_sel_cond_a_dis', u32, 1),
    ('pclk_sw_sel_cond_b_dis', u32, 1),
    ('pclk_sw_sel_cond_c_dis', u32, 1),
    ('reserved17', u32, 5),
    ('perst_override', u32, 1),
    ('reserved6', u32, 10),
    ('pipe_clkreq_serdes', u32, 1),
    ('pipe_aux_power_down', u32, 1),
    ('pll_power_down', u32, 1),
    ('clock_req_output_stat', u32, 1),
    ('reserved1', u32, 1),
    ('pll_is_up', u32, 1),
]
class grc_seeprom_addr(Structure):
    pass
grc_seeprom_addr._fields_ = [
    ('not_write', u32, 1),
    ('complete', u32, 1),
    ('reset', u32, 1),
    ('device_id', u32, 3),
    ('start_access', u32, 1),
    ('half_clock_period', u32, 9),
    ('addr', u32, 14),
    ('reserved0', u32, 2),
]
class grc_seeprom_ctrl(Structure):
    pass
grc_seeprom_ctrl._fields_ = [
    ('reserved6', u32, 26),
    ('data_input', u32, 1),
    ('data_output', u32, 1),
    ('data_output_tristate', u32, 1),
    ('clock_input', u32, 1),
    ('clock_output', u32, 1),
    ('clock_output_tristate', u32, 1),
]
class grc_mdi_ctrl(Structure):
    pass
grc_mdi_ctrl._fields_ = [
    ('reserved4', u32, 28),
    ('mdi_clk', u32, 1),
    ('mdi_sel', u32, 1),
    ('mdi_en', u32, 1),
    ('mdi_data', u32, 1),
]
class grc_exp_rom_addr(Structure):
    pass
grc_exp_rom_addr._fields_ = [
    ('test_bits', u32, 8),
    ('base', u32, 24),
]
class grc_regs(Structure):
    pass
grc_regs._fields_ = [
    ('mode', grc_mode),
    ('misc_config', grc_misc_config),
    ('misc_local_control', grc_misc_local_control),
    ('timer', u32),
    ('rxcpu_event', grc_cpu_event),
    ('rxcpu_timer_reference', u32),
    ('rxcpu_semaphore', grc_cpu_semaphore),
    ('pcie_misc_status', grc_pcie_misc_status),
    ('card_reader_dma_read_policy', u32),
    ('card_reader_dma_write_policy', u32),
    ('ofs_28', u32),
    ('ofs_2c', u32),
    ('ofs_30', u32),
    ('ofs_34', u32),
    ('seeprom_addr', grc_seeprom_addr),
    ('seeprom_data', u32),
    ('seeprom_ctrl', grc_seeprom_ctrl),
    ('mdi_ctrl', grc_mdi_ctrl),
    ('seeprom_delay', u32),
    ('rxcpu_event_enable', grc_cpu_event_enable),
    ('ofs_50', u32),
    ('ofs_54', u32),
    ('ofs_58', u32),
    ('ofs_5c', u32),
    ('ofs_60', u32),
    ('ofs_64', u32),
    ('ofs_68', u32),
    ('ofs_6c', u32),
    ('msg_xchng_out', u32),
    ('msg_xchng_in', u32),
    ('ofs_78', u32),
    ('ofs_7c', u32),
    ('secfg1', grc_secfg_1),
    ('secfg2', grc_secfg_2),
    ('bond_id', grc_bond_id),
    ('clock_ctrl', grc_clock_ctrl),
    ('misc_control', grc_misc_control),
    ('fastboot_pc', grc_fastboot_program_counter),
    ('ofs_98', u32),
    ('ofs_9c', u32),
    ('ofs_a0', u32),
    ('power_management_debug', grc_power_management_debug),
    ('ofs_a8', u32),
    ('ofs_ac', u32),
    ('ofs_b0', u32),
    ('ofs_b4', u32),
    ('ofs_b8', u32),
    ('ofs_bc', u32),
    ('ofs_c0', u32),
    ('ofs_c4', u32),
    ('ofs_c8', u32),
    ('ofs_cc', u32),
    ('ofs_d0', u32),
    ('ofs_d4', u32),
    ('ofs_d8', u32),
    ('ofs_dc', u32),
    ('ofs_e0', u32),
    ('ofs_e4', u32),
    ('ofs_e8', u32),
    ('exp_rom_addr', grc_exp_rom_addr),
    ('ofs_ec', u32),
    ('ofs_f0', u32),
    ('ofs_f4', u32),
    ('ofs_f8', u32),
    ('ofs_fc', u32),
]
class hc_mode(Structure):
    pass
hc_mode._fields_ = [
    ('during_int_frame_cntr_fix_disable', u32, 1),
    ('end_of_rx_stream_detector_fires_all_msix', u32, 1),
    ('end_of_rx_stream_int', u32, 1),
    ('enable_attn_int_fix', u32, 1),
    ('reserved', u32, 10),
    ('coalesce_now_1_5', u32, 5),
    ('no_int_on_force_update', u32, 1),
    ('no_int_on_dmad_force', u32, 1),
    ('reserved2', u32, 1),
    ('clear_ticks_mode_on_rx', u32, 1),
    ('status_block_size', u32, 2),
    ('msi_bits', u32, 3),
    ('coalesce_now', u32, 1),
    ('attn_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
class hc_status(Structure):
    pass
hc_status._fields_ = [
    ('reserved', u32, 29),
    ('error', u32, 1),
    ('reserved2', u32, 2),
]
class hc_flow_attention(Structure):
    pass
hc_flow_attention._fields_ = [
    ('sbdi', u32, 1),
    ('sbdc', u32, 1),
    ('sbdrs', u32, 1),
    ('sdi', u32, 1),
    ('sdc', u32, 1),
    ('reserved', u32, 3),
    ('rbdi', u32, 1),
    ('rbdc', u32, 1),
    ('rlp', u32, 1),
    ('rls', u32, 1),
    ('rdi', u32, 1),
    ('rdc', u32, 1),
    ('rcb_incorrect', u32, 1),
    ('dmac_discard', u32, 1),
    ('hc', u32, 1),
    ('reserved2', u32, 7),
    ('ma', u32, 1),
    ('mbuf_low_water', u32, 1),
    ('reserved3', u32, 6),
]
class hc_regs(Structure):
    pass
hc_regs._fields_ = [
    ('mode', hc_mode),
    ('status', hc_status),
    ('rx_coal_ticks', u32),
    ('tx_coal_ticks', u32),
    ('rx_max_coal_bds', u32),
    ('tx_max_coal_bds', u32),
    ('ofs_18', u32),
    ('ofs_1c', u32),
    ('rx_max_coal_bds_in_int', u32),
    ('tx_max_coal_bds_in_int', u32),
    ('ofs_28', u32),
    ('ofs_2c', u32),
    ('ofs_30', u32),
    ('ofs_34', u32),
    ('status_block_host_addr_hi', u32),
    ('status_block_host_addr_low', u32),
    ('ofs_40', u32),
    ('status_block_nic_addr', u32),
    ('flow_attention', hc_flow_attention),
    ('ofs_4c', u32),
    ('nic_jumbo_rbd_ci', u32),
    ('nic_std_rbd_ci', u32),
    ('nic_mini_rbd_ci', u32),
    ('ofs_5c', u32),
    ('ofs_60', u32),
    ('ofs_64', u32),
    ('ofs_68', u32),
    ('ofs_6c', u32),
    ('ofs_70', u32),
    ('ofs_74', u32),
    ('ofs_78', u32),
    ('ofs_7c', u32),
    ('nic_diag_rr_pi', u32 * 16),
    ('nic_diag_sbd_ci', u32 * 16),
]
class ma_mode(Structure):
    pass
class N7ma_mode4DOT_51E(Union):
    pass
class N7ma_mode4DOT_514DOT_52E(Structure):
    pass
N7ma_mode4DOT_514DOT_52E._fields_ = [
    ('tx_mbuf_cfg', u32, 2),
    ('cpu_pipeline_request_disable', u32, 1),
    ('low_latency_enable', u32, 1),
    ('fast_path_read_disable', u32, 1),
    ('reserved21', u32, 6),
    ('dmaw2_addr_trap', u32, 1),
    ('bufman_addr_trap', u32, 1),
    ('txbd_addr_trap', u32, 1),
    ('sdc_dmac_trap', u32, 1),
    ('sdi_addr_trap', u32, 1),
    ('mcf_addr_trap', u32, 1),
    ('hc_addr_trap', u32, 1),
    ('dc_addr_trap', u32, 1),
    ('rdi2_addr_trap', u32, 1),
    ('rdi1_addr_trap', u32, 1),
    ('rq_addr_trap', u32, 1),
    ('dmar2_addr_trap', u32, 1),
    ('pci_addr_trap', u32, 1),
    ('tx_risc_addr_trap', u32, 1),
    ('rx_risc_addr_trap', u32, 1),
    ('dmar1_addr_trap', u32, 1),
    ('dmaw1_addr_trap', u32, 1),
    ('rx_mac_addr_trap', u32, 1),
    ('tx_mac_addr_trap', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
N7ma_mode4DOT_51E._anonymous_ = ['_0']
N7ma_mode4DOT_51E._fields_ = [
    ('_0', N7ma_mode4DOT_514DOT_52E),
    ('word', u32),
]
ma_mode._anonymous_ = ['_0']
ma_mode._fields_ = [
    ('_0', N7ma_mode4DOT_51E),
]
class ma_status(Structure):
    pass
ma_status._fields_ = [
    ('reserved', u32, 11),
    ('dmaw2_addr_trap', u32, 1),
    ('reserved2', u32, 3),
    ('sdi_addr_trap', u32, 1),
    ('reserved3', u32, 3),
    ('rdi2_addr_trap', u32, 1),
    ('rdi1_addr_trap', u32, 1),
    ('rq_addr_trap', u32, 1),
    ('reserved4', u32, 1),
    ('pci_addr_trap', u32, 1),
    ('reserved5', u32, 1),
    ('rx_risc_addr_trap', u32, 1),
    ('dmar1_addr_trap', u32, 1),
    ('dmaw1_addr_trap', u32, 1),
    ('rx_mac_addr_trap', u32, 1),
    ('tx_mac_addr_trap', u32, 1),
    ('reserved6', u32, 2),
]
class ma_regs(Structure):
    pass
ma_regs._fields_ = [
    ('mode', ma_mode),
    ('status', ma_status),
    ('trap_addr_low', u32),
    ('trap_addr_hi', u32),
]

# values for enumeration 'known_mailboxes'
known_mailboxes = c_int # enum
class mailbox(Structure):
    pass
mailbox._fields_ = [
    ('hi', u32),
    ('low', u32),
]
class hpmb_regs(Structure):
    pass
hpmb_regs._fields_ = [
    ('box', mailbox * 64),
]
class lpmb_regs(Structure):
    pass
lpmb_regs._fields_ = [
    ('box', mailbox * 64),
]
class mbuf_hdr(Structure):
    pass
mbuf_hdr._fields_ = [
    ('length', u32, 7),
    ('next_mbuf', u32, 16),
    ('reserved', u32, 7),
    ('f', u32, 1),
    ('c', u32, 1),
]
class mbuf_frame_desc(Structure):
    pass
mbuf_frame_desc._fields_ = [
    ('status_ctrl', u32),
    ('len', u16),
    ('reserved', u8),
    ('qids', u8),
    ('tcp_udp_hdr_start', u16),
    ('ip_hdr_start', u16),
    ('vlan_id', u16),
    ('data_start', u16),
    ('tcp_udp_checksum', u16),
    ('ip_checksum', u16),
    ('checksum_status', u16),
    ('pseudo_checksum', u16),
    ('rupt', u8),
    ('rule_class', u8),
    ('rule_match', u16),
    ('mbuf', u16),
    ('reserved2', u16),
    ('reserved3', u32),
    ('reserved4', u32),
]
class mbuf(Structure):
    pass
class N4mbuf4DOT_53E(Union):
    pass
N4mbuf4DOT_53E._fields_ = [
    ('frame', mbuf_frame_desc),
    ('word', u32 * 30),
    ('byte', u8 * 120),
]
mbuf._fields_ = [
    ('hdr', mbuf_hdr),
    ('next_frame_ptr', u32),
    ('data', N4mbuf4DOT_53E),
]
class msi_mode(Structure):
    pass
msi_mode._fields_ = [
    ('priority', u32, 2),
    ('msix_fix_pcie_client', u32, 1),
    ('reserved', u32, 18),
    ('msi_message', u32, 3),
    ('msix_multi_vector_mode', u32, 1),
    ('msi_byte_swap_enable', u32, 1),
    ('msi_single_shot_disable', u32, 1),
    ('pci_parity_error_attn', u32, 1),
    ('pci_master_abort_attn', u32, 1),
    ('pci_target_abort_attn', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
class msi_status(Structure):
    pass
msi_status._fields_ = [
    ('reserved', u32, 27),
    ('pci_parity_error', u32, 1),
    ('pci_master_abort', u32, 1),
    ('pci_target_abort', u32, 1),
    ('reserved2', u32, 1),
    ('msi_pci_request', u32, 1),
]
class msi_regs(Structure):
    pass
msi_regs._fields_ = [
    ('mode', msi_mode),
    ('status', msi_status),
]
class nrdma_mode(Structure):
    pass
nrdma_mode._fields_ = [
    ('reserved26', u32, 6),
    ('addr_oflow_err_log_en', u32, 1),
    ('reserved18', u32, 7),
    ('pci_req_burst_len', u32, 2),
    ('reserved14', u32, 2),
    ('attn_ens', u32, 12),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
class nrdma_status(Structure):
    pass
nrdma_status._fields_ = [
    ('reserved11', u32, 21),
    ('malformed_or_poison_tlp_err_det', u32, 1),
    ('rdma_local_mem_wr_longer_than_dma_len_err', u32, 1),
    ('rdma_pci_fifo_oflow_err', u32, 1),
    ('rdma_pci_fifo_urun_err', u32, 1),
    ('rdma_pci_fifo_orun_err', u32, 1),
    ('rdma_pci_host_addr_oflow_err', u32, 1),
    ('dma_rd_comp_to', u32, 1),
    ('comp_abort_err', u32, 1),
    ('unsupp_req_err_det', u32, 1),
    ('reserved0', u32, 2),
]
class nrdma_programmable_ipv6_extension_header(Structure):
    pass
nrdma_programmable_ipv6_extension_header._fields_ = [
    ('hdr_type2_en', u32, 1),
    ('hdr_type1_en', u32, 1),
    ('reserved16', u32, 14),
    ('hdr_type2', u32, 8),
    ('hdr_type1', u32, 8),
]
class nrdma_rstates_debug(Structure):
    pass
nrdma_rstates_debug._fields_ = [
    ('reserved11', u32, 21),
    ('sdi_dr_wr', u32, 1),
    ('dr_sdi_wr_ack', u32, 1),
    ('non_lso_sel', u32, 1),
    ('non_lso_q_full', u32, 1),
    ('non_lso_busy', u32, 1),
    ('rstate3', u32, 2),
    ('reserved3', u32, 1),
    ('rstate1', u32, 3),
]
class nrdma_rstate2_debug(Structure):
    pass
nrdma_rstate2_debug._fields_ = [
    ('reserved5', u32, 27),
    ('rstate2', u32, 5),
]
class nrdma_bd_status_debug(Structure):
    pass
nrdma_bd_status_debug._fields_ = [
    ('reserved3', u32, 29),
    ('bd_non_mbuf', u32, 1),
    ('fst_bd_mbuf', u32, 1),
    ('lst_bd_mbuf', u32, 1),
]
class nrdma_req_ptr_debug(Structure):
    pass
nrdma_req_ptr_debug._fields_ = [
    ('ih_dmad_length', u32, 16),
    ('reserved13', u32, 3),
    ('txmbuf_left', u32, 8),
    ('rh_dmad_load_en', u32, 1),
    ('rftq_d_dmad_pnt', u32, 2),
    ('reserved0', u32, 2),
]
class nrdma_hold_d_dmad_debug(Structure):
    pass
nrdma_hold_d_dmad_debug._fields_ = [
    ('reserved2', u32, 30),
    ('rhold_d_dmad', u32, 2),
]
class nrdma_length_and_address_debug(Structure):
    pass
nrdma_length_and_address_debug._fields_ = [
    ('rdma_rd_length', u32, 16),
    ('reserved6', u32, 10),
    ('mbuf_addr_idx', u32, 6),
]
class nrdma_mbuf_byte_count_debug(Structure):
    pass
nrdma_mbuf_byte_count_debug._fields_ = [
    ('reserved4', u32, 28),
    ('rmbuf_byte_cnt', u32, 4),
]
class nrdma_pcie_debug_status(Structure):
    pass
nrdma_pcie_debug_status._fields_ = [
    ('lt_term', u32, 4),
    ('reserved27', u32, 1),
    ('lt_too_lg', u32, 1),
    ('lt_dma_reload', u32, 1),
    ('lt_dma_good', u32, 1),
    ('cur_trans_active', u32, 1),
    ('drpcireq', u32, 1),
    ('dr_pci_word_swap', u32, 1),
    ('dr_pci_byte_swap', u32, 1),
    ('new_slow_core_clk_mode', u32, 1),
    ('rbd_non_mbuf', u32, 1),
    ('rfst_bd_mbuf', u32, 1),
    ('rlst_bd_mbuf', u32, 1),
    ('dr_pci_len', u32, 16),
]
class nrdma_pcie_dma_read_req_debug(Structure):
    pass
nrdma_pcie_dma_read_req_debug._fields_ = [
    ('dr_pci_ad_hi', u32, 16),
    ('dr_pci_ad_lo', u32, 16),
]
class nrdma_pcie_dma_req_length_debug(Structure):
    pass
nrdma_pcie_dma_req_length_debug._fields_ = [
    ('reserved16', u32, 16),
    ('rdma_len', u32, 16),
]
class nrdma_fifo1_debug(Structure):
    pass
nrdma_fifo1_debug._fields_ = [
    ('reserved9', u32, 23),
    ('c_write_addr', u32, 9),
]
class nrdma_fifo2_debug(Structure):
    pass
nrdma_fifo2_debug._fields_ = [
    ('reserved18', u32, 14),
    ('rlctrl_in', u32, 9),
    ('c_read_addr', u32, 9),
]
class nrdma_post_proc_pkt_req_cnt(Structure):
    pass
nrdma_post_proc_pkt_req_cnt._fields_ = [
    ('reserved8', u32, 24),
    ('pkt_req_cnt', u32, 8),
]
class nrdma_mbuf_addr_debug(Structure):
    pass
nrdma_mbuf_addr_debug._fields_ = [
    ('reserved26', u32, 6),
    ('mactq_full', u32, 1),
    ('txfifo_almost_urun', u32, 1),
    ('tde_fifo_entry', u32, 8),
    ('rcmp_head', u32, 16),
]
class nrdma_tce_debug1(Structure):
    pass
nrdma_tce_debug1._fields_ = [
    ('odi_state_out', u32, 4),
    ('odi_state_in', u32, 4),
    ('fifo_odi_data_code', u32, 2),
    ('fifo_odi_data', u32, 22),
]
class nrdma_tce_debug2(Structure):
    pass
nrdma_tce_debug2._fields_ = [
    ('det_abort_cnt', u32, 8),
    ('reserved0', u32, 24),
]
class nrdma_tce_debug3(Structure):
    pass
nrdma_tce_debug3._fields_ = [
    ('reserved28', u32, 4),
    ('tx_pkt_cnt', u32, 8),
    ('reserved17', u32, 2),
    ('tce_ma_req', u32, 1),
    ('tce_ma_cmd_len', u32, 3),
    ('reserved0', u32, 12),
]
class nrdma_reserved_control(Structure):
    pass
nrdma_reserved_control._fields_ = [
    ('txmbuf_margin_nlso', u32, 11),
    ('reserved20', u32, 1),
    ('fifo_high_mark', u32, 8),
    ('fifo_low_mark', u32, 8),
    ('slow_clock_fix_dis', u32, 1),
    ('en_hw_fix_25155', u32, 1),
    ('reserved1', u32, 1),
    ('select_fed_enable', u32, 1),
]
class nrdma_flow_reserved_control(Structure):
    pass
nrdma_flow_reserved_control._fields_ = [
    ('reserved24', u32, 8),
    ('fifo_threshold_mbuf_req_msb', u32, 8),
    ('mbuf_threshold_mbuf_req', u32, 8),
    ('reserved4', u32, 4),
    ('fifo_hi_mark', u32, 1),
    ('fifo_lo_mark', u32, 1),
    ('reserved1', u32, 1),
    ('fifo_threshold_mbuf_req_lmsb', u32, 1),
]
class nrdma_corruption_enable_control(Structure):
    pass
nrdma_corruption_enable_control._fields_ = [
    ('lcrc_dr_fix_en', u32, 1),
    ('new_length_fix_en', u32, 1),
    ('reserved22', u32, 8),
    ('cq51816_nlso_fix_en', u32, 1),
    ('cq51036_nlso_fix_en', u32, 1),
    ('reserved15', u32, 5),
    ('sbd_8b_less_fix_en3', u32, 1),
    ('sbd_8b_less_fix_en2', u32, 1),
    ('mem_too_large_fix_en2', u32, 1),
    ('mem_too_large_fix_en1', u32, 1),
    ('mem_too_large_fix_en', u32, 1),
    ('sbd_9b_less_fix_en_fast_return', u32, 1),
    ('sbd_9b_less_fix_en', u32, 1),
    ('cq35774_hw_fix_en', u32, 1),
    ('reserved', u32, 7),
]
class nrdma_regs(Structure):
    pass
nrdma_regs._fields_ = [
    ('mode', nrdma_mode),
    ('status', nrdma_status),
    ('programmable_ipv6_extension_header', nrdma_programmable_ipv6_extension_header),
    ('rstates_debug', nrdma_rstates_debug),
    ('rstate2_debug', nrdma_rstate2_debug),
    ('bd_status_debug', nrdma_bd_status_debug),
    ('req_ptr_debug', nrdma_req_ptr_debug),
    ('hold_d_dmad_debug', nrdma_hold_d_dmad_debug),
    ('len_and_addr_debug', nrdma_length_and_address_debug),
    ('mbuf_byte_cnt_debug', nrdma_mbuf_byte_count_debug),
    ('pcie_debug_status', nrdma_pcie_debug_status),
    ('pcie_dma_read_req_debug', nrdma_pcie_dma_read_req_debug),
    ('pcie_dma_req_length_debug', nrdma_pcie_dma_req_length_debug),
    ('fifo1_debug', nrdma_fifo1_debug),
    ('fifo2_debug', nrdma_fifo2_debug),
    ('ofs_3c', u32),
    ('post_proc_pkt_req_cnt', nrdma_post_proc_pkt_req_cnt),
    ('ofs_44', u32),
    ('ofs_48', u32),
    ('ofs_4c', u32),
    ('ofs_50', u32),
    ('ofs_54', u32),
    ('ofs_58', u32),
    ('ofs_5c', u32),
    ('mbuf_addr_debug', nrdma_mbuf_addr_debug),
    ('tce_debug1', nrdma_tce_debug1),
    ('tce_debug2', nrdma_tce_debug2),
    ('tce_debug3', nrdma_tce_debug3),
    ('reserved_control', nrdma_reserved_control),
    ('flow_reserved_control', nrdma_flow_reserved_control),
    ('corruption_enable_control', nrdma_corruption_enable_control),
]
class ofs_7c(Structure):
    pass
ofs_7c._fields_ = [
]
class nvram_dir_item(Structure):
    pass
nvram_dir_item._fields_ = [
    ('sram_start', u32),
    ('typelen', u32),
    ('nvram_start', u32),
]
class nvram_header(Structure):
    pass
class N12nvram_header4DOT_54E(Structure):
    pass
N12nvram_header4DOT_54E._fields_ = [
    ('mgaic', u32),
    ('bc_sram_start', u32),
    ('bc_words', u32),
    ('bc_nvram_start', u32),
    ('crc', u32),
]
class N12nvram_header4DOT_55E(Structure):
    pass
N12nvram_header4DOT_55E._fields_ = [
    ('len', u16),
    ('dir_cksum', u8),
    ('rev', u8),
    ('_unused', u32),
    ('mac_address', u8 * 8),
    ('partno', c_char * 16),
    ('partrev', c_char * 2),
    ('bc_rev', u16),
    ('mfg_date', u8 * 4),
    ('mba_vlan_p1', u16),
    ('mba_vlan_p2', u16),
    ('pci_did', u16),
    ('pci_vid', u16),
    ('pci_ssid', u16),
    ('pci_svid', u16),
    ('cpu_mhz', u16),
    ('smbus_addr1', u8),
    ('smbus_addr0', u8),
    ('mac_backup', u8 * 8),
    ('mac_backup_p2', u8 * 8),
    ('power_dissipated', u32),
    ('power_consumed', u32),
    ('feat_cfg', u32),
    ('hw_cfg', u32),
    ('mac_address_p2', u8 * 8),
    ('feat_cfg_p2', u32),
    ('hw_cfg_p2', u32),
    ('shared_cfg', u32),
    ('power_budget_0', u32),
    ('power_budget_1', u32),
    ('serworks_use', u32),
    ('serdes_override', u32),
    ('tpm_nvram_size', u16),
    ('mac_nvram_size', u16),
    ('power_budget_2', u32),
    ('power_budget_3', u32),
    ('crc', u32),
]
nvram_header._fields_ = [
    ('bs', N12nvram_header4DOT_54E),
    ('directory', nvram_dir_item * 8),
    ('mfg', N12nvram_header4DOT_55E),
]
class nvram_command(Structure):
    pass
nvram_command._fields_ = [
    ('policy_error', u32, 4),
    ('atmel_page_size', u32, 1),
    ('reserved1', u32, 4),
    ('reserved2', u32, 1),
    ('reserved3', u32, 1),
    ('reserved4', u32, 1),
    ('wrsr', u32, 1),
    ('ewsr', u32, 1),
    ('write_disable_command', u32, 1),
    ('write_enable_command', u32, 1),
    ('reserved5', u32, 5),
    ('atmel_power_of_2_pg_sz', u32, 1),
    ('atmel_pg_sz_rd', u32, 1),
    ('last', u32, 1),
    ('first', u32, 1),
    ('erase', u32, 1),
    ('wr', u32, 1),
    ('doit', u32, 1),
    ('done', u32, 1),
    ('reserved6', u32, 2),
    ('reset', u32, 1),
]
class nvram_status(Structure):
    pass
nvram_status._fields_ = [
    ('reserved', u32, 1),
    ('spi_at_read_state', u32, 5),
    ('spi_at_write_state', u32, 6),
    ('spi_st_read_state', u32, 4),
    ('spi_st_write_state', u32, 6),
    ('seq_fsm_state', u32, 4),
    ('see_fsm_state', u32, 6),
]
class nvram_software_arbitration(Structure):
    pass
nvram_software_arbitration._fields_ = [
    ('reserved', u32, 16),
    ('req3', u32, 1),
    ('req2', u32, 1),
    ('req1', u32, 1),
    ('req0', u32, 1),
    ('arb_won3', u32, 1),
    ('arb_won2', u32, 1),
    ('arb_won1', u32, 1),
    ('arb_won0', u32, 1),
    ('req_clr3', u32, 1),
    ('req_clr2', u32, 1),
    ('req_clr1', u32, 1),
    ('req_clr0', u32, 1),
    ('req_set3', u32, 1),
    ('req_set2', u32, 1),
    ('req_set1', u32, 1),
    ('req_set0', u32, 1),
]
class nvram_access(Structure):
    pass
nvram_access._fields_ = [
    ('reserved', u32, 26),
    ('st_lockup_fix_enable', u32, 1),
    ('disable_auto_eeprom_reset', u32, 1),
    ('eprom_sda_oe_mode', u32, 1),
    ('ate_mode', u32, 1),
    ('write_enable', u32, 1),
    ('enable', u32, 1),
]
class nvram_write1(Structure):
    pass
nvram_write1._fields_ = [
    ('reserved', u32, 16),
    ('disable_command', u32, 8),
    ('enable_command', u32, 8),
]
class nvram_arbitration_watchdog(Structure):
    pass
nvram_arbitration_watchdog._fields_ = [
    ('reserved_31_28', u32, 4),
    ('reserved_27_24', u32, 4),
    ('reserved_23_8', u32, 16),
    ('reserved_7', u32, 1),
    ('reserved_6', u32, 1),
    ('reserved_5', u32, 1),
    ('reserved_4_0', u32, 5),
]
class nvram_auto_sense_status(Structure):
    pass
nvram_auto_sense_status._fields_ = [
    ('reserved21', u32, 11),
    ('device_id', u32, 5),
    ('reserved13', u32, 3),
    ('state', u32, 5),
    ('reserved6', u32, 2),
    ('successful', u32, 1),
    ('enable', u32, 1),
    ('reserved1', u32, 3),
    ('busy', u32, 1),
]
class nvram_regs(Structure):
    pass
nvram_regs._fields_ = [
    ('command', nvram_command),
    ('status', nvram_status),
    ('write_data', u32),
    ('data_address', u32),
    ('read_data', u32),
    ('config1', u32),
    ('config2', u32),
    ('config3', u32),
    ('sw_arb', nvram_software_arbitration),
    ('access', nvram_access),
    ('write1', nvram_write1),
    ('arbitration_watchdog_timer_register', nvram_arbitration_watchdog),
    ('address_lockout_boundary', u32),
    ('address_lockout_address_counter_debug', u32),
    ('auto_sense_status', nvram_auto_sense_status),
]
class otp_mode(Structure):
    pass
otp_mode._fields_ = [
    ('reserved', u32, 31),
    ('mode', u32, 1),
]
class otp_control(Structure):
    pass
otp_control._fields_ = [
    ('bypass_otp_clk', u32, 1),
    ('reserved', u32, 2),
    ('cpu_debug_sel', u32, 4),
    ('burst_stat_sel', u32, 1),
    ('access_mode', u32, 2),
    ('otp_prog_en', u32, 1),
    ('otp_debug_mode', u32, 1),
    ('wrp_continue_on_fail', u32, 1),
    ('wrp_time_margin', u32, 3),
    ('wrp_sadbyp', u32, 1),
    ('unused', u32, 1),
    ('wrp_pbyp', u32, 1),
    ('wrp_pcount', u32, 3),
    ('wrp_vsel', u32, 4),
    ('wrp_prog_sel', u32, 1),
    ('command', u32, 4),
    ('start', u32, 1),
]
class otp_status(Structure):
    pass
otp_status._fields_ = [
    ('reserved', u32, 20),
    ('control_error', u32, 1),
    ('wrp_error', u32, 1),
    ('invalid_command', u32, 1),
    ('otp_stby_reg', u32, 1),
    ('init_wait_done', u32, 1),
    ('prog_blocked', u32, 1),
    ('invalid_prog_req', u32, 1),
    ('wrp_fail', u32, 1),
    ('wrp_busy', u32, 1),
    ('wrp_dout', u32, 1),
    ('wrp_data_read', u32, 1),
    ('command_done', u32, 1),
]
class otp_addr(Structure):
    pass
otp_addr._fields_ = [
    ('reserved', u32, 16),
    ('address', u32, 16),
]
class otp_soft_reset(Structure):
    pass
otp_soft_reset._fields_ = [
    ('reserved', u32, 31),
    ('reset', u32, 1),
]
class otp_regs(Structure):
    pass
otp_regs._fields_ = [
    ('mode', otp_mode),
    ('control', otp_control),
    ('status', otp_status),
    ('address', otp_addr),
    ('write_data', u32),
    ('read_data', u32),
    ('soft_reset', otp_soft_reset),
]
class pci_status(Structure):
    pass
class N10pci_status4DOT_57E(Union):
    pass
class N10pci_status4DOT_574DOT_58E(Structure):
    pass
N10pci_status4DOT_574DOT_58E._fields_ = [
    ('detected_parity_error', u16, 1),
    ('signaled_system_error', u16, 1),
    ('received_master_abort', u16, 1),
    ('received_target_abort', u16, 1),
    ('signaled_target_abort', u16, 1),
    ('devsel_timing', u16, 2),
    ('master_data_parity_error', u16, 1),
    ('fast_back_to_back_capable', u16, 1),
    ('reserved', u16, 1),
    ('sixty_six_mhz_capable', u16, 1),
    ('capabilities_list', u16, 1),
    ('interrupt_status', u16, 1),
    ('reserved2', u16, 3),
]
N10pci_status4DOT_57E._anonymous_ = ['_0']
N10pci_status4DOT_57E._fields_ = [
    ('_0', N10pci_status4DOT_574DOT_58E),
    ('word', u16),
]
pci_status._anonymous_ = ['_0']
pci_status._fields_ = [
    ('_0', N10pci_status4DOT_57E),
]
class pci_command(Structure):
    pass
class N11pci_command4DOT_59E(Union):
    pass
class N11pci_command4DOT_594DOT_60E(Structure):
    pass
N11pci_command4DOT_594DOT_60E._fields_ = [
    ('reserved3', u16, 5),
    ('interrupt_disable', u16, 1),
    ('fast_back_to_back_enable', u16, 1),
    ('system_error_enable', u16, 1),
    ('stepping_control', u16, 1),
    ('parity_error_enable', u16, 1),
    ('vga_palette_snoop', u16, 1),
    ('memory_write_and_invalidate', u16, 1),
    ('special_cycles', u16, 1),
    ('bus_master', u16, 1),
    ('memory_space', u16, 1),
    ('io_space', u16, 1),
]
N11pci_command4DOT_59E._anonymous_ = ['_0']
N11pci_command4DOT_59E._fields_ = [
    ('_0', N11pci_command4DOT_594DOT_60E),
    ('word', u16),
]
pci_command._anonymous_ = ['_0']
pci_command._fields_ = [
    ('_0', N11pci_command4DOT_59E),
]
class pci_pm_cap(Structure):
    pass
pci_pm_cap._fields_ = [
    ('pme_support', u32, 5),
    ('d2_support', u32, 1),
    ('d1_support', u32, 1),
    ('aux_current', u32, 3),
    ('dsi', u32, 1),
    ('reserved6', u32, 1),
    ('pme_clock', u32, 1),
    ('version', u32, 3),
    ('next_cap', u32, 8),
    ('cap_id', u32, 8),
]
class pci_pm_ctrl_status(Structure):
    pass
pci_pm_ctrl_status._fields_ = [
    ('pm_data', u32, 8),
    ('reserved7', u32, 8),
    ('pme_status', u32, 1),
    ('data_scale', u32, 2),
    ('data_select', u32, 4),
    ('pme_enable', u32, 1),
    ('reserved8', u32, 4),
    ('no_soft_reset', u32, 1),
    ('reserved9', u32, 1),
    ('power_state', u32, 2),
]
class pci_msi_cap_hdr(Structure):
    pass
pci_msi_cap_hdr._fields_ = [
    ('msi_control', u32, 7),
    ('msi_pvmask_capable', u32, 1),
    ('sixty_four_bit_addr_capable', u32, 1),
    ('multiple_message_enable', u32, 3),
    ('multiple_message_capable', u32, 3),
    ('msi_enable', u32, 1),
    ('next_cap', u32, 8),
    ('cap_id', u32, 8),
]
class pci_misc_host_ctrl(Structure):
    pass
pci_misc_host_ctrl._fields_ = [
    ('asic_rev_id', u32, 16),
    ('unused', u32, 6),
    ('enable_tagged_status_mode', u32, 1),
    ('mask_interrupt_mode', u32, 1),
    ('enable_indirect_access', u32, 1),
    ('enable_register_word_swap', u32, 1),
    ('enable_clock_control_register_rw_cap', u32, 1),
    ('enable_pci_state_register_rw_cap', u32, 1),
    ('enable_endian_word_swap', u32, 1),
    ('enable_endian_byte_swap', u32, 1),
    ('mask_interrupt', u32, 1),
    ('clear_interrupt', u32, 1),
]
class pci_dma_rw_ctrl(Structure):
    pass
pci_dma_rw_ctrl._fields_ = [
    ('reserved25', u32, 7),
    ('cr_write_watermark', u32, 3),
    ('dma_write_watermark', u32, 3),
    ('reserved10', u32, 9),
    ('card_reader_dma_read_mrrs', u32, 3),
    ('dma_read_mrrs_for_slow_speed', u32, 3),
    ('reserved1', u32, 3),
    ('disable_cache_alignment', u32, 1),
]
class pci_state(Structure):
    pass
pci_state._fields_ = [
    ('reserved20', u32, 12),
    ('generate_reset_pulse', u32, 1),
    ('ape_ps_wr_en', u32, 1),
    ('ape_shm_wr_en', u32, 1),
    ('ape_ctrl_reg_wr_en', u32, 1),
    ('config_retry', u32, 1),
    ('reserved15', u32, 2),
    ('pci_vaux_present', u32, 1),
    ('max_retry', u32, 3),
    ('flat_view', u32, 1),
    ('vpd_available', u32, 1),
    ('rom_retry_enable', u32, 1),
    ('rom_enable', u32, 1),
    ('bus_32_bit', u32, 1),
    ('bus_speed_hi', u32, 1),
    ('conv_pci_mode', u32, 1),
    ('int_not_active', u32, 1),
    ('force_reset', u32, 1),
]
class pci_device_id(Structure):
    pass
pci_device_id._fields_ = [
    ('did', u32, 16),
    ('vid', u32, 16),
]
class pci_class_code_rev_id(Structure):
    pass
pci_class_code_rev_id._fields_ = [
    ('class_code', u32, 24),
    ('rev_id', u32, 8),
]
class pci_regs(Structure):
    pass
class N8pci_regs4DOT_61E(Structure):
    pass
N8pci_regs4DOT_61E._fields_ = [
    ('did', u32, 16),
    ('vid', u32, 16),
]
class N8pci_regs4DOT_62E(Structure):
    pass
N8pci_regs4DOT_62E._fields_ = [
    ('status', pci_status),
    ('command', pci_command),
]
class N8pci_regs4DOT_63E(Structure):
    pass
N8pci_regs4DOT_63E._fields_ = [
    ('bist', u8, 8),
    ('hdr_type', u32, 8),
    ('lat_timer', u32, 8),
    ('cache_line_sz', u32, 8),
]
class N8pci_regs4DOT_64E(Structure):
    pass
N8pci_regs4DOT_64E._fields_ = [
    ('ssid', u16),
    ('svid', u16),
]
class N8pci_regs4DOT_65E(Structure):
    pass
N8pci_regs4DOT_65E._fields_ = [
    ('reserved1', u32, 24),
    ('cap_ptr', u32, 8),
]
class N8pci_regs4DOT_66E(Structure):
    pass
N8pci_regs4DOT_66E._fields_ = [
    ('max_lat', u32, 8),
    ('min_gnt', u32, 8),
    ('int_pin', u32, 8),
    ('int_line', u32, 8),
]
pci_regs._anonymous_ = ['_5', '_3', '_2', '_0', '_4', '_1']
pci_regs._fields_ = [
    ('_0', N8pci_regs4DOT_61E),
    ('_1', N8pci_regs4DOT_62E),
    ('class_code_rev_id', pci_class_code_rev_id),
    ('_2', N8pci_regs4DOT_63E),
    ('bar0_hi', u32),
    ('bar0_low', u32),
    ('bar1_hi', u32),
    ('bar1_low', u32),
    ('bar2_hi', u32),
    ('bar2_low', u32),
    ('cardbus_cis_ptr', u32),
    ('_3', N8pci_regs4DOT_64E),
    ('rombar', u32),
    ('_4', N8pci_regs4DOT_65E),
    ('reserved2', u32),
    ('_5', N8pci_regs4DOT_66E),
    ('int_mailbox', u64),
    ('pm_cap', pci_pm_cap),
    ('pm_ctrl_status', pci_pm_ctrl_status),
    ('unknown2', u32 * 2),
    ('msi_cap_hdr', pci_msi_cap_hdr),
    ('msi_lower_address', u32),
    ('msi_upper_address', u32),
    ('msi_data', u32),
    ('misc_host_ctrl', pci_misc_host_ctrl),
    ('dma_rw_ctrl', pci_dma_rw_ctrl),
    ('state', pci_state),
    ('reset_counters_initial_values', u32),
    ('reg_base_addr', u32),
    ('mem_base_addr', u32),
    ('reg_data', u32),
    ('mem_data', u32),
    ('unknown3', u32 * 2),
    ('misc_local_control', u32),
    ('unknown4', u32),
    ('std_ring_prod_ci_hi', u32),
    ('std_ring_prod_ci_low', u32),
    ('recv_ret_ring_ci_hi', u32),
    ('recv_ret_ring_ci_low', u32),
]
class pcie_tl_tlp_ctrl(Structure):
    pass
pcie_tl_tlp_ctrl._fields_ = [
    ('excessive_current_fix_en', u32, 1),
    ('reserved30', u32, 1),
    ('int_mode_fix_en', u32, 1),
    ('reserved28', u32, 1),
    ('unexpected_completion_err_fix_en', u32, 1),
    ('type1_vendor_defined_msg_fix_en', u32, 1),
    ('data_fifo_protect', u32, 1),
    ('address_check_en', u32, 1),
    ('tc0_check_en', u32, 1),
    ('crc_swap', u32, 1),
    ('ca_err_dis', u32, 1),
    ('ur_err_dis', u32, 1),
    ('rsv_err_dis', u32, 1),
    ('mps_chk_en', u32, 1),
    ('ep_err_dis', u32, 1),
    ('bytecount_chk_en', u32, 1),
    ('reserved14', u32, 2),
    ('dma_read_traffic_class', u32, 3),
    ('dma_write_traffic_class', u32, 3),
    ('reserved6', u32, 2),
    ('completion_timeout', u32, 6),
]
class pcie_tl_transaction_config(Structure):
    pass
pcie_tl_transaction_config._fields_ = [
    ('retry_buffer_timining_mod_en', u32, 1),
    ('reserved30', u32, 1),
    ('one_shot_msi_en', u32, 1),
    ('reserved28', u32, 1),
    ('select_core_clock_override', u32, 1),
    ('cq9139_fix_en', u32, 1),
    ('cmpt_pwr_check_en', u32, 1),
    ('cq12696_fix_en', u32, 1),
    ('device_serial_no_override', u32, 1),
    ('cq12455_fix_en', u32, 1),
    ('tc_vc_filtering_check_en', u32, 1),
    ('dont_gen_hot_plug_msg', u32, 1),
    ('ignore_hot_plug_msg', u32, 1),
    ('msi_multimsg_cap', u32, 3),
    ('data_select_limit', u32, 4),
    ('pcie_1_1_pl_en', u32, 1),
    ('pcie_1_1_dl_en', u32, 1),
    ('pcie_1_1_tl_en', u32, 1),
    ('reserved7', u32, 2),
    ('pcie_power_budget_cap_en', u32, 1),
    ('lom_configuration', u32, 1),
    ('concate_select', u32, 1),
    ('ur_status_bit_fix_en', u32, 1),
    ('vendor_defined_msg_fix_en', u32, 1),
    ('power_state_write_mem_enable', u32, 1),
    ('reserved0', u32, 1),
]
class pcie_tl_wdma_len_byte_en_req_diag(Structure):
    pass
pcie_tl_wdma_len_byte_en_req_diag._fields_ = [
    ('request_length', u32, 16),
    ('byte_enables', u32, 8),
    ('reserved1', u32, 7),
    ('raw_request', u32, 1),
]
class pcie_tl_rdma_len_req_diag(Structure):
    pass
pcie_tl_rdma_len_req_diag._fields_ = [
    ('request_length', u32, 16),
    ('reserved1', u32, 15),
    ('raw_request', u32, 1),
]
class pcie_tl_msi_len_req_diag(Structure):
    pass
pcie_tl_msi_len_req_diag._fields_ = [
    ('request_length', u32, 16),
    ('reserved1', u32, 15),
    ('raw_request', u32, 1),
]
class pcie_tl_slave_req_len_type_diag(Structure):
    pass
pcie_tl_slave_req_len_type_diag._fields_ = [
    ('reg_slv_len_req', u32, 6),
    ('request_length', u32, 10),
    ('reserved2', u32, 14),
    ('request_type', u32, 1),
    ('raw_request', u32, 1),
]
class pcie_tl_flow_control_inputs_diag(Structure):
    pass
pcie_tl_flow_control_inputs_diag._fields_ = [
    ('reg_fc_input', u32, 5),
    ('non_posted_header_avail', u32, 1),
    ('posted_header_avail', u32, 1),
    ('completion_header_avail', u32, 1),
    ('posted_data_avail', u32, 12),
    ('completion_data_avail', u32, 12),
]
class pcie_tl_xmt_state_machines_gated_reqs_diag(Structure):
    pass
pcie_tl_xmt_state_machines_gated_reqs_diag._fields_ = [
    ('reg_sm_r0_r3', u32, 1),
    ('tlp_tx_data_state_machine', u32, 3),
    ('tlp_tx_arb_state_machine', u32, 4),
    ('reserved4', u32, 20),
    ('slave_dma_gated_req', u32, 1),
    ('msi_dma_gated_req', u32, 1),
    ('read_dma_gated_req', u32, 1),
    ('write_dma_gated_req', u32, 1),
]
class pcie_tl_tlp_bdf(Structure):
    pass
pcie_tl_tlp_bdf._fields_ = [
    ('reserved17', u32, 15),
    ('config_write_indicator', u32, 1),
    ('bus', u32, 8),
    ('device', u32, 5),
    ('function', u32, 3),
]
class pcie_tl_regs(Structure):
    pass
pcie_tl_regs._fields_ = [
    ('tlp_ctrl', pcie_tl_tlp_ctrl),
    ('transaction_config', pcie_tl_transaction_config),
    ('ofs_08', u32),
    ('ofs_0c', u32),
    ('wdma_req_upper_addr_diag', u32),
    ('wdma_req_lower_addr_diag', u32),
    ('wdma_len_byte_en_req_diag', pcie_tl_wdma_len_byte_en_req_diag),
    ('rdma_req_upper_addr_diag', u32),
    ('rdma_req_lower_addr_diag', u32),
    ('rdma_len_req_diag', pcie_tl_rdma_len_req_diag),
    ('msi_dma_req_upper_addr_diag', u32),
    ('msi_dma_req_lower_addr_diag', u32),
    ('msi_dma_len_req_diag', pcie_tl_msi_len_req_diag),
    ('slave_req_len_type_diag', pcie_tl_slave_req_len_type_diag),
    ('flow_control_inputs_diag', pcie_tl_flow_control_inputs_diag),
    ('xmt_state_machines_gated_reqs_diag', pcie_tl_xmt_state_machines_gated_reqs_diag),
    ('address_ack_xfer_count_and_arb_length_diag', u32),
    ('dma_completion_header_diag_0', u32),
    ('dma_completion_header_diag_1', u32),
    ('dma_completion_header_diag_2', u32),
    ('dma_completion_misc_diag_0', u32),
    ('dma_completion_misc_diag_1', u32),
    ('dma_completion_misc_diag_2', u32),
    ('split_controller_req_length_address_ack_remaining_diag', u32),
    ('split_controller_misc_diag_0', u32),
    ('split_controller_misc_diag_1', u32),
    ('bdf', pcie_tl_tlp_bdf),
    ('tlp_debug', u32),
    ('retry_buffer_free', u32),
    ('target_debug_1', u32),
    ('target_debug_2', u32),
    ('target_debug_3', u32),
    ('target_debug_4', u32),
]
class pcie_dl_ctrl(Structure):
    pass
pcie_dl_ctrl._fields_ = [
    ('reserved19', u32, 13),
    ('pll_refsel_sw', u32, 1),
    ('reserved17', u32, 1),
    ('power_management_ctrl_en', u32, 1),
    ('power_down_serdes_transmitter', u32, 1),
    ('power_down_serdes_pll', u32, 1),
    ('power_down_serdes_receiver', u32, 1),
    ('enable_beacon', u32, 1),
    ('automatic_timer_threshold_en', u32, 1),
    ('dllp_timeout_mech_en', u32, 1),
    ('chk_rcv_flow_ctrl_credits', u32, 1),
    ('link_enable', u32, 1),
    ('power_management_ctrl', u32, 8),
]
class pcie_dl_status(Structure):
    pass
pcie_dl_status._fields_ = [
    ('reserved26', u32, 6),
    ('phy_link_state', u32, 3),
    ('power_management_state', u32, 4),
    ('power_management_substate', u32, 2),
    ('data_link_up', u32, 1),
    ('reserved11', u32, 5),
    ('pme_turn_off_status_in_d0', u32, 1),
    ('flow_ctrl_update_timeout', u32, 1),
    ('flow_ctrl_recv_oflow', u32, 1),
    ('flow_ctrl_proto_err', u32, 1),
    ('data_link_proto_err', u32, 1),
    ('replay_rollover', u32, 1),
    ('replay_timeout', u32, 1),
    ('nak_recvd', u32, 1),
    ('dllp_error', u32, 1),
    ('bad_tlp_seq_no', u32, 1),
    ('tlp_error', u32, 1),
]
class pcie_dl_attn(Structure):
    pass
pcie_dl_attn._fields_ = [
    ('reserved5', u32, 27),
    ('data_link_layer_attn_ind', u32, 1),
    ('nak_rcvd_cntr_attn_ind', u32, 1),
    ('dllp_err_cntr_attn_ind', u32, 1),
    ('tlp_bad_seq_cntr_attn_ind', u32, 1),
    ('tlp_err_cntr_attn_ind', u32, 1),
]
class pcie_dl_attn_mask(Structure):
    pass
pcie_dl_attn_mask._fields_ = [
    ('reserved8', u32, 24),
    ('attn_mask', u32, 3),
    ('data_link_layer_attn_mask', u32, 1),
    ('nak_rcvd_cntr_attn_mask', u32, 1),
    ('dllp_err_cntr_attn_mask', u32, 1),
    ('tlp_bad_seq_cntr_attn_mask', u32, 1),
    ('tlp_err_cntr_attn_mask', u32, 1),
]
class pcie_dl_seq_no(Structure):
    pass
pcie_dl_seq_no._fields_ = [
    ('reserved12', u32, 20),
    ('value', u32, 12),
]
class pcie_dl_replay(Structure):
    pass
pcie_dl_replay._fields_ = [
    ('reserved23', u32, 9),
    ('timeout_value', u32, 13),
    ('buffer_size', u32, 10),
]
class pcie_dl_ack_timeout(Structure):
    pass
pcie_dl_ack_timeout._fields_ = [
    ('reserved11', u32, 21),
    ('value', u32, 11),
]
class pcie_dl_pm_threshold(Structure):
    pass
pcie_dl_pm_threshold._fields_ = [
    ('reserved24', u32, 8),
    ('l0_stay_time', u32, 4),
    ('l1_stay_time', u32, 4),
    ('l1_threshold', u32, 8),
    ('l0s_threshold', u32, 8),
]
class pcie_dl_retry_buffer_ptr(Structure):
    pass
pcie_dl_retry_buffer_ptr._fields_ = [
    ('reserved11', u32, 21),
    ('value', u32, 11),
]
class pcie_dl_test(Structure):
    pass
pcie_dl_test._fields_ = [
    ('reserved16', u32, 16),
    ('store_recv_tlps', u32, 1),
    ('disable_tlps', u32, 1),
    ('disable_dllps', u32, 1),
    ('force_phy_link_up', u32, 1),
    ('bypass_flow_ctrl', u32, 1),
    ('ram_core_clock_margin_test_en', u32, 1),
    ('ram_overstress_test_en', u32, 1),
    ('ram_read_margin_test_en', u32, 1),
    ('speed_up_completion_timer', u32, 1),
    ('speed_up_replay_timer', u32, 1),
    ('speed_up_ack_latency_timer', u32, 1),
    ('speed_up_pme_service_timer', u32, 1),
    ('force_purge', u32, 1),
    ('force_retry', u32, 1),
    ('invert_crc', u32, 1),
    ('send_bad_crc_bit', u32, 1),
]
class pcie_dl_packet_bist(Structure):
    pass
pcie_dl_packet_bist._fields_ = [
    ('reserved24', u32, 8),
    ('packet_checker_loaded', u32, 1),
    ('recv_mismatch', u32, 1),
    ('rand_tlp_len_en', u32, 1),
    ('tlp_len', u32, 11),
    ('random_ipg_len_en', u32, 1),
    ('ipg_len', u32, 7),
    ('transmit_start', u32, 1),
    ('packet_generator_test_mode_en', u32, 1),
]
class pcie_dl_regs(Structure):
    pass
pcie_dl_regs._fields_ = [
    ('dl_ctrl', pcie_dl_ctrl),
    ('dl_status', pcie_dl_status),
    ('dl_attn', pcie_dl_attn),
    ('dl_attn_mask', pcie_dl_attn_mask),
    ('next_transmit_seq_no', pcie_dl_seq_no),
    ('acked_transmit_seq_no', pcie_dl_seq_no),
    ('purged_transmit_seq_no', pcie_dl_seq_no),
    ('receive_req_no', pcie_dl_seq_no),
    ('replay', pcie_dl_replay),
    ('ack_timeout', pcie_dl_ack_timeout),
    ('power_mgmt_threshold', pcie_dl_pm_threshold),
    ('retry_buffer_write_ptr', pcie_dl_retry_buffer_ptr),
    ('retry_buffer_read_ptr', pcie_dl_retry_buffer_ptr),
    ('retry_buffer_purged_ptr', pcie_dl_retry_buffer_ptr),
    ('retry_buffer_read_write_port', u32),
    ('error_count_threshold', u32),
    ('tlp_error_counter', u32),
    ('dllp_error_counter', u32),
    ('nak_received_counter', u32),
    ('test', pcie_dl_test),
    ('packet_bist', pcie_dl_packet_bist),
    ('link_pcie_1_1_control', u32),
]
class pcie_pl_regs(Structure):
    pass
pcie_pl_regs._fields_ = [
    ('phy_mode', u32),
    ('phy_link_status', u32),
    ('phy_link_ltssm_control', u32),
    ('phy_link_training_link_number', u32),
    ('phy_link_training_lane_number', u32),
    ('phy_link_training_n_fts', u32),
    ('phy_attention', u32),
    ('phy_attention_mask', u32),
    ('phy_receive_error_counter', u32),
    ('phy_receive_framing_error_counter', u32),
    ('phy_receive_error_threshold', u32),
    ('phy_test_control', u32),
    ('phy_serdes_control_override', u32),
    ('phy_timing_parameter_override', u32),
    ('phy_hardware_diag_1', u32),
    ('phy_hardware_diag_2', u32),
]
class pcie_pl_lo_regs(Structure):
    pass
pcie_pl_lo_regs._fields_ = [
    ('phyctl0', u32),
    ('phyctl1', u32),
    ('phyctl2', u32),
    ('phyctl3', u32),
    ('phyctl4', u32),
    ('phyctl5', u32),
]
class pcie_dl_lo_ftsmax(Structure):
    pass
pcie_dl_lo_ftsmax._fields_ = [
    ('unknown', u32, 24),
    ('val', u32, 8),
]
class pcie_dl_lo_regs(Structure):
    pass
pcie_dl_lo_regs._fields_ = [
    ('unknown0', u32),
    ('unknown4', u32),
    ('unknown8', u32),
    ('ftsmax', pcie_dl_lo_ftsmax),
]
class pcie_alt_regs(Structure):
    pass
class N13pcie_alt_regs4DOT_56E(Union):
    pass
N13pcie_alt_regs4DOT_56E._fields_ = [
    ('dll', pcie_dl_lo_regs),
    ('pll', pcie_pl_lo_regs),
]
pcie_alt_regs._anonymous_ = ['_0']
pcie_alt_regs._fields_ = [
    ('_0', N13pcie_alt_regs4DOT_56E),
]
class rbdc_mode(Structure):
    pass
class N9rbdc_mode4DOT_67E(Structure):
    pass
N9rbdc_mode4DOT_67E._fields_ = [
    ('reserved', u32, 29),
    ('attention_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
rbdc_mode._anonymous_ = ['_0']
rbdc_mode._fields_ = [
    ('_0', N9rbdc_mode4DOT_67E),
]
class rbdc_status(Structure):
    pass
rbdc_status._fields_ = [
    ('reserved', u32, 29),
    ('error', u32, 1),
    ('reserved2', u32, 2),
]
class rbdc_rbd_pi(Structure):
    pass
rbdc_rbd_pi._fields_ = [
    ('reserved', u32, 23),
    ('bd_pi', u32, 9),
]
class rbdc_regs(Structure):
    pass
rbdc_regs._fields_ = [
    ('mode', rbdc_mode),
    ('status', rbdc_status),
    ('jumbo_rbd_pi', rbdc_rbd_pi),
    ('std_rbd_pi', rbdc_rbd_pi),
    ('mini_rbd_pi', rbdc_rbd_pi),
]
class rbdi_mode(Structure):
    pass
class N9rbdi_mode4DOT_68E(Union):
    pass
class N9rbdi_mode4DOT_684DOT_69E(Structure):
    pass
N9rbdi_mode4DOT_684DOT_69E._fields_ = [
    ('reserved', u32, 29),
    ('receive_bds_available_on_disabled_rbd_ring_attn_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
N9rbdi_mode4DOT_68E._anonymous_ = ['_0']
N9rbdi_mode4DOT_68E._fields_ = [
    ('_0', N9rbdi_mode4DOT_684DOT_69E),
    ('word', u32),
]
rbdi_mode._anonymous_ = ['_0']
rbdi_mode._fields_ = [
    ('_0', N9rbdi_mode4DOT_68E),
]
class rbdi_status(Structure):
    pass
rbdi_status._fields_ = [
    ('reserved', u32, 29),
    ('receive_bds_available_on_disabled_rbd_ring', u32, 1),
    ('reserved2', u32, 2),
]
class rbdi_ring_replenish_threshold(Structure):
    pass
rbdi_ring_replenish_threshold._fields_ = [
    ('reserved', u32, 22),
    ('count', u32, 10),
]
class rbdi_regs(Structure):
    pass
rbdi_regs._fields_ = [
    ('mode', rbdi_mode),
    ('status', rbdi_status),
    ('local_jumbo_rbd_pi', u32),
    ('local_std_rbd_pi', u32),
    ('local_mini_rbd_pi', u32),
    ('mini_ring_replenish_threshold', rbdi_ring_replenish_threshold),
    ('std_ring_replenish_threshold', rbdi_ring_replenish_threshold),
    ('jumbo_ring_replenish_threshold', rbdi_ring_replenish_threshold),
    ('reserved', u32 * 56),
    ('std_ring_replenish_watermark', rbdi_ring_replenish_threshold),
    ('jumbo_ring_replenish_watermark', rbdi_ring_replenish_threshold),
]
class rbd_rule(Structure):
    pass
rbd_rule._fields_ = [
    ('enabled', u32, 1),
    ('and_with_next', u32, 1),
    ('p1', u32, 1),
    ('p2', u32, 1),
    ('p3', u32, 1),
    ('mask', u32, 1),
    ('discard', u32, 1),
    ('map', u32, 1),
    ('reserved', u32, 6),
    ('op', u32, 2),
    ('header', u32, 3),
    ('frame_class', u32, 5),
    ('offset', u32, 8),
]
class rbd_value_mask(Structure):
    pass
rbd_value_mask._fields_ = [
    ('mask', u16),
    ('value', u16),
]
class rcb_flags(Structure):
    pass
rcb_flags._fields_ = [
    ('reserved', u16, 1),
    ('disabled', u16, 1),
    ('reserved2', u16, 14),
]
class rcb(Structure):
    pass
rcb._fields_ = [
    ('addr_hi', u32),
    ('addr_low', u32),
    ('flags', rcb_flags),
    ('max_len', u16),
    ('nic_addr', u32),
]
class rdc_mode(Structure):
    pass
class N8rdc_mode4DOT_70E(Union):
    pass
class N8rdc_mode4DOT_704DOT_71E(Structure):
    pass
N8rdc_mode4DOT_704DOT_71E._fields_ = [
    ('reserved', u32, 29),
    ('attention_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
N8rdc_mode4DOT_70E._anonymous_ = ['_0']
N8rdc_mode4DOT_70E._fields_ = [
    ('_0', N8rdc_mode4DOT_704DOT_71E),
    ('word', u32),
]
rdc_mode._anonymous_ = ['_0']
rdc_mode._fields_ = [
    ('_0', N8rdc_mode4DOT_70E),
]
class rdc_regs(Structure):
    pass
rdc_regs._fields_ = [
    ('mode', rdc_mode),
]
class rdi_mode(Structure):
    pass
rdi_mode._fields_ = [
    ('reserved', u32, 27),
    ('illegal_return_ring_size', u32, 1),
    ('frame_size_too_large_for_bd', u32, 1),
    ('reserved2', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
class rdi_status(Structure):
    pass
rdi_status._fields_ = [
    ('reserved', u32, 27),
    ('illegal_return_ring_size', u32, 1),
    ('frame_size_too_large_for_bd', u32, 1),
    ('reserved2', u32, 3),
]
class rcb_registers(Structure):
    pass
class N13rcb_registers4DOT_72E(Structure):
    pass
N13rcb_registers4DOT_72E._fields_ = [
    ('ring_size', u32, 16),
    ('max_frame_len', u32, 14),
    ('disable_ring', u32, 1),
    ('reserved', u32, 1),
]
rcb_registers._anonymous_ = ['_0']
rcb_registers._fields_ = [
    ('host_addr_hi', u32),
    ('host_addr_low', u32),
    ('_0', N13rcb_registers4DOT_72E),
    ('nic_addr', u32),
]
class rdi_regs(Structure):
    pass
rdi_regs._fields_ = [
    ('mode', rdi_mode),
    ('status', rdi_status),
    ('unknown', u32 * 14),
    ('jumbo_rcb', rcb_registers),
    ('std_rcb', rcb_registers),
    ('mini_rcb', rcb_registers),
    ('local_jumbo_rbd_ci', u32),
    ('local_std_rbd_ci', u32),
    ('local_mini_rbd_ci', u32),
    ('unknown2', u32),
    ('local_rr_pi', u32 * 16),
    ('hw_diag', u32),
]
class rdma_mode(Structure):
    pass
rdma_mode._fields_ = [
    ('reserved', u32, 2),
    ('in_band_vtag_enable', u32, 1),
    ('hardware_ipv6_post_dma_processing_enable', u32, 1),
    ('hardware_ipv4_post_dma_processing_enable', u32, 1),
    ('post_dma_debug_enable', u32, 1),
    ('address_overflow_error_logging_enable', u32, 1),
    ('mmrr_disable', u32, 1),
    ('jumbo_2k_mmrr_mode', u32, 1),
    ('reserved2', u32, 5),
    ('pci_request_burst_length', u32, 2),
    ('reserved3', u32, 2),
    ('mbuf_sbd_corruption_attn_enable', u32, 1),
    ('mbuf_rbd_corruption_attn_enable', u32, 1),
    ('bd_sbd_corruption_attn_enable', u32, 1),
    ('read_dma_pci_x_split_transaction_timeout_expired_attention_enable', u32, 1),
    ('read_dma_local_memory_write_longer_than_dma_length_attention_enable', u32, 1),
    ('read_dma_pci_fifo_overread_attention_enable', u32, 1),
    ('read_dma_pci_fifo_underrun_attention_enable', u32, 1),
    ('read_dma_pci_fifo_overrun_attention_enable', u32, 1),
    ('read_dma_pci_host_address_overflow_error_attention_enable', u32, 1),
    ('read_dma_pci_parity_error_attention_enable', u32, 1),
    ('read_dma_pci_master_abort_attention_enable', u32, 1),
    ('read_dma_pci_target_abort_attention_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
class rdma_status(Structure):
    pass
rdma_status._fields_ = [
    ('reserved', u32, 18),
    ('mbuf_sbd_corruption_attention', u32, 1),
    ('mbuf_rbd_corruption_attention', u32, 1),
    ('bd_sbd_corruption_attention', u32, 1),
    ('read_dma_pci_x_split_transaction_timeout_expired', u32, 1),
    ('read_dma_local_memory_write_longer_than_dma_length_error', u32, 1),
    ('read_dma_pci_fifo_overread_error', u32, 1),
    ('read_dma_pci_fifo_underrun_error', u32, 1),
    ('read_dma_pci_fifo_overrun_error', u32, 1),
    ('read_dma_pci_host_address_overflow_error', u32, 1),
    ('read_dma_completion_timer_timeout', u32, 1),
    ('read_dma_completer_abort', u32, 1),
    ('read_dma_unsupported_request', u32, 1),
    ('reserved2', u32, 2),
]
class rdma_programmable_ipv6_extension_header(Structure):
    pass
rdma_programmable_ipv6_extension_header._fields_ = [
    ('type_2_en', u32, 1),
    ('type_1_en', u32, 1),
    ('reserved16', u32, 14),
    ('ext_hdr_type_2', u32, 8),
    ('ext_hdr_type_1', u32, 8),
]
class rdma_rstates_debug(Structure):
    pass
rdma_rstates_debug._fields_ = [
    ('reserved6', u32, 26),
    ('rstate3', u32, 2),
    ('reserved3', u32, 1),
    ('rstate1', u32, 3),
]
class rdma_rstate2_debug(Structure):
    pass
rdma_rstate2_debug._fields_ = [
    ('reserved5', u32, 27),
    ('rstate2', u32, 5),
]
class rdma_bd_status_debug(Structure):
    pass
rdma_bd_status_debug._fields_ = [
    ('reserved3', u32, 29),
    ('bd_non_mbuf', u32, 1),
    ('fst_bd_mbuf', u32, 1),
    ('lst_bd_mbuf', u32, 1),
]
class rdma_req_ptr_debug(Structure):
    pass
rdma_req_ptr_debug._fields_ = [
    ('ih_dmad_length', u32, 16),
    ('reserved10', u32, 6),
    ('txmbuf_left', u32, 6),
    ('rh_dmad_load_en', u32, 1),
    ('rftq_d_dmad_pnt', u32, 2),
    ('rftq_b_dmad_pnt', u32, 1),
]
class rdma_hold_d_dmad_debug(Structure):
    pass
rdma_hold_d_dmad_debug._fields_ = [
    ('reserved2', u32, 30),
    ('rhold_d_dmad', u32, 2),
]
class rdma_length_and_address_index_debug(Structure):
    pass
rdma_length_and_address_index_debug._fields_ = [
    ('rdma_rd_length', u32, 16),
    ('mbuf_addr_idx', u32, 16),
]
class rdma_mbuf_byte_count_debug(Structure):
    pass
rdma_mbuf_byte_count_debug._fields_ = [
    ('reserved4', u32, 28),
    ('rmbuf_byte_cnt', u32, 4),
]
class rdma_pcie_mbuf_byte_count_debug(Structure):
    pass
rdma_pcie_mbuf_byte_count_debug._fields_ = [
    ('lt_term', u32, 4),
    ('reserved27', u32, 1),
    ('lt_too_lg', u32, 1),
    ('lt_dma_reload', u32, 1),
    ('lt_dma_good', u32, 1),
    ('cur_trans_active', u32, 1),
    ('drpcireq', u32, 1),
    ('dr_pci_word_swap', u32, 1),
    ('dr_pci_byte_swap', u32, 1),
    ('new_slow_core_clk_mode', u32, 1),
    ('rbd_non_mbuf', u32, 1),
    ('rfst_bd_mbuf', u32, 1),
    ('rlst_bd_mbuf', u32, 1),
    ('dr_pci_len', u32, 16),
]
class rdma_pcie_read_request_address_debug(Structure):
    pass
rdma_pcie_read_request_address_debug._fields_ = [
    ('dr_pci_ad_hi', u32, 16),
    ('dr_pci_ad_lo', u32, 16),
]
class rdma_fifo1_debug(Structure):
    pass
rdma_fifo1_debug._fields_ = [
    ('reserved8', u32, 24),
    ('c_write_addr', u32, 8),
]
class rdma_fifo2_debug(Structure):
    pass
rdma_fifo2_debug._fields_ = [
    ('reserved16', u32, 16),
    ('rlctrl_in', u32, 8),
    ('c_read_addr', u32, 8),
]
class rdma_packet_request_debug_1(Structure):
    pass
rdma_packet_request_debug_1._fields_ = [
    ('reserved8', u32, 24),
    ('pkt_req_cnt', u32, 8),
]
class rdma_packet_request_debug_2(Structure):
    pass
rdma_packet_request_debug_2._fields_ = [
    ('sdc_ack_cnt', u32),
]
class rdma_packet_request_debug_3(Structure):
    pass
rdma_packet_request_debug_3._fields_ = [
    ('cs', u32, 4),
    ('reserved26', u32, 2),
    ('lt_fst_seg', u32, 1),
    ('lt_lst_seg', u32, 1),
    ('lt_mem_ip_hdr_ofst', u32, 8),
    ('lt_mem_tcp_hdr_ofst', u32, 8),
    ('reserved7', u32, 1),
    ('pre_sdcq_pkt_cnt', u32, 7),
]
class rdma_tcp_checksum_debug(Structure):
    pass
rdma_tcp_checksum_debug._fields_ = [
    ('reserved30', u32, 2),
    ('fd_addr_req', u32, 6),
    ('lt_mem_data_ofst', u32, 8),
    ('lt_mem_tcp_chksum', u32, 16),
]
class rdma_ip_tcp_header_checksum_debug(Structure):
    pass
rdma_ip_tcp_header_checksum_debug._fields_ = [
    ('lt_mem_ip_chksum', u32, 16),
    ('lt_mem_tcphdr_chksum', u32, 16),
]
class rdma_pseudo_checksum_debug(Structure):
    pass
rdma_pseudo_checksum_debug._fields_ = [
    ('lt_mem_pse_chksum_no_tcplen', u32, 16),
    ('lt_mem_pkt_len', u32, 16),
]
class rdma_mbuf_address_debug(Structure):
    pass
rdma_mbuf_address_debug._fields_ = [
    ('reserved30', u32, 2),
    ('mbuf1_addr', u32, 6),
    ('reserved22', u32, 2),
    ('mbuf0_addr', u32, 6),
    ('reserved14', u32, 2),
    ('pre_mbuf1_addr', u32, 6),
    ('reserved6', u32, 2),
    ('pre_mbuf0_addr', u32, 6),
]
class rdma_misc_ctrl_1(Structure):
    pass
rdma_misc_ctrl_1._fields_ = [
    ('txmbuf_margin', u32, 11),
    ('select_fed_enable', u32, 1),
    ('fifo_high_mark', u32, 8),
    ('fifo_low_mark', u32, 8),
    ('slow_clock_fix_disable', u32, 1),
    ('cq25155_fix_en', u32, 1),
    ('late_col_fix_en', u32, 1),
    ('sdi_shortq_en', u32, 1),
]
class rdma_misc_ctrl_2(Structure):
    pass
rdma_misc_ctrl_2._fields_ = [
    ('fifo_threshold_bd_req', u32, 8),
    ('fifo_threshold_mbuf_req', u32, 8),
    ('reserved14', u32, 2),
    ('mbuf_threshold_mbuf_req', u32, 6),
    ('reserved7', u32, 1),
    ('clock_req_fix_en', u32, 1),
    ('mbuf_threshold_clk_req', u32, 6),
]
class rdma_misc_ctrl_3(Structure):
    pass
rdma_misc_ctrl_3._fields_ = [
    ('reserved6', u32, 26),
    ('cq33951_fix_dis', u32, 1),
    ('cq30888_fix1_en', u32, 1),
    ('cq30888_fix2_en', u32, 1),
    ('cq30808_fix_en', u32, 1),
    ('reserved1', u32, 1),
    ('reserved0', u32, 1),
]
class rdma_regs(Structure):
    pass
rdma_regs._fields_ = [
    ('mode', rdma_mode),
    ('status', rdma_status),
    ('programmable_ipv6_extension_header', rdma_programmable_ipv6_extension_header),
    ('rstates_debug', rdma_rstates_debug),
    ('rstate2_debug', rdma_rstate2_debug),
    ('bd_status_debug', rdma_bd_status_debug),
    ('req_ptr_debug', rdma_req_ptr_debug),
    ('hold_d_dmad_debug', rdma_hold_d_dmad_debug),
    ('length_and_address_index_debug', rdma_length_and_address_index_debug),
    ('mbuf_byte_count_debug', rdma_mbuf_byte_count_debug),
    ('pcie_mbuf_byte_count_debug', rdma_pcie_mbuf_byte_count_debug),
    ('pcie_read_request_address_debug', rdma_pcie_read_request_address_debug),
    ('pcie_dma_request_length_debug', u32),
    ('fifo1_debug', rdma_fifo1_debug),
    ('fifo2_debug', rdma_fifo2_debug),
    ('ofs_3c', u32),
    ('packet_request_debug_1', rdma_packet_request_debug_1),
    ('packet_request_debug_2', rdma_packet_request_debug_2),
    ('packet_request_debug_3', rdma_packet_request_debug_3),
    ('tcp_checksum_debug', rdma_tcp_checksum_debug),
    ('ip_tcp_header_checksum_debug', rdma_ip_tcp_header_checksum_debug),
    ('pseudo_checksum_debug', rdma_pseudo_checksum_debug),
    ('mbuf_address_debug', rdma_mbuf_address_debug),
    ('ofs_5c', u32),
    ('ofs_60', u32),
    ('ofs_64', u32),
    ('ofs_68', u32),
    ('ofs_6c', u32),
    ('ofs_70', u32),
    ('ofs_74', u32),
    ('ofs_78', u32),
    ('ofs_7c', u32),
    ('ofs_80', u32),
    ('ofs_84', u32),
    ('ofs_88', u32),
    ('ofs_8c', u32),
    ('ofs_90', u32),
    ('ofs_94', u32),
    ('ofs_98', u32),
    ('ofs_9c', u32),
    ('ofs_a0', u32),
    ('ofs_a4', u32),
    ('ofs_a8', u32),
    ('ofs_ac', u32),
    ('ofs_b0', u32),
    ('ofs_b4', u32),
    ('ofs_b8', u32),
    ('ofs_bc', u32),
    ('ofs_c0', u32),
    ('ofs_c4', u32),
    ('ofs_c8', u32),
    ('ofs_cc', u32),
    ('ofs_d0', u32),
    ('ofs_d4', u32),
    ('ofs_d8', u32),
    ('ofs_dc', u32),
    ('ofs_e0', u32),
    ('ofs_e4', u32),
    ('ofs_e8', u32),
    ('ofs_ec', u32),
    ('ofs_f0', u32),
    ('ofs_f4', u32),
    ('ofs_f8', u32),
    ('ofs_fc', u32),
]
class receive_list_placement_mode(Structure):
    pass
receive_list_placement_mode._fields_ = [
    ('reserved', u32, 27),
    ('stats_overflow_attention_enable', u32, 1),
    ('mapping_out_of_range_attention_enable', u32, 1),
    ('class_zero_attention_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
class receive_list_placement_status(Structure):
    pass
receive_list_placement_status._fields_ = [
    ('reserved', u32, 27),
    ('stats_overflow_attention', u32, 1),
    ('mapping_out_of_range_attention', u32, 1),
    ('class_zero_attention', u32, 1),
    ('reserved2', u32, 2),
]
class receive_selector_not_empty_bits(Structure):
    pass
receive_selector_not_empty_bits._fields_ = [
    ('reserved', u32, 16),
    ('list_non_empty_bits', u32, 16),
]
class receive_list_placement_configuration(Structure):
    pass
receive_list_placement_configuration._fields_ = [
    ('reserved', u32, 17),
    ('default_interrupt_distribution_queue', u32, 2),
    ('bad_frames_class', u32, 5),
    ('number_of_active_lists', u32, 5),
    ('number_of_lists_per_distribution_group', u32, 3),
]
class receive_list_placement_statistics_control(Structure):
    pass
receive_list_placement_statistics_control._fields_ = [
    ('reserved', u32, 29),
    ('statistics_clear', u32, 1),
    ('reserved2', u32, 1),
    ('statistics_enable', u32, 1),
]
class receive_list_placement_statistics_enable_mask(Structure):
    pass
class N45receive_list_placement_statistics_enable_mask4DOT_73E(Union):
    pass
class N45receive_list_placement_statistics_enable_mask4DOT_734DOT_74E(Structure):
    pass
N45receive_list_placement_statistics_enable_mask4DOT_734DOT_74E._fields_ = [
    ('reserved', u32, 6),
    ('rss_priority', u32, 1),
    ('rc_return_ring_enable', u32, 1),
    ('cpu_mactq_priority_disable', u32, 1),
    ('reserved2', u32, 1),
    ('enable_inerror_stats', u32, 1),
    ('enable_indiscard_stats', u32, 1),
    ('enable_no_more_rbd_stats', u32, 1),
    ('reserved3', u32, 15),
    ('perst_l', u32, 1),
    ('a1_silent_indication', u32, 1),
    ('enable_cos_stats', u32, 1),
]
N45receive_list_placement_statistics_enable_mask4DOT_73E._anonymous_ = ['_0']
N45receive_list_placement_statistics_enable_mask4DOT_73E._fields_ = [
    ('_0', N45receive_list_placement_statistics_enable_mask4DOT_734DOT_74E),
    ('word', u32),
]
receive_list_placement_statistics_enable_mask._anonymous_ = ['_0']
receive_list_placement_statistics_enable_mask._fields_ = [
    ('_0', N45receive_list_placement_statistics_enable_mask4DOT_73E),
]
class receive_list_placement_statistics_increment_mask(Structure):
    pass
receive_list_placement_statistics_increment_mask._fields_ = [
    ('reserved', u32, 10),
    ('counters_increment_mask', u32, 6),
    ('reserved2', u32, 15),
    ('counters_increment_mask_again', u32, 1),
]
class receive_list_local_statistics_counter(Structure):
    pass
receive_list_local_statistics_counter._fields_ = [
    ('reserved', u32, 22),
    ('counters_value', u32, 10),
]
class receive_list_lock(Structure):
    pass
receive_list_lock._fields_ = [
    ('grant', u32, 16),
    ('request', u32, 16),
]
class rlp_regs(Structure):
    pass
class N8rlp_regs4DOT_75E(Structure):
    pass
N8rlp_regs4DOT_75E._fields_ = [
    ('list_head', u32),
    ('list_tail', u32),
    ('list_count', u32),
    ('unknown', u32),
]
rlp_regs._fields_ = [
    ('mode', receive_list_placement_mode),
    ('status', receive_list_placement_status),
    ('lock', receive_list_lock),
    ('selector_not_empty_bits', receive_selector_not_empty_bits),
    ('config', receive_list_placement_configuration),
    ('stats_control', receive_list_placement_statistics_control),
    ('stats_enable_mask', receive_list_placement_statistics_enable_mask),
    ('stats_increment_mask', receive_list_placement_statistics_increment_mask),
    ('unknown', u32 * 56),
    ('rx_selector', N8rlp_regs4DOT_75E * 16),
    ('stat_counter', receive_list_local_statistics_counter * 23),
]
class rss_ind_table_1(Structure):
    pass
rss_ind_table_1._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry0', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry1', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry2', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry3', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry4', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry5', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry6', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry7', u32, 2),
]
class rss_ind_table_2(Structure):
    pass
rss_ind_table_2._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry8', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry9', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry10', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry11', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry12', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry13', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry14', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry15', u32, 2),
]
class rss_ind_table_3(Structure):
    pass
rss_ind_table_3._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry16', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry17', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry18', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry19', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry20', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry21', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry22', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry23', u32, 2),
]
class rss_ind_table_4(Structure):
    pass
rss_ind_table_4._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry24', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry25', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry26', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry27', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry28', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry29', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry30', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry31', u32, 2),
]
class rss_ind_table_5(Structure):
    pass
rss_ind_table_5._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry32', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry33', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry34', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry35', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry36', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry37', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry38', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry39', u32, 2),
]
class rss_ind_table_6(Structure):
    pass
rss_ind_table_6._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry40', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry41', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry42', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry43', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry44', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry45', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry46', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry47', u32, 2),
]
class rss_ind_table_7(Structure):
    pass
rss_ind_table_7._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry48', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry49', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry50', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry51', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry52', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry53', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry54', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry55', u32, 2),
]
class rss_ind_table_8(Structure):
    pass
rss_ind_table_8._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry56', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry57', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry58', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry59', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry60', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry61', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry62', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry63', u32, 2),
]
class rss_ind_table_9(Structure):
    pass
rss_ind_table_9._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry64', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry65', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry66', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry67', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry68', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry69', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry70', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry71', u32, 2),
]
class rss_ind_table_10(Structure):
    pass
rss_ind_table_10._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry72', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry73', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry74', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry75', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry76', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry77', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry78', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry79', u32, 2),
]
class rss_ind_table_11(Structure):
    pass
rss_ind_table_11._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry80', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry81', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry82', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry83', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry84', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry85', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry86', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry87', u32, 2),
]
class rss_ind_table_12(Structure):
    pass
rss_ind_table_12._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry88', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry89', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry90', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry91', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry92', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry93', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry94', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry95', u32, 2),
]
class rss_ind_table_13(Structure):
    pass
rss_ind_table_13._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry96', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry97', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry98', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry99', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry100', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry101', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry102', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry103', u32, 2),
]
class rss_ind_table_14(Structure):
    pass
rss_ind_table_14._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry104', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry105', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry106', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry107', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry108', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry109', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry110', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry111', u32, 2),
]
class rss_ind_table_15(Structure):
    pass
rss_ind_table_15._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry112', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry113', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry114', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry115', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry116', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry117', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry118', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry119', u32, 2),
]
class rss_ind_table_16(Structure):
    pass
rss_ind_table_16._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry120', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry121', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry122', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry123', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry124', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry125', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry126', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry127', u32, 2),
]
class rss_hash_key(Structure):
    pass
rss_hash_key._fields_ = [
    ('byte1', u32, 8),
    ('byte2', u32, 8),
    ('byte3', u32, 8),
    ('byte4', u32, 8),
]
class rmac_programmable_ipv6_extension_header(Structure):
    pass
rmac_programmable_ipv6_extension_header._fields_ = [
    ('hdr_type2_en', u32, 1),
    ('hdr_type1_en', u32, 1),
    ('reserved16', u32, 14),
    ('hdr_type2', u32, 8),
    ('hdr_type1', u32, 8),
]
class rss_regs(Structure):
    pass
rss_regs._fields_ = [
    ('ofs_00', u32),
    ('ofs_04', u32),
    ('ofs_08', u32),
    ('ofs_0c', u32),
    ('ofs_10', u32),
    ('ofs_14', u32),
    ('ofs_18', u32),
    ('ofs_1c', u32),
    ('ofs_20', u32),
    ('ofs_24', u32),
    ('ofs_28', u32),
    ('ofs_2c', u32),
    ('ind_table_1', rss_ind_table_1),
    ('ind_table_2', rss_ind_table_2),
    ('ind_table_3', rss_ind_table_3),
    ('ind_table_4', rss_ind_table_4),
    ('ind_table_5', rss_ind_table_5),
    ('ind_table_6', rss_ind_table_6),
    ('ind_table_7', rss_ind_table_7),
    ('ind_table_8', rss_ind_table_8),
    ('ind_table_9', rss_ind_table_9),
    ('ind_table_10', rss_ind_table_10),
    ('ind_table_11', rss_ind_table_11),
    ('ind_table_12', rss_ind_table_12),
    ('ind_table_13', rss_ind_table_13),
    ('ind_table_14', rss_ind_table_14),
    ('ind_table_15', rss_ind_table_15),
    ('ind_table_16', rss_ind_table_16),
    ('hash_key_0', rss_hash_key),
    ('hash_key_1', rss_hash_key),
    ('hash_key_2', rss_hash_key),
    ('hash_key_3', rss_hash_key),
    ('hash_key_4', rss_hash_key),
    ('hash_key_5', rss_hash_key),
    ('hash_key_6', rss_hash_key),
    ('hash_key_7', rss_hash_key),
    ('hash_key_8', rss_hash_key),
    ('hash_key_9', rss_hash_key),
    ('ofs_98', u32),
    ('ofs_9c', u32),
    ('rmac_ipv6_ext_hdr', rmac_programmable_ipv6_extension_header),
]
class rtsdi_mode(Structure):
    pass
rtsdi_mode._fields_ = [
    ('reserved', u32, 26),
    ('multiple_segment_enable', u32, 1),
    ('pre_dma_debug', u32, 1),
    ('hardware_pre_dma_enable', u32, 1),
    ('stats_overflow_attention_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
class rtsdi_status(Structure):
    pass
rtsdi_status._fields_ = [
    ('reserved', u32, 29),
    ('stats_overflow_attention', u32, 1),
    ('reserved2', u32, 2),
]
class rtsdi_statistics_control(Structure):
    pass
rtsdi_statistics_control._fields_ = [
    ('reserved', u32, 27),
    ('zap_statistics', u32, 1),
    ('flush_statistics', u32, 1),
    ('statistics_clear', u32, 1),
    ('faster_update', u32, 1),
    ('statistics_enable', u32, 1),
]
class rtsdi_statistics_mask(Structure):
    pass
rtsdi_statistics_mask._fields_ = [
    ('reserved', u32, 31),
    ('counters_enable_mask', u32, 1),
]
class rtsdi_statistics_increment_mask(Structure):
    pass
rtsdi_statistics_increment_mask._fields_ = [
    ('reserved', u32, 8),
    ('counters_increment_mask_1', u32, 5),
    ('reserved2', u32, 3),
    ('counters_increment_mask_2', u32, 16),
]
class rtsdi_regs(Structure):
    pass
rtsdi_regs._fields_ = [
    ('mode', rtsdi_mode),
    ('status', rtsdi_status),
    ('statistics_control', rtsdi_statistics_control),
    ('statistics_mask', rtsdi_statistics_mask),
    ('statistics_increment_mask', rtsdi_statistics_increment_mask),
    ('ofs_14', u32),
    ('ofs_18', u32),
    ('ofs_1c', u32),
    ('av_fetch_delay', u32),
    ('av_fetch_cx_comp', u32),
    ('av_fetch_l1_comp', u32),
]
class sbdc_mode(Structure):
    pass
sbdc_mode._fields_ = [
    ('reserved', u32, 29),
    ('attention_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
class sbdc_debug(Structure):
    pass
sbdc_debug._fields_ = [
    ('reserved', u32, 29),
    ('rstate', u32, 3),
]
class sbdc_regs(Structure):
    pass
sbdc_regs._fields_ = [
    ('mode', sbdc_mode),
    ('debug', sbdc_debug),
]
class sbdi_mode(Structure):
    pass
sbdi_mode._fields_ = [
    ('reserved', u32, 26),
    ('multi_txq_en', u32, 1),
    ('pass_bit', u32, 1),
    ('rupd_enable', u32, 1),
    ('attention_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
class sbdi_status(Structure):
    pass
sbdi_status._fields_ = [
    ('reserved', u32, 29),
    ('error', u32, 1),
    ('reserved2', u32, 2),
]
class sbdi_regs(Structure):
    pass
sbdi_regs._fields_ = [
    ('mode', sbdi_mode),
    ('status', sbdi_status),
    ('prod_idx', u32 * 16),
]
class sbds_mode(Structure):
    pass
sbds_mode._fields_ = [
    ('reserved', u32, 29),
    ('attention_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
class sbds_status(Structure):
    pass
sbds_status._fields_ = [
    ('reserved', u32, 29),
    ('error', u32, 1),
    ('reserved2', u32, 2),
]
class sbds_local_nic_send_bd_consumer_idx(Structure):
    pass
sbds_local_nic_send_bd_consumer_idx._fields_ = [
    ('reserved', u32, 23),
    ('index', u32, 9),
]
class sbds_regs(Structure):
    pass
sbds_regs._fields_ = [
    ('mode', sbds_mode),
    ('status', sbds_status),
    ('hardware_diagnostics', u32),
    ('local_nic_send_bd_consumer_idx', sbds_local_nic_send_bd_consumer_idx),
    ('unknown', u32 * 12),
    ('con_idx', u32 * 16),
]
class sdc_mode(Structure):
    pass
sdc_mode._fields_ = [
    ('reserved', u32, 27),
    ('cdelay', u32, 1),
    ('reserved2', u32, 2),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
class sdc_pre_dma_command_exchange(Structure):
    pass
sdc_pre_dma_command_exchange._fields_ = [
    ('pass', u32, 1),
    ('skip', u32, 1),
    ('end_of_frag', u32, 1),
    ('reserved', u32, 13),
    ('head_txmbuf_ptr', u32, 8),
    ('tail_txmbuf_ptr', u32, 8),
]
class sdc_regs(Structure):
    pass
sdc_regs._fields_ = [
    ('mode', sdc_mode),
    ('unknown', u32),
    ('pre_dma_command_exchange', sdc_pre_dma_command_exchange),
]
class sdi_mode(Structure):
    pass
sdi_mode._fields_ = [
    ('reserved', u32, 26),
    ('multiple_segment_enable', u32, 1),
    ('pre_dma_debug', u32, 1),
    ('hardware_pre_dma_enable', u32, 1),
    ('stats_overflow_attention_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
class sdi_status(Structure):
    pass
sdi_status._fields_ = [
    ('reserved', u32, 29),
    ('stats_overflow_attention', u32, 1),
    ('reserved2', u32, 2),
]
class sdi_statistics_control(Structure):
    pass
sdi_statistics_control._fields_ = [
    ('reserved', u32, 27),
    ('zap_statistics', u32, 1),
    ('flush_statistics', u32, 1),
    ('statistics_clear', u32, 1),
    ('faster_update', u32, 1),
    ('statistics_enable', u32, 1),
]
class sdi_statistics_mask(Structure):
    pass
sdi_statistics_mask._fields_ = [
    ('reserved', u32, 31),
    ('counters_enable_mask', u32, 1),
]
class sdi_statistics_increment_mask(Structure):
    pass
sdi_statistics_increment_mask._fields_ = [
    ('reserved', u32, 8),
    ('counters_increment_mask_1', u32, 5),
    ('reserved2', u32, 3),
    ('counters_increment_mask_2', u32, 16),
]
class sdi_regs(Structure):
    pass
sdi_regs._fields_ = [
    ('mode', sdi_mode),
    ('status', sdi_status),
    ('statistics_control', sdi_statistics_control),
    ('statistics_mask', sdi_statistics_mask),
    ('statistics_increment_mask', sdi_statistics_increment_mask),
    ('unknown', u32 * 27),
    ('local_statistics', u32 * 18),
]
class mac_stats_regs(Structure):
    pass
mac_stats_regs._fields_ = [
    ('ifHCOutOctets', u32),
    ('ofs_04', u32),
    ('etherStatsCollisions', u32),
    ('outXonSent', u32),
    ('outXoffSent', u32),
    ('ofs_14', u32),
    ('dot3StatsInternalMacTransmitErrors', u32),
    ('dot3StatsSingleCollisionFrames', u32),
    ('dot3StatsMultipleCollisionFrames', u32),
    ('dot3StatsDeferredTransmissions', u32),
    ('ofs_28', u32),
    ('dot3StatsExcessiveTransmissions', u32),
    ('dot3StatsLateCollisions', u32),
    ('ofs_34', u32),
    ('ofs_38', u32),
    ('ofs_3c', u32),
    ('ofs_40', u32),
    ('ofs_44', u32),
    ('ofs_48', u32),
    ('ofs_4c', u32),
    ('ofs_50', u32),
    ('ofs_54', u32),
    ('ofs_58', u32),
    ('ofs_5c', u32),
    ('ofs_60', u32),
    ('ofs_64', u32),
    ('ofs_68', u32),
    ('iHCOutUcastPkts', u32),
    ('iHCOutMulticastPkts', u32),
    ('iHCOutBroadcastPkts', u32),
    ('ofs_78', u32),
    ('ofs_7c', u32),
    ('iHCOOutOctets', u32),
    ('ofs_84', u32),
    ('etherStatsFragments', u32),
    ('ifHCInUcastPkts', u32),
    ('ifHCInMulticastPkts', u32),
    ('ifHCInBroadcastPkts', u32),
    ('dot3StatsFCSErrors', u32),
    ('dot3StatsAlignmentErrors', u32),
    ('xonPauseFrameReceived', u32),
    ('xoffPauseFrameReceived', u32),
    ('macControlFramesReceived', u32),
    ('xoffStateEntered', u32),
    ('dot3StatsFramesTooLongs', u32),
    ('etherStatsJabbers', u32),
    ('etherStatsUndersizePkts', u32),
    ('ofs_bc', u32),
]
class status_block(Structure):
    pass
class N12status_block4DOT_76E(Structure):
    pass
N12status_block4DOT_76E._fields_ = [
    ('updated', u32, 1),
    ('link_status', u32, 1),
    ('attention', u32, 1),
    ('reserved1', u32, 29),
]
class N12status_block4DOT_77E(Structure):
    pass
N12status_block4DOT_77E._fields_ = [
    ('status_tag', u32, 8),
    ('reserved2', u32, 24),
]
class N12status_block4DOT_78E(Structure):
    pass
N12status_block4DOT_78E._fields_ = [
    ('rr1_pi', u32, 16),
    ('rpci', u32, 16),
]
class N12status_block4DOT_79E(Structure):
    pass
N12status_block4DOT_79E._fields_ = [
    ('rr3_pi', u32, 16),
    ('rr2_pi', u32, 16),
]
class N12status_block4DOT_80E(Structure):
    pass
N12status_block4DOT_80E._fields_ = [
    ('rr0_pi', u32, 16),
    ('sbdci', u32, 16),
]
class N12status_block4DOT_81E(Structure):
    pass
N12status_block4DOT_81E._fields_ = [
    ('rjpci', u32, 16),
    ('reserved6', u32, 16),
]
status_block._anonymous_ = ['_5', '_0', '_1', '_2', '_3', '_4']
status_block._fields_ = [
    ('_0', N12status_block4DOT_76E),
    ('_1', N12status_block4DOT_77E),
    ('_2', N12status_block4DOT_78E),
    ('_3', N12status_block4DOT_79E),
    ('_4', N12status_block4DOT_80E),
    ('_5', N12status_block4DOT_81E),
]
class tsc_length_offset(Structure):
    pass
tsc_length_offset._fields_ = [
    ('reserved23', u32, 9),
    ('mbuf_offset', u32, 7),
    ('length', u32, 16),
]
class tsc_dma_flags(Structure):
    pass
tsc_dma_flags._fields_ = [
    ('reserved20', u32, 12),
    ('mbuf_offset_valid', u32, 1),
    ('last_fragment', u32, 1),
    ('no_word_swap', u32, 1),
    ('status_dma', u32, 1),
    ('mac_source_addr_sel', u32, 2),
    ('mac_source_addr_ins', u32, 1),
    ('tcp_udp_cksum_en', u32, 1),
    ('ip_cksum_en', u32, 1),
    ('force_raw_cksum_en', u32, 1),
    ('data_only', u32, 1),
    ('header', u32, 1),
    ('vlan_tag_present', u32, 1),
    ('force_interrupt', u32, 1),
    ('last_bd_in_frame', u32, 1),
    ('coalesce_now', u32, 1),
    ('mbuf', u32, 1),
    ('invoke_processor', u32, 1),
    ('dont_generate_crc', u32, 1),
    ('no_byte_swap', u32, 1),
]
class tsc_vlan_tag(Structure):
    pass
tsc_vlan_tag._fields_ = [
    ('reserved16', u32, 16),
    ('vlan_tag', u32, 16),
]
class tsc_pre_dma_cmd_xchng(Structure):
    pass
tsc_pre_dma_cmd_xchng._fields_ = [
    ('ready', u32, 1),
    ('pass_bit', u32, 1),
    ('skip', u32, 1),
    ('unsupported_mss', u32, 1),
    ('reserved7', u32, 21),
    ('bd_index', u32, 7),
]
class tcp_seg_ctrl_regs(Structure):
    pass
tcp_seg_ctrl_regs._fields_ = [
    ('lower_host_addr', u32),
    ('upper_host_addr', u32),
    ('length_offset', tsc_length_offset),
    ('dma_flags', tsc_dma_flags),
    ('vlan_tag', tsc_vlan_tag),
    ('pre_dma_cmd_xchng', tsc_pre_dma_cmd_xchng),
]
class wdma_mode(Structure):
    pass
wdma_mode._fields_ = [
    ('reserved', u32, 2),
    ('status_tag_fix_enable', u32, 1),
    ('reserved2', u32, 10),
    ('swap_test_en', u32, 1),
    ('hc_byte_swap', u32, 1),
    ('hc_word_swap', u32, 1),
    ('bd_byte_swap', u32, 1),
    ('bd_word_swap', u32, 1),
    ('data_byte_swap', u32, 1),
    ('data_word_swap', u32, 1),
    ('software_byte_swap_control', u32, 1),
    ('receive_accelerate_mode', u32, 1),
    ('write_dma_local_memory', u32, 1),
    ('write_dma_pci_fifo_overwrite_attention_enable', u32, 1),
    ('write_dma_pci_fifo_underrun_attention_enable', u32, 1),
    ('write_dma_pci_fifo_overrun_attention_enable', u32, 1),
    ('write_dma_pci_host_address_overflow_error_attention_enable', u32, 1),
    ('write_dma_pci_parity_error_attention_enable', u32, 1),
    ('write_dma_pci_master_abort_attention_enable', u32, 1),
    ('write_dma_pci_target_abort_attention_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]
class wdma_status(Structure):
    pass
wdma_status._fields_ = [
    ('reserved', u32, 22),
    ('write_dma_local_memory_read_longer_than_dma_length_error', u32, 1),
    ('write_dma_pci_fifo_overwrite_error', u32, 1),
    ('write_dma_pci_fifo_underrun_error', u32, 1),
    ('write_dma_pci_fifo_overrun_error', u32, 1),
    ('write_dma_pci_host_address_overflow_error', u32, 1),
    ('reserved1', u32, 5),
]
class wdma_regs(Structure):
    pass
wdma_regs._fields_ = [
    ('mode', wdma_mode),
    ('status', wdma_status),
]
RBD_RULE_HDR_FRAME = 0 # Variable c_int '0'
UNKNOWN_CMD = 65535 # Variable c_int '65535'
HIDE_FUNC_ACK = 32775 # Variable c_int '32775'
CAP_VPD = 4 # Variable c_int '4'
CAP_CTRL_ACK = 32774 # Variable c_int '32774'
RBD_RULE_OP_LESS = 3 # Variable c_int '3'
SEND_MSI_ACK = 32773 # Variable c_int '32773'
READ_DMA_REPLY = 32772 # Variable c_int '32772'
WRITE_NVRAM_ACK = 32778 # Variable c_int '32778'
READ_DMA_CMD = 4 # Variable c_int '4'
PME_ASSERT_ACK = 32776 # Variable c_int '32776'
CAP_MSIX = 1 # Variable c_int '1'
READ_LOCAL_REPLY = 32770 # Variable c_int '32770'
READ_LOCAL_CMD = 2 # Variable c_int '2'
CAP_MSI = 2 # Variable c_int '2'
ERR_REPLY = 36864 # Variable c_int '36864'
TG3_IMAGE_TYPE_ASF_INIT = 1 # Variable c_int '1'
PME_ASSERT_CMD = 8 # Variable c_int '8'
RBD_RULE_HDR_UDP = 3 # Variable c_int '3'
TG3_IMAGE_EXE_A_MASK = 8388608 # Variable c_int '8388608'
PING_REPLY = 32769 # Variable c_int '32769'
WRITE_LOCAL_ACK = 32771 # Variable c_int '32771'
WRITE_LOCAL_CMD = 3 # Variable c_int '3'
CLOAK_DIS_ACK = 32781 # Variable c_int '32781'
PING_CMD = 1 # Variable c_int '1'
CAP_CTRL_CMD = 6 # Variable c_int '6'
RBD_RULE_OP_GREATER = 2 # Variable c_int '2'
RBD_RULE_HDR_IP = 1 # Variable c_int '1'
TG3_MAGIC = 1721324970 # Variable c_int '1721324970'
CMD_REPLY = 32768 # Variable c_int '32768'
HIDE_FUNC_CMD = 7 # Variable c_int '7'
READ_NVRAM_CMD = 9 # Variable c_int '9'
RBD_RULE_OP_NOTEQUAL = 1 # Variable c_int '1'
CLOAK_EN_ACK = 32780 # Variable c_int '32780'
RBD_RULE_OP_EQUAL = 0 # Variable c_int '0'
CAP_POWER_MANAGEMENT = 8 # Variable c_int '8'
TX_STD_ENQ_ACK = 32782 # Variable c_int '32782'
TX_STD_ENQ_CMD = 14 # Variable c_int '14'
TG3_IMAGE_TYPE_PXE = 0 # Variable c_int '0'
RBD_RULE_HDR_TCP = 2 # Variable c_int '2'
TX_STD_ENQ_ERR = 36878 # Variable c_int '36878'
CRC32_POLYNOMIAL = 3988292384L # Variable c_uint '3988292384u'
TG3_FEAT_ASF = 128 # Variable c_int '128'
RBD_RULE_HDR_DATA = 4 # Variable c_int '4'
TG3_IMAGE_EXE_B_MASK = 4194304 # Variable c_int '4194304'
WRITE_NVRAM_CMD = 10 # Variable c_int '10'
CLOAK_EN_CMD = 12 # Variable c_int '12'
SEND_MSI_CMD = 5 # Variable c_int '5'
PCIE_RETRY_BUFFER_DUMP_ACK = 32779 # Variable c_int '32779'
MA_ALL_TRAPS = 1121660 # Variable c_int '1121660'
PCIE_RETRY_BUFFER_DUMP_CMD = 11 # Variable c_int '11'
CLOAK_DIS_CMD = 13 # Variable c_int '13'
TG3_FEAT_PXE = 2 # Variable c_int '2'
READ_NVRAM_ACK = 32777 # Variable c_int '32777'
int8_t = c_int8
int16_t = c_int16
int32_t = c_int32
int64_t = c_int64
int_least8_t = c_byte
int_least16_t = c_short
int_least32_t = c_int
int_least64_t = c_long
uint_least8_t = c_ubyte
uint_least16_t = c_ushort
uint_least32_t = c_uint
uint_least64_t = c_ulong
int_fast8_t = c_byte
int_fast16_t = c_long
int_fast32_t = c_long
int_fast64_t = c_long
uint_fast8_t = c_ubyte
uint_fast16_t = c_ulong
uint_fast32_t = c_ulong
uint_fast64_t = c_ulong
intptr_t = c_long
uintptr_t = c_ulong
intmax_t = c_long
uintmax_t = c_ulong
__all__ = ['nrdma_mbuf_addr_debug', 'pcie_dl_ack_timeout',
           'N20grc_cpu_event_enable4DOT_474DOT_48E',
           'receive_list_lock', 'nvram_command',
           'TG3_IMAGE_EXE_A_MASK', 'receive_selector_not_empty_bits',
           'N13emac_mac_addr4DOT_32E', 'acpi_sdt_hdr', 'otp_status',
           'uint8_t', 'dmar_rmrr', 'rss_hash_key',
           'mb_rbd_rr0_consumer',
           'rmac_programmable_ipv6_extension_header',
           'sdc_pre_dma_command_exchange', 'RBD_RULE_OP_GREATER',
           'N12nvram_header4DOT_54E', 'sdc_mode', 'rss_regs',
           'cpmu_cr_idle_det_debounce_ctrl', 'TG3_FEAT_PXE',
           'nvram_arbitration_watchdog', 'sbd_flags',
           'transmit_mac_lengths', 'dmar_atsr', 'dmar_dev_scope',
           'nrdma_programmable_ipv6_extension_header', 'sbdi_regs',
           'N14ftq_write_peek4DOT_43E', 'int_fast32_t',
           'RBD_RULE_HDR_DATA', 'uint_least8_t', 'rss_ind_table_13',
           'cfg_port_regs', 'wdma_mode', 'pcie_tl_msi_len_req_diag',
           'rss_ind_table_15', 'N11pci_command4DOT_59E',
           'TG3_IMAGE_TYPE_PXE', 'WRITE_NVRAM_ACK',
           'grc_seeprom_ctrl', 'nrdma_rstate2_debug',
           'bdrdma_pcie_dma_rd_req_addr_dbg',
           'asf_time_stamp_counter', 'TG3_IMAGE_LEN',
           'emac_low_watermark_max_receive_frame', 'nrdma_status',
           'N8pci_regs4DOT_63E',
           'bufman_risc_mbuf_cluster_allocation_response',
           'N12status_block4DOT_79E', 'u32', 'bufman_regs',
           'receive_list_local_statistics_counter',
           'RBD_RULE_HDR_TCP', 'bufman_mbuf_high_watermark',
           'receive_list_placement_statistics_control',
           'cpmu_clock_status', 'emac_regs', 'hc_regs',
           'N13emac_mac_addr4DOT_324DOT_33E', 'nrdma_req_ptr_debug',
           'CAP_POWER_MANAGEMENT', 'grc_exp_rom_addr',
           'rdma_mbuf_byte_count_debug', 'TG3_IMAGE_EXE_B_MASK',
           'hpmb_regs', 'uint_fast8_t', 'transmit_mac_mode',
           'N13rcb_registers4DOT_72E', 'rdc_regs',
           'N16emac_led_control4DOT_244DOT_25E',
           'grc_pcie_misc_status', 'bufman_rdma_mbuf_low_watermark',
           'N14cpu_breakpoint4DOT_174DOT_18E', 'pcie_pl_lo_regs',
           'N9rbdi_mode4DOT_684DOT_69E', 'ma_status',
           'rdma_req_ptr_debug', 'pcie_dl_ctrl', 'wdma_regs',
           'N12status_block4DOT_81E', 'status_block',
           'pcie_tl_xmt_state_machines_gated_reqs_diag',
           'uint_least32_t', 'int_least64_t', 'sbds_mode',
           'nrdma_pcie_dma_req_length_debug', 'pcie_tl_tlp_ctrl',
           'N10vlan_frame4DOT_37E', 'N9dmac_mode4DOT_214DOT_22E',
           'sbdc_regs', 'READ_NVRAM_CMD',
           'N11pci_command4DOT_594DOT_60E',
           'mb_rbd_standard_producer', 'tsc_length_offset',
           'N9rbdi_mode4DOT_68E', 'TX_STD_ENQ_ACK',
           'pcie_tl_flow_control_inputs_diag', 'rss_ind_table_11',
           'rss_ind_table_10', 'cpmu_clock', 'rss_ind_table_12',
           'N8dma_desc4DOT_23E', 'rss_ind_table_14', 'TG3_FEAT_ASF',
           'rss_ind_table_16', 'sbdi_status', 'N8rlp_regs4DOT_75E',
           'sbds_regs', 'wdma_status', 'rdma_hold_d_dmad_debug',
           'asf_heartbeat_timer',
           'N20emac_rx_rule_control4DOT_344DOT_35E', 'asf_poll_timer',
           'tsc_pre_dma_cmd_xchng', 'u64', 'nrdma_bd_status_debug',
           'CAP_MSIX', 'READ_LOCAL_CMD', 'otp_control',
           'receive_list_placement_status', 'rtsdi_statistics_mask',
           'rdma_tcp_checksum_debug', 'nrdma_reserved_control',
           'rdma_mode', 'rdma_packet_request_debug_3',
           'cpmu_gphy_control_status', 'rdma_packet_request_debug_1',
           'bufman_hardware_diagnostic_3',
           'bufman_hardware_diagnostic_2',
           'bufman_hardware_diagnostic_1',
           'receive_mac_rules_configuration', 'sbds_status',
           'bdrdma_pcie_dma_req_len_dbg', 'pcie_dl_attn',
           'bdrdma_rstate2_dbg', 'pcie_dl_test', 'vlan_frame',
           'N12nvram_header4DOT_55E', 'rbd_value_mask', 'rbd_flags',
           'ofs_7c', 'cpmu_override', 'pci_pm_cap', 'dma_desc',
           'emac_status', 'N12status_block4DOT_77E', 'pcie_pl_regs',
           'rdi_mode', 'gencomm', 'grc_misc_control', 'HIDE_FUNC_ACK',
           'rdma_mbuf_address_debug', 'N12status_block4DOT_78E',
           'rtsdi_statistics_increment_mask', 'N9ftq_reset4DOT_39E',
           'nrdma_corruption_enable_control', 'emac_event_enable',
           'cr_port_regs', 'rbd_ex', 'bufman_status',
           'rdma_packet_request_debug_2', 'pci_pm_ctrl_status',
           'lpmb_regs', 'SEND_MSI_ACK', 'RBD_RULE_OP_NOTEQUAL',
           'rdma_fifo2_debug', 'nrdma_fifo1_debug', 'TG3_IMAGE_TYPE',
           'PCIE_RETRY_BUFFER_DUMP_CMD', 'uint_fast16_t',
           'uint_fast32_t', 'CAP_CTRL_CMD', 'bufman_mbuf_pool_bar',
           'cpu_mode', 'pci_state', 'nrdma_fifo2_debug',
           'sdi_statistics_control',
           'N13grc_cpu_event4DOT_454DOT_46E', 'dmac_mode',
           'N14dmar_dev_scope3DOT_0E', 'READ_NVRAM_ACK', 'sbd',
           'otp_regs', 'PME_ASSERT_CMD', 'nvram_status',
           'bdrdma_mode', 'N13pcie_alt_regs4DOT_56E',
           'receive_list_placement_statistics_enable_mask',
           'grc_seeprom_addr', 'N10pci_status4DOT_574DOT_58E', 'xsdt',
           'N19ftq_enqueue_dequeue4DOT_41E',
           'receive_list_placement_mode', 'otp_addr', 'hc_mode',
           'CLOAK_DIS_CMD', 'nrdma_mode',
           'rdma_length_and_address_index_debug', 'UNKNOWN_CMD',
           'RBD_RULE_HDR_FRAME', 'CAP_CTRL_ACK', 'bdrdma_fifo1_dbg',
           'N18receive_mac_status4DOT_28E', 'sdi_regs', 'dmar_rhsa',
           'sbdc_mode', 'cpu_breakpoint',
           'N28grc_fastboot_program_counter4DOT_49E',
           'rdma_rstates_debug', 'mb_rbd_rr2_consumer',
           'WRITE_LOCAL_CMD', 'nrdma_flow_reserved_control',
           'nrdma_pcie_debug_status', 'rdma_regs',
           'grc_fastboot_program_counter', 'N11bufman_mode3DOT_7E',
           'rdma_ip_tcp_header_checksum_debug',
           'cpmu_pcie_idle_det_debounce_ctrl', 'cfg_port_pci_class',
           'SEND_MSI_CMD', 'PCIE_RETRY_BUFFER_DUMP_ACK', 'int16_t',
           'uint64_t', 'asf_retransmission_timer', 'TX_STD_ENQ_ERR',
           'rss_ind_table_9', 'rss_ind_table_8', 'rss_ind_table_5',
           'rss_ind_table_4', 'rss_ind_table_7', 'rss_ind_table_6',
           'bufman_dma_mbuf_low_watermark',
           'N20grc_cpu_event_enable4DOT_47E', 'rss_ind_table_3',
           'rss_ind_table_2', 'bdrdma_req_ptr_dbg', 'sbdi_mode',
           'N9rbd_flags3DOT_3E', 'tsc_vlan_tag', 'cfg_port_pci_sid',
           'nvram_software_arbitration', 'pci_command',
           'RBD_RULE_HDR_UDP', 'cpu_last_branch_address',
           'N10cpu_status4DOT_15E', 'bufman_mbuf_pool_length',
           'bdrdma_addr_idx_dbg', 'dmac_regs', 'bufman_mode',
           'rbdi_mode', 'receive_mac_status', 'grc_cpu_event',
           'emac_mii_communication',
           'N19transmit_mac_status4DOT_264DOT_27E',
           'rdma_pcie_mbuf_byte_count_debug', 'pci_misc_host_ctrl',
           'pci_device_id', 'N9dmac_mode4DOT_21E',
           'N15rbd_error_flags3DOT_5E', 'N12status_block4DOT_80E',
           'RBD_RULE_OP_EQUAL', 'rtsdi_mode', 'emac_mii_status',
           'cpmu_padring_control', 'asf_smbus_output',
           'sdi_statistics_mask', 'N19transmit_mac_status4DOT_26E',
           'grc_misc_local_control', 'READ_DMA_CMD',
           'N10pci_status4DOT_57E', 'N8pci_regs4DOT_64E',
           'rdma_pcie_read_request_address_debug', 'hc_status',
           'N10vlan_frame4DOT_374DOT_38E',
           'N13emac_mac_addr4DOT_304DOT_31E',
           'N15cfg_port_pci_id3DOT_9E', 'ma_regs', 'ftq_queue_regs',
           'pcie_dl_status', 'cpmu_pcie_status', 'grc_mode',
           'uintptr_t', 'rdi_regs', 'PING_CMD', 'intptr_t',
           'mb_rbd_rr3_consumer', 'int_fast8_t', 'otp_soft_reset',
           'RBD_RULE_OP_LESS', 'rbdi_regs', 'mb_sbd_host_producer',
           'ERR_REPLY', 'nrdma_regs', 'cpmu_energy_det_debounce_ctrl',
           'WRITE_NVRAM_CMD',
           'rdma_programmable_ipv6_extension_header',
           'grc_misc_config', 'grc_power_management_debug',
           'pcie_dl_pm_threshold', 'pcie_dl_replay',
           'pcie_tl_wdma_len_byte_en_req_diag', 'pcie_dl_lo_regs',
           'frame', 'nvram_write1', 'mb_interrupt',
           'N13emac_mac_addr4DOT_30E',
           'N15cfg_port_pci_id3DOT_94DOT_10E',
           'pcie_tl_transaction_config', 'cpmu_status',
           'pci_msi_cap_hdr', 'cpmu_core_idle_det_debounce_ctrl',
           'rdma_rstate2_debug', 'dmar_drhd', 'cpmu_mutex',
           'rtsdi_status', 'dmar_andd', 'cpmu_chip_id',
           'N18cfg_port_pci_class4DOT_13E', 'mailbox',
           'N9sbd_flags3DOT_13DOT_2E', 'N13grc_cpu_event4DOT_45E',
           'rbd_rule', 'bdrdma_regs', 'CLOAK_EN_ACK',
           'cfg_port_bar_ctrl', 'asf_smbus_input', 'nvram_regs',
           'rtsdi_regs', 'otp_mode',
           'sbds_local_nic_send_bd_consumer_idx', 'nrdma_tce_debug1',
           'CMD_REPLY', 'nrdma_tce_debug3', 'nrdma_tce_debug2',
           'uint16_t', 'grc_bond_id', 'ftq_write_peek',
           'ftq_enqueue_dequeue', 'int32_t',
           'N10cpu_status4DOT_154DOT_16E', 'asf_regs',
           'pci_class_code_rev_id',
           'N18receive_mac_status4DOT_284DOT_29E', 'uint_least16_t',
           'rbdc_mode', 'pcie_dl_seq_no', 'emac_rx_rule_control',
           'rcb_flags', 'rbdi_status',
           'N14ftq_write_peek4DOT_434DOT_44E',
           'bufman_risc_mbuf_cluster_allocation_request', 'u16',
           'msi_regs',
           'receive_list_placement_statistics_increment_mask',
           'N8pci_regs4DOT_66E', 'N9ftq_reset4DOT_394DOT_40E',
           'rss_ind_table_1', 'sdi_mode', 'rdc_mode', 'emac_mode',
           'cpu_event_mask', 'pcie_dl_regs', 'rdma_status',
           'cfg_port_cap_ctrl', 'bdrdma_bd_status_dbg',
           'mbuf_frame_desc', 'transmit_mac_status', 'grc_secfg_2',
           'grc_secfg_1', 'ftq_regs', 'rbd', 'uintmax_t',
           'N45receive_list_placement_statistics_enable_mask4DOT_73E',
           'nrdma_length_and_address_debug', 'N9rbdc_mode4DOT_67E',
           'int_fast16_t', 'N8rdc_mode4DOT_704DOT_71E',
           'grc_mdi_ctrl', 'N9rbd_flags3DOT_33DOT_4E', 'sdi_status',
           'pcie_dl_retry_buffer_ptr', 'cpmu_dll_lock_timer',
           'rtsdi_statistics_control', 'N4mbuf4DOT_53E',
           'pcie_tl_slave_req_len_type_diag', 'receive_mac_mode',
           'cpmu_ram_control', 'emac_mii_mode', 'rbdc_regs',
           'N8pci_regs4DOT_61E', 'nrdma_pcie_dma_read_req_debug',
           'asf_watchdog_timer', 'N9emac_regs4DOT_36E',
           'uint_fast64_t', 'rdma_misc_ctrl_3', 'uint32_t',
           'nrdma_rstates_debug', 'emac_regulator_voltage_control',
           'pci_status', 'mb_sbd_nic_producer',
           'N20emac_rx_rule_control4DOT_34E', 'rcb_registers',
           'N9sbd_flags3DOT_1E', 'pcie_dl_attn_mask', 'rbdc_status',
           'READ_LOCAL_REPLY', 'ma_mode', 'nvram_header',
           'N7ma_mode4DOT_51E', 'nrdma_mbuf_byte_count_debug',
           'rbdc_rbd_pi', 'bdrdma_len_dbg', 'emac_autopolling_status',
           'int_least32_t', 'PING_REPLY', 'pcie_tl_rdma_len_req_diag',
           'N16emac_led_control4DOT_24E', 'rdma_fifo1_debug',
           'nvram_dir_item', 'bdrdma_status', 'pcie_tl_tlp_bdf',
           'nrdma_hold_d_dmad_debug', 'cpu_regs',
           'N45receive_list_placement_statistics_enable_mask4DOT_734DOT_74E',
           'bdrdma_rstates_dbg',
           'N19ftq_enqueue_dequeue4DOT_414DOT_42E', 'cpmu_regs',
           'msi_mode', 'hc_flow_attention',
           'N14cpu_breakpoint4DOT_17E',
           'N16cfg_port_pci_sid4DOT_114DOT_12E', 'intmax_t',
           'bdrdma_rsvrd_ctrl', 'PME_ASSERT_ACK', 'READ_DMA_REPLY',
           'tsc_dma_flags', 'CAP_MSI',
           'N28grc_fastboot_program_counter4DOT_494DOT_50E',
           'mbuf_hdr', 'int_least8_t',
           'bufman_receive_flow_threshold', 'WRITE_LOCAL_ACK',
           'N15rbd_error_flags3DOT_53DOT_6E',
           'bdrdma_pcie_dbg_status', 'int_least16_t', 'ftq_reset',
           'asf_poll_legacy_timer', 'CAP_VPD', 'msi_status',
           'grc_cpu_event_enable', 'pci_regs',
           'N18cfg_port_pci_class4DOT_134DOT_14E',
           'N8pci_regs4DOT_65E', 'bdrdma_len_and_addr_idx_dbg',
           'pcie_alt_regs', 'N8pci_regs4DOT_62E',
           'mb_rbd_rr1_consumer', 'cpu_status', 'uint_least64_t',
           'bdrdma_hold_d_dmad_dbg', 'N11bufman_mode3DOT_73DOT_8E',
           'pcie_tl_regs', 'nrdma_post_proc_pkt_req_cnt',
           'N8rdc_mode4DOT_70E', 'TG3_IMAGE_TYPE_ASF_INIT',
           'bdrdma_fifo2_dbg', 'sdi_statistics_increment_mask', 'u8',
           'cfg_port_pci_id', 'rdma_bd_status_debug', 'rcb',
           'HIDE_FUNC_CMD', 'rdma_pseudo_checksum_debug',
           'receive_list_placement_configuration', 'mac_stats_regs',
           'nvram_auto_sense_status', 'int8_t', 'CLOAK_EN_CMD',
           'dmar_tbl_hdr', 'grc_cpu_semaphore', 'CRC32_POLYNOMIAL',
           'pcie_dl_lo_ftsmax', 'N23cpu_last_branch_address4DOT_19E',
           'pci_dma_rw_ctrl', 'MA_ALL_TRAPS', 'rdi_status',
           'nvram_access', 'rlp_regs', 'sbdc_debug',
           'known_mailboxes',
           'N23cpu_last_branch_address4DOT_194DOT_20E', 'int64_t',
           'asf_control', 'rdma_misc_ctrl_1', 'rdma_misc_ctrl_2',
           'rsdp2_t', 'mbuf', 'pcie_dl_packet_bist', 'grc_regs',
           'rsdp_t', 'rbd_error_flags', 'int_fast64_t',
           'rbdi_ring_replenish_threshold', 'CLOAK_DIS_ACK',
           'emac_mac_addr', 'RBD_RULE_HDR_IP', 'sdc_regs',
           'N12status_block4DOT_76E', 'cpmu_control', 'TG3_MAGIC',
           'tcp_seg_ctrl_regs', 'N7ma_mode4DOT_514DOT_52E',
           'emac_led_control', 'N16cfg_port_pci_sid4DOT_11E',
           'asf_smbus_driver_select', 'TX_STD_ENQ_CMD',
           'grc_clock_ctrl']
