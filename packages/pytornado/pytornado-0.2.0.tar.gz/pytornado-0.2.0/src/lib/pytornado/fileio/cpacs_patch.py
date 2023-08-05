#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################################################################################
# ----- (START) Temporary fix -----
# REASON: TiGL 3.0.0-rc2 does not yet have any control surface functions implemented
###################################################################################


def PATCH_getControlSurfaceCount(tixi, comp_seg_uid):
    """
    Function to get the number of Control Surfaces

    Function 'getControlSurfaceCount' returns the number of control surface
    (only TED) on a given component segment.

    Args:
        :tixi (TIXI Handle): TIXI Handle of the CPACS file
        :comp_seg_uid (str): UID of the component segment

    Returns:
        :contrl_surf_count (integer): Number of control surfaces on the component segment

    Note:
        * Written by Aidan Jungo
    """

    if not tixi.checkDocumentHandle():
        ValueError('Probleme with TIXI handle')

    if not tixi.uIDCheckExists(comp_seg_uid):
        raise ValueError(f"No UID named '{comp_seg_uid}' has been found!")

    comp_sec_xpath = tixi.uIDGetXPath(comp_seg_uid)
    contrl_surf_xpath = comp_sec_xpath + \
        '/controlSurfaces/trailingEdgeDevices/trailingEdgeDevice'

    contrl_surf_count = tixi.xPathEvaluateNodeNumber(contrl_surf_xpath)

    return contrl_surf_count


def PATCH_getControlSurfaceUID(tixi, comp_seg_uid, index):
    """
    Function to get the Control Surface UID

    Function 'getControlSurfaceUID' return the Control Surface UID for a given
    component segment UID and controlSurfaces index.

    Args:
        tixi (TIXI Handle): TIXI Handle of the CPACS file
        comp_seg_uid (str): UID of the component segment
        index (integer): Index of the Control Surface

    Returns:
        contrl_surf_count (integer): Number of Control Surfaces on the component segment

    Note:
        * Written by Aidan Jungo
    """

    if not tixi.checkDocumentHandle():
        ValueError('Probleme with TIXI handle')

    if not tixi.uIDCheckExists(comp_seg_uid):
        raise ValueError(f"No UID named {comp_seg_uid} has been found!")

    comp_sec_xpath = tixi.uIDGetXPath(comp_seg_uid)
    contrl_surf_xpath = comp_sec_xpath + '/controlSurfaces/trailingEdgeDevices \
                        /trailingEdgeDevice[' + str(index) + ']'

    if not tixi.checkElement(contrl_surf_xpath):
        raise ValueError('No control surface for this UID at this index')

    contrl_surf_uid = tixi.getTextAttribute(contrl_surf_xpath, 'uID')

    return contrl_surf_uid

###################################################################################
# ----- (END) Temporary fix -----
###################################################################################
