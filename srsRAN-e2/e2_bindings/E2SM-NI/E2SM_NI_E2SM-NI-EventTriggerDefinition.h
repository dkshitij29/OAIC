/*
 * Generated by asn1c-0.9.29 (http://lionet.info/asn1c)
 * From ASN.1 module "E2SM-NI-IEs"
 * 	found in "/local/mnt/openairinterface5g/openair2/RIC_AGENT/MESSAGES/ASN1/R01/e2sm-ni-v01.00.asn1"
 * 	`asn1c -pdu=all -fcompound-names -gen-PER -no-gen-OER -no-gen-example -fno-include-deps -fincludes-quoted -D /local/mnt/openairinterface5g/cmake_targets/ran_build/build/CMakeFiles/E2SM-NI/`
 */

#ifndef	_E2SM_NI_E2SM_NI_EventTriggerDefinition_H_
#define	_E2SM_NI_E2SM_NI_EventTriggerDefinition_H_


#include "asn_application.h"

/* Including external dependencies */
#include "E2SM_NI_E2SM-NI-EventTriggerDefinition-Format1.h"
#include "constr_CHOICE.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Dependencies */
typedef enum E2SM_NI_E2SM_NI_EventTriggerDefinition_PR {
	E2SM_NI_E2SM_NI_EventTriggerDefinition_PR_NOTHING,	/* No components present */
	E2SM_NI_E2SM_NI_EventTriggerDefinition_PR_eventDefinition_Format1
	/* Extensions may appear below */
	
} E2SM_NI_E2SM_NI_EventTriggerDefinition_PR;

/* E2SM_NI_E2SM-NI-EventTriggerDefinition */
typedef struct E2SM_NI_E2SM_NI_EventTriggerDefinition {
	E2SM_NI_E2SM_NI_EventTriggerDefinition_PR present;
	union E2SM_NI_E2SM_NI_EventTriggerDefinition_u {
		E2SM_NI_E2SM_NI_EventTriggerDefinition_Format1_t	 eventDefinition_Format1;
		/*
		 * This type is extensible,
		 * possible extensions are below.
		 */
	} choice;
	
	/* Context for parsing across buffer boundaries */
	asn_struct_ctx_t _asn_ctx;
} E2SM_NI_E2SM_NI_EventTriggerDefinition_t;

/* Implementation */
extern asn_TYPE_descriptor_t asn_DEF_E2SM_NI_E2SM_NI_EventTriggerDefinition;

#ifdef __cplusplus
}
#endif

#endif	/* _E2SM_NI_E2SM_NI_EventTriggerDefinition_H_ */
#include "asn_internal.h"
