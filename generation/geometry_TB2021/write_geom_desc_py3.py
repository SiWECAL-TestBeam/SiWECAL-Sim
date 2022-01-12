#!/usr/bin/env python3

#
# this script writes the dd4hep geometry description file for various TB configurations
# Based on the one from DJeans 31 october 2017
# https://gitlab.cern.ch/calice/calice_dd4heptestbeamsim/-/blob/master/2017_SiECAL_DESY/write_geom_desc.py
# Updated for TB2021 Fabricio Jimenez Morales: fabricio.jm@cern.ch

# to run for config #1:
# $> python write_geom_desc.py 1

import sys

def writeCommonStuff(config):

    # preliminary stuff
    print('<lccdd xmlns:compact="http://www.lcsim.org/schemas/compact/1.0"')
    print('xmlns:xs="http://www.w3.org/2001/XMLSchema"')
    print('xs:noNamespaceSchemaLocation="http://www.lcsim.org/schemas/compact/1.0/compact.xsd">')
    print('<info name="SiW-TB-2021_conf'+str(config)+'_v03"') # Not sure about this versioning, see below in line 'detector name="EcalTestBeam"'
    print('    title="SiW-TB-2021_conf'+str(config)+'_v03"')
    print('    author="F. Jimenez Morales"')
    print('    url="cern.ch"')
    print('    status="development"')
    print('    version="$Id$">')
    print('    <comment>')
    print('   The compact File for the SiECAL TB Setup at DESY (2021) ')
    print('   configuration ' + str(config))
    print('   updated geom December 2021')
    print('   fabricio.jm@cern.ch')
    print('</comment>')
    print('</info>')
    print('<includes>')
    print('<gdmlFile  ref="${DD4hepINSTALL}/DDDetectors/compact/elements.xml"/>')
    print('<gdmlFile  ref="${DD4hepINSTALL}/DDDetectors/compact/materials.xml"/>')
    print('<gdmlFile  ref="./extra_materials.xml"/>')
    print('</includes>')
    print('<plugins>')
    print('<plugin name="InstallSurfaceManager"/>')
    print('</plugins>')
    print('<define>')
    print('<constant name="world_side" value="80000*mm"/>')
    print('<constant name="world_x" value="world_side"/>')
    print('<constant name="world_y" value="world_side"/>')
    print('<constant name="world_z" value="world_side"/>')
    print('<!-- to limit the amount of MCParticles stored -->')
    print('<constant name="tracker_region_rmax" value="1*cm" />')
    print('<constant name="tracker_region_zmax" value="1*cm" />')
    print('</define>')
    print('<limits>')
    print('<limitset name="cal_limits">')
    print('<limit name="step_length_max" particles="*" value="5.0" unit="mm" />')
    print('</limitset>')
    print('</limits>')
    print('<comment>Common Generic visualization attributes</comment>')
    print('<display>')
    print('<vis name="InvisibleNoDaughters"      showDaughters="false" visible="false"/>')
    print('<vis name="InvisibleWithDaughters"    showDaughters="true" visible="false"/>')
    print('<vis name="GreenVis"   alpha="1" r="0.0" g="1.0" b="0.0" showDaughters="true" visible="true"/>')
    print('<vis name="RedVis"     alpha="1" r="1.0" g="0.0" b="0.0" showDaughters="true" visible="true"/>')
    print('<vis name="BlueVis"    alpha="1" r="0.0" g="0.0" b="1.0" showDaughters="true" visible="true"/>')
    print('<vis name="InVis"     alpha="1.0"  r="0.0" g="1.0"  b="0.0" showDaughters="true"  visible="false"/>')
    print('</display>')
    print('<define>')
    print('<include ref="ECAL_commondefs.xml"/>')
    print('</define>')
    print('<display>')
    print('<include ref="ECAL_commondisp.xml"/>')
    print('</display>')
    print('<readouts>')
    print('<readout name="SiEcalCollection">')
    print('<segmentation type="TiledLayerGridXY" grid_size_x="Ecal_CellSizeX" grid_size_y="Ecal_CellSizeX" offset_x="-Ecal_dim_x/2.0" offset_y="-Ecal_dim_y/2.0" />')
    print('<id>system:8,layer:8,x:8,y:8,slice:4</id>')
    print('</readout>')
    print('</readouts>')
    print('<detectors>')
    print('<detector name="EcalTestBeam" type="CaloPrototype_v02" vis="EcalVis" id="3" readout="SiEcalCollection" insideTrackingVolume="false">')
    print('<dimensions x="Ecal_dim_x" y="Ecal_dim_y" z="Ecal_dim_z"/>')
    print('<common_parameters frontFaceZ="Ecal_FrontFaceZ" nCellsX="Ecal_NcellsX" nCellsY="Ecal_NcellsY" cellSizeX="Ecal_CellSizeX" cellSizeY="Ecal_CellSizeY"/> ')
    print('<type_flags type="1" />')
    print('<envelope vis="EcalVis">')
    print('<shape type="Box" dx="Ecal_dim_x/2.0 + env_safety" dy="Ecal_dim_y/2.0 + env_safety"  dz="Ecal_dim_z/2.0 + env_safety" material="Air" />')
    print('<rotation x="0" y="0" z="0"/>')
    print('<position x="0" y="0" z="Ecal_dim_z/2.0"/>')
    print('</envelope>')


#give a layerconfig, write the xml file for dd4hep
def write_geom_xml(layerconfig):
    # check input is reasonable
    if len(layerconfig)<1:
        print('empty layer config')
        return
    # TODO: Put here the plastic PLATE!!!
    print('<slice material = "Air"         thickness = "27*mm"   vis="Invisible"/>')
    # the layers of the prototype
    for layer in layerconfig:
        nAbs=layer[0]
        slab=layer[1]
        Si_z=layer[2]
        if nAbs<0 or nAbs>2:
            print('crazy number of W plates!', nAbs)
            exit
        nAir=2-nAbs
        print('<layer repeat="1" vis="EcalVis">')
        if nAir>0:
            print('<slice material = "Air" thickness = "'+str(nAir)+'*Ecal_WThickness"  vis="AirVis" />')
        if nAbs>0:
            print('<slice material = "TungstenDens1910" thickness = "'+str(nAbs)+'*Ecal_WThickness"  vis="TungstenVis" />')
        
        if slab:
            print('<slice material = "CarbonFiber" thickness = "Ecal_CFThickness"        vis="CFVis"/>')
            print('<slice material = "Cu"          thickness = "Ecal_KaptonThickness"    vis="CuVis" />')
            print('<slice material = "Air"         thickness = "Ecal_GlueThickness_kap"  vis="AirVis"/>')
            print('<slice material = "Si"          thickness = "Ecal_WaferThickness'+str(Si_z)+'"     vis="SiVis" sensitive = "yes" />')
            print('<slice material = "Air"         thickness = "Ecal_GlueThickness_pcb"  vis="AirVis"/>')
            # Below: Copper layer (not kapton? but same thicknes but same thicknesss)
            print('<slice material = "Cu"          thickness = "Ecal_KaptonThickness"    vis="CuVis" />')
            print('<slice material = "PCB"         thickness = "Ecal_PcbThickness"       vis="PCBVis" />')
            print('<slice material = "Air"         thickness = "Ecal_ChipThickness"       vis="AirVis" />')
            print('<slice material = "Air"         thickness = "Ecal_w_slab_gap'+str(Si_z)+'"        vis="AirVis"/>')
        else:
            print('<slice material = "Air" thickness = "Ecal_LayerDistance-2*Ecal_WThickness" vis="AirVis"/>')

        print('</layer>')
    # postscriptum
    print('</detector>')
    print('</detectors>')

#final tag
    print('</lccdd>')

# define layerconfig structure
# an array of pairs: one entry per layer
# each layer has an integer = # of W plates, and a bool = presence of detector slab
# there are two configurations, no W (conf 0) and with W (conf 1) which were used in Nov 2021 TB
def defineLayerConfig(iconf):
    layerconfig=[]
    if iconf == 0:
        print("Not implemented yet, conf 0")
        exit
    # probably for 2021 deprecate the bool, second element in appends below
    elif iconf==1:
        layerconfig.append( [0, True, 320] ) # no absorber
        layerconfig.append( [1, True, 320] )
        layerconfig.append( [1, True, 320] )
        layerconfig.append( [1, True, 320] )
        layerconfig.append( [1, True, 320] )
        layerconfig.append( [1, True, 320] )
        layerconfig.append( [1, True, 320] )
        layerconfig.append( [1, True, 500] ) # 0.5mm wafer
        layerconfig.append( [1, True, 500] ) # 0.5mm wafer
        layerconfig.append( [1, True, 500] ) # 0.5mm wafer
        layerconfig.append( [1, True, 500] ) # 0.5mm wafer
        layerconfig.append( [1, True, 320] )
        layerconfig.append( [2, True, 320] )
        layerconfig.append( [2, True, 320] )
        layerconfig.append( [2, True, 320] )
    else:
        print('unknown config index', iconf)
        exit

    return layerconfig



if len(sys.argv)==2:
    iconfig=int(sys.argv[1])
    lconf=defineLayerConfig(iconfig)
    writeCommonStuff(iconfig)
    write_geom_xml(lconf)
else:
    print('need to give single argument')
    print('write_geom_desc.py #conf')
