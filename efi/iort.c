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

/*
 * The ARM counterpart of werk.c's DMAR handling.
 *
 * An ARM UEFI platform has no DMAR table -- DMAR is Intel VT-d only.
 * The OS instead learns the SMMU (ARM's IOMMU) topology, and programs
 * DMA isolation, from the ACPI IORT (I/O Remapping Table). walk_iort()
 * neutralises the IORT the way walk_dmar() neutralises DMAR: by default
 * (DISABLE_IORT) it renames the table signature, so the OS never
 * parses it and leaves the SMMU unconfigured for device DMA isolation.
 * The RMR path -- a surgical identity map, the analogue of a DMAR RMRR
 * -- is built by create_rmr() but stays gated off behind
 * IDENTITY_MAP_RMR, exactly as IDENTITY_MAP_* are for DMAR in werk.c.
 */

#include "dmarf.h"

const char *iort_node_name(u8 type)
{
	switch (type) {
	case IORT_NODE_ITS_GROUP:       return "ITS group";
	case IORT_NODE_NAMED_COMPONENT: return "named component";
	case IORT_NODE_ROOT_COMPLEX:    return "PCIe root complex";
	case IORT_NODE_SMMU_V1V2:       return "SMMUv1/v2";
	case IORT_NODE_SMMU_V3:         return "SMMUv3";
	case IORT_NODE_PMCG:            return "PMCG";
	case IORT_NODE_RMR:             return "reserved memory range";
	default:                        return "unknown";
	}
}

void walk_iort_node(struct iort_node *n)
{
	DbgPrint(L"\n");
	DbgPrint(L"iort node type: %d (%a)\n", n->type, iort_node_name(n->type));
	DbgPrint(L"iort node length: %d\n", n->length);
	DbgPrint(L"iort node revision: %d\n", n->rev);
	DbgPrint(L"iort node id mappings: %d at node offset %d\n",
		 n->mapping_count, n->mapping_offset);

	if (n->type == IORT_NODE_SMMU_V1V2 || n->type == IORT_NODE_SMMU_V3) {
		struct iort_smmu *s = (struct iort_smmu *)n;
		DbgPrint(L"iort smmu base address: %lx\n", s->base_address);
	}

	for (u32 i = 0; i < n->mapping_count; i++) {
		struct iort_id_mapping *m = (struct iort_id_mapping *)
			((uintptr_t)n + n->mapping_offset
			 + i * sizeof(struct iort_id_mapping));
		DbgPrint(L"  id map: input %08x count %08x output %08x "
			 L"node ref %x\n", m->input_base, m->id_count,
			 m->output_base, m->output_reference);
	}
}

/*
 * Append an RMR node identity-mapping [base, limit] for the Tigon NIC
 * specifically -- the SMMU analogue of werk.c's device-scoped
 * create_rmrr(). The Tigon's PCIe Requester ID (tg_rid, captured by
 * main.c when the driver binds) is resolved to its SMMU StreamID
 * through the PCIe root complex node's ID mappings, and the RMR is
 * scoped to that StreamID alone. Returns the bytes appended, or 0 if
 * the device or its StreamID could not be resolved. Reached only when
 * IDENTITY_MAP_RMR is set.
 */
u32 create_rmr(void *a, u64 base, u64 limit)
{
	struct iort_tbl_hdr *iort = a;
	struct iort_node *rc = 0;
	struct iort_rmr *r;
	struct iort_id_mapping *map;
	struct iort_rmr_desc *desc;
	u32 offset = iort->node_offset;
	u32 smmu_ref = 0;
	u32 stream_id = 0;
	int resolved = 0;
	u32 len;

	if (tg_rid == 0)
		return 0;

	/* find the PCIe root complex node */
	for (u32 i = 0; i < iort->node_count && offset < iort->length; i++) {
		struct iort_node *n = (struct iort_node *)((uintptr_t)a + offset);
		if (n->length == 0 || offset + n->length > iort->length)
			break;
		if (n->type == IORT_NODE_ROOT_COMPLEX) {
			rc = n;
			break;
		}
		offset += n->length;
	}
	if (rc == 0)
		return 0;

	/* resolve the Tigon's Requester ID to its SMMU StreamID through
	   the root complex node's ID mappings; the matching mapping also
	   names the target SMMU node. */
	for (u32 i = 0; i < rc->mapping_count; i++) {
		struct iort_id_mapping *m = (struct iort_id_mapping *)
			((uintptr_t)rc + rc->mapping_offset
			 + i * sizeof(struct iort_id_mapping));
		if (m->flags & 1) {                    /* single mapping */
			stream_id = m->output_base;
			smmu_ref = m->output_reference;
			resolved = 1;
			break;
		}
		if (tg_rid >= m->input_base
		    && tg_rid < m->input_base + m->id_count) {
			stream_id = m->output_base + (tg_rid - m->input_base);
			smmu_ref = m->output_reference;
			resolved = 1;
			break;
		}
	}
	if (!resolved)
		return 0;

	r = (struct iort_rmr *)((uintptr_t)a + iort->length);
	len = sizeof(struct iort_rmr) + sizeof(struct iort_id_mapping)
	    + sizeof(struct iort_rmr_desc);

	r->node.type = IORT_NODE_RMR;
	r->node.length = len;
	r->node.rev = 3;                 /* IORT revision E defines the RMR */
	r->node.identifier = 0;
	r->node.mapping_count = 1;
	r->node.mapping_offset = sizeof(struct iort_rmr);
	r->flags = 0;
	r->desc_count = 1;
	r->desc_offset = sizeof(struct iort_rmr)
	               + sizeof(struct iort_id_mapping);

	/* scope the RMR to the Tigon's StreamID alone */
	map = (struct iort_id_mapping *)((uintptr_t)r + r->node.mapping_offset);
	map->input_base = 0;
	map->id_count = 1;
	map->output_base = stream_id;
	map->output_reference = smmu_ref;
	map->flags = 0;

	desc = (struct iort_rmr_desc *)((uintptr_t)r + r->desc_offset);
	desc->base = base;
	desc->length = limit - base + 1;
	desc->reserved = 0;

	return len;
}

void walk_iort(void *a)
{
	struct iort_tbl_hdr *iort = a;
	u32 offset = iort->node_offset;
	u32 created = 0;

	DbgPrint(L"table sig: %.4a\n", iort->sig);
	DbgPrint(L"table len: %d\n", iort->length);
	DbgPrint(L"table rev: %d\n", iort->rev);
	DbgPrint(L"\n");
	DbgPrint(L"oemid: %.6a\n", iort->oemid);
	DbgPrint(L"iort node count: %d\n", iort->node_count);
	DbgPrint(L"iort node offset: %d\n", iort->node_offset);

	for (u32 i = 0; i < iort->node_count && offset < iort->length; i++) {
		struct iort_node *n = (struct iort_node *)((uintptr_t)a + offset);

		if (n->length == 0) {
			DbgPrint(L"\nzero-length node at offset %d -- stopping\n",
				 offset);
			break;
		}
		DbgPrint(L"\niort node at offset %d\n", offset);
		walk_iort_node(n);
		offset += n->length;
	}

#if !DISABLE_IORT
#if IDENTITY_MAP_RMR
	created = create_rmr(a, 0, 0xffffff);
	if (created) {
		iort->length += created;
		iort->node_count += 1;
		DbgPrint(L"\n\nnew RMR node appended (%d bytes)\n", created);
	}
#endif
#endif
	if (!created) {
		DbgPrint(L"\n\nIORT!\n");
		CopyMem(iort->sig, "TROI", 4);
	}

	update_tbl_cksum(a);
}
