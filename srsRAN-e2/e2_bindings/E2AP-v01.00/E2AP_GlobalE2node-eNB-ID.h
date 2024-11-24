/*
 * Generated by asn1c-0.9.29 (http://lionet.info/asn1c)
 * From ASN.1 module "E2AP-IEs"
 * 	found in "/local/mnt/openairinterface5g/openair2/RIC_AGENT/MESSAGES/ASN1/R01/e2ap-v01.00.asn1"
 * 	`asn1c -pdu=all -fcompound-names -gen-PER -no-gen-OER -no-gen-example -fno-include-deps -fincludes-quoted -D /local/mnt/openairinterface5g/cmake_targets/ran_build/build/CMakeFiles/E2AP/`
 */

#ifndef	_E2AP_GlobalE2node_eNB_ID_H_
#define	_E2AP_GlobalE2node_eNB_ID_H_


#include "asn_application.h"

/* Including external dependencies */
#include "E2AP_GlobalENB-ID.h"
#include "constr_SEQUENCE.h"

#ifdef __cplusplus
extern "C" {
#endif

/* E2AP_GlobalE2node-eNB-ID */
typedef struct E2AP_GlobalE2node_eNB_ID {
	E2AP_GlobalENB_ID_t	 global_eNB_ID;
	/*
	 * This type is extensible,
	 * possible extensions are below.
	 */
	
	/* Context for parsing across buffer boundaries */
	asn_struct_ctx_t _asn_ctx;
} E2AP_GlobalE2node_eNB_ID_t;

/* Implementation */
extern asn_TYPE_descriptor_t asn_DEF_E2AP_GlobalE2node_eNB_ID;
extern asn_SEQUENCE_specifics_t asn_SPC_E2AP_GlobalE2node_eNB_ID_specs_1;
extern asn_TYPE_member_t asn_MBR_E2AP_GlobalE2node_eNB_ID_1[1];

#ifdef __cplusplus
}
#endif

#endif	/* _E2AP_GlobalE2node_eNB_ID_H_ */
#include "asn_internal.h"
