"""
    the name of the PK is not consistent everywhere, some tables also have 
    composite PK-keys. If a table is mentioned in the dict below, it does
    not adhere to the conventional name of 'id' for the primary key in that
    table. To make the proper select query, we need to give the key(s) as a
    tuple back. For this we use a slave function.

    NOTICE there is a high likelihood of bugs in here, some elements might be
    marked as keys, but are not populated in the on_id2 field by SIIS's dev team.
"""

pks_columns = {
    # 'arcfragattributesdetail'
    'arcfragclamphole' : ['arcFragAttributesDetail_id'],
    'arcfragdowelhole' : ['arcFragAttributesDetail_id'],
    # 'arcfragdegreeofunfinished'
    'arcfragstonecarving' : ['arcFragAttributesDetail_id'], 
    # 'arcfragstonetype'
    # 'arcfragstonecarvingtype'
    # 'arcfragfunctionalcategory'
    # 'arcfragoriginallocation'
    # 'arcfragexecution'
    # 'arcfragattributeface'
    # 'activity_log'
    # 'arcfragattributetype'
    # 'arcfragflatsurftreatmenttype'
    # 'arcfragclampholeshape'
    # 'arcfragspecificfunctionalcategory'
    # 'arcfragvariant2'
    # 'arcfragvariant3'
    # 'architecturalfeaturesubtype'
    # 'arcfragtype'
    # 'arcfragvariant1'
    # 'architecturalfeaturetype'
    'architecturalfeature' : ['locus_id', 'id_local'], 
    'architecturalfragment' : ['find_id'], 
    # 'change_log'
    # 'change_log_archive'
    'chronologymethodology' : ['chronology_id', 'methodology_id'], 
    'chronologyperiods' : ['chronology_id'],
    'chronologypottery' : ['chronology_id', 'characteristic'], 
    'chronologysrswphase' : ['chronology_id', 'srswPhase'], 
    'coin' : ['find_id'], 
    # 'compactiontype' 
    # 'compositiontype'
    # 'collatedloci'
    'chronology' : ['uuid'], 
    # 'crs'
    # 'hecarvedstonethickness'
    # 'find'
    # 'geometry'
    'graffiti' : ['locus_id', 'id_local'], 
    # 'geometry_type'
    'hefloor' : ['locus_id'], 
    # 'dynasty'
    'concentration' : ['locus_id'],
    # 'data_zone'
    # 'concentrationmaterialcategory'
    # 'hecarvedstonetype'
    'hefloormosaicmaterial' : ['floor_id', 'material_id'], 
    'hefloormosaicsubtechnique' : ['floor_id', 'subTechnique_id'], 
    'hefloorpavedmaterial' : ['floor_id', 'pavedMaterial_id'], 
    # 'hefloorof'
    'hefloorcarvedstonetype' : ['floor_id', 'carvedStoneType_id'], 
    'hefloorgameboard' : ['floor_id', 'id_local'], 
    'hesuperstructure' : ['locus_id'],
    'hesuperstructurevaultmaterial' : ['vault_id', 'material_id'], 
    'hevault' : ['superstructure_id'], 
    # 'hevaultmaterial'
    # 'hevaultjoints'
    # 'hevaulttechnique'
    'layer' : ['locus_id'], 
    # 'inclusions_quantity'
    # 'inclusions_size'
    # 'kingsemperors'
    # 'layersubtype2'
    # 'layersubtype3'
    # 'inclusions_nature'
    'hefloorstonemasonsmark' : ['floor_id', 'id_local'],
    'hefloortiledimensions' : ['floor_id', 'id_local'], 
    # 'hepavedjoints' : 
    # 'hefloortechnique'
    # 'hemosaicmaterial'
    # 'hemosaicsubtechnique'
    # 'hesuperstructuresubtype'
    # 'layercolor'
    # 'locus_type'
    # 'material_category'
    # 'placephase'
    'machine' : ['hostname'], 
    # 'polylocisurveyarea'
    'polyloci' : ['polylociID'],
    'polylocilocus' : ['polyloci_id', 'locus_id'], 
    'polylocisurvey' : ['polylociSurveyID'], 
    'polylocisurveycategory' : ['polylociSurvey_id', 'category_id'], 
    # 'polysurveycategories' : 
    # 'locus_subtype_1'
    'metadata' : ['the_key'], 
    # 'methodology'
    'locusinclusions' : ['uuid'], 
    # 'periods'
    # 'material_class'
    # 'suprasite'
    # 'relatedlociposition'
    'restorablevessel' :  ['uuid'], 
    'sample' : ['sampleID'], 
    # 'site' 
    'spolia' : ['locus_id', 'id_local'], 
    # 'survey'
    # 'polysurveytitlecategories'
    'surveypolylocisurvey' : ['polylociSurvey_id', 'survey_id'], 
    # 'sync_activity'
    # 'tbl_context'
    'user': ['username'], 
    # 'reign'
    'relatedlocus' : ['locus_id', 'relatedToLocus'], 
    # 'relatedlocinature'
    # 'veprogressofexcavation'
    'vebrickcourse' : ['verticalElevation_id', 'id_local'], 
    'vebricktype' : ['verticalElevation_id', 'id_local'],
    'vecutstone' : ['verticalElevation_id'], 
    'vefinishing' : ['verticalElevation_id', 'id_local'], 
    'vefinishingcladding' : ['verticalElevation_id', 'finishing_id'], 
    'vefinishingcolor' : ['verticalElevation_id', 'finishing_id'], 
    # 'vefinishingsubtype'
    # 'vefinishingtype'
    'velocusstonetype' : ['verticalElevation_id', 'stoneType_id'],
    # 'vejoints'
    # 'user_role'
    # 'user_role_type'
    'vebrick' : ['verticalElevation_id'], 
    # 'vematerialbond'
    # 'vebrickmorphology'
    # 'veconstructiontype'
    # 'vecladdingmaterial'
    # 'vebuildingmaterial'
    # 'veface'
    # 'vefunction'
    # 'veorientationaxis'
    # 'vestoneform'
    # 'view_architecturalfragment'
    # 'view_coin'
    # 'view_find'
    'vestonecourse' : ['verticalElevation_id', 'id_local'], 
    # 'vestonetype'
    # 'vesubfunction'
    'hefloorcarvedstonethickness' : ['floor_id', 'carvedStoneThickness_id'], 
    # 'locus'
    'verticalelevation' : ['locus_id']
    # 'arcfragobject'
    # 'hepavedmaterial' : 
    # 'veconstructionsubtype'
}

def extract_pk_column(table):
    if table not in pks_columns: 
        return ['id']
    else: 
        return pks_columns[table]
